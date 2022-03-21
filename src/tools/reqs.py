import pprint
import urllib
from django.db.models import Avg,Sum,Min,Max,Count
from django.db.models.aggregates import StdDev
from .nest import *

#GENERIC FUNCTION TO RUN A GET CALL ON REST SERIALIZERS
##Default is to auto prefetch, but need to be able to turn it off.
##For instance, on our PAST graph-like data, the prefetch can overwhelm the system if you try to get everything
##can also just pass an array of prefetch vars

def get_req(queryset,s,r,options_dict,auto_prefetch=True,retrieve_all=False):
	
	params=r.GET
	pp = pprint.PrettyPrinter(indent=4)
	print("--get req params--")
	pp.pprint(dict(r.GET))
		
	#SELECT SPECIFIC FIELDS TO RETURN
	selected_fields=params.get('selected_fields')
	if selected_fields is not None:
		selected_fields=[i for i in selected_fields.split(',')]
	else:
		selected_fields=[]
	
	#INCLUDE AGGREGATION FIELDS
	aggregations_param=params.get('aggregate_fields')
	
	if aggregations_param is not None:
		valid_aggregation_fields=[f for f in options_dict if 'Integer' in options_dict[f]['type'] or 'Decimal' in options_dict[f]['type']]
		aggregation_fields=[f for f in aggregations_param.split(',') if f in valid_aggregation_fields]
		selected_fields=[]
		auto_prefetch=False
	else:
		aggregation_fields=[]
	
	all_fields={i:options_dict[i] for i in options_dict if 'type' in options_dict[i]}
	active_fields=list(set([i for i in params]+selected_fields+aggregation_fields).intersection(set(all_fields)))
	
	#ORDER RESULTS
	order_by=params.get('order_by')
	if order_by is not None:
		order_by=order_by.split(',')
		print('--order by--')
		print(order_by)
		queryset=queryset.order_by(*order_by)
	
	###FILTER RESULTS
	##select text and numeric fields, ignoring those without a type
	text_fields=[i for i in all_fields if 'CharField' in all_fields[i]['type']]
	numeric_fields=[i for i in all_fields if 'IntegerField' in all_fields[i]['type'] or 'DecimalField' in all_fields[i]['type'] or 'FloatField' in all_fields[i]['type']]
	boolean_fields=[i for i in all_fields if 'BooleanField' in all_fields[i]['type']]
	
	##build filters
	kwargs={}
	###numeric filters
	active_numeric_search_fields=[i for i in set(params).intersection(set(numeric_fields))]
	if len(active_numeric_search_fields)>0:
		for field in active_numeric_search_fields:
			vals=[float(i) for i in params.get(field).split(',')]
			vals.sort()
			min,max=vals
			kwargs['{0}__{1}'.format(field, 'lte')]=max
			kwargs['{0}__{1}'.format(field, 'gte')]=min
	###text filters (inexact match)
	active_text_search_fields=[i for i in set(params).intersection(set(text_fields))]
	if len(active_text_search_fields)>0:
		for field in active_text_search_fields:
			searchstring=params.get(field)
			kwargs['{0}__{1}'.format(field, 'icontains')]=searchstring
	active_boolean_search_fields=[i for i in set(params).intersection(set(boolean_fields))]
	if len(active_boolean_search_fields)>0:
		for field in active_boolean_search_fields:
			searchstring=params.get(field)
			if searchstring.lower() in ["true","t","1","yes"]:
				searchstring=True
			elif searchstring.lower() in ["false","f","0","no"]:
				searchstring=False
			
			if searchstring in [True,False]:
				kwargs[field]=searchstring
	
	###apply filters
	queryset=queryset.filter(**kwargs)
	results_count=queryset.count()
	print('--counts--')
	print("resultset size:",results_count)
	
	#PREFETCH REQUISITE FIELDS
	if auto_prefetch:
		prefetch_keys=list(options_dict.keys())
	else:
		prefetch_keys = active_fields
	
	#print(prefetch_keys)
	##ideally, I'd run this list against the model and see
	##which were m2m relationships (prefetch_related) and which were 1to1 (select_related)
	prefetch_vars=list(set(['__'.join(i.split('__')[:-1]) for i in prefetch_keys if '__' in i]))
	for p in prefetch_vars:
		queryset=queryset.prefetch_related(p)
	#print('--prefetch--')
	#print(prefetch_vars)
	
	#AGGREGATIONS
	##e.g. voyage_slaves_numbers__imp_total_num_slaves_embarked__sum
	aggregations_param=params.get('aggregate_fields')
	
	if aggregation_fields != []:
		aggqueryset=[]
		selected_fields=[]
		for aggfield in aggregation_fields:
			for aggsuffix in ["sum","avg","min","max","count","stddev"]:
				selected_fields.append(aggfield+"_"+aggsuffix)
			aggqueryset.append(queryset.aggregate(Sum(aggfield)))
			aggqueryset.append(queryset.aggregate(Avg(aggfield)))
			aggqueryset.append(queryset.aggregate(Min(aggfield)))
			aggqueryset.append(queryset.aggregate(Max(aggfield)))
			aggqueryset.append(queryset.aggregate(Max(aggfield)))
			aggqueryset.append(queryset.aggregate(StdDev(aggfield)))
		queryset=aggqueryset
		
	#PAGINATION/LIMITS
	if retrieve_all==False:
		default_results_per_page=10
		results_per_page=params.get('results_per_page')
		if results_per_page==None:
			results_per_page=default_results_per_page
		else:
			results_per_page=int(results_per_page)
		results_page=params.get('results_page')
		def urlunencode(d):
			d2=dict(d)
			for k in d:
				d2[k]=str(d[k])
			return(d2)
		if results_page==None or results_page=='':
			results_page=1
			prev_uri=None
			next_dict=urlunencode(params)
			urlunencode(next_dict)
			next_dict['results_page']=2
			next_uri='?'.join([r.build_absolute_uri('?'),urllib.parse.urlencode(next_dict)])
		else:
			results_page=int(results_page)
			params_dict=urlunencode(params)
			params_dict['results_per_page']=results_per_page
			if results_page==1:
				prev_uri=None
				next_dict=params_dict
				next_dict['results_page']=2
				next_uri='?'.join([r.build_absolute_uri('?'),urllib.parse.urlencode(next_dict)])
			else:
				next_dict=dict(params_dict)
				prev_dict=dict(params_dict)
				prev_dict['results_page']=results_page-1
				next_dict['results_page']=results_page+1
				next_uri='?'.join([r.build_absolute_uri('?'),urllib.parse.urlencode(next_dict)])
				prev_uri='?'.join([r.build_absolute_uri('?'),urllib.parse.urlencode(prev_dict)])
		if (results_page)*results_per_page>results_count:
			next_uri=None
		start_idx=(results_page-1)*results_per_page
		end_idx=(results_page)*results_per_page
		queryset=queryset[start_idx:end_idx]
	else:
		next_uri=None
		prev_uri=None
	
	return queryset,selected_fields,next_uri,prev_uri,results_count

def options_handler(self,request,flatfile=None,auto=False):
	"""
	Handler method for 'OPTIONS' request.
	CAN SPECIFY "hierarchical=True to get a nested schema" -- DEFAULT IS FLAT
	"""		
	#GETS A FLAT VERSION OF THE SCHEMA WITH DOUBLE-UNDERSCORES FOR NESTED RELATIONS
	
	schema=flatfile
	
	#AUTO OPTIONS IS
	#OVERKILL FOR THE PUBLIC API
	#WEIRD & FRAGILE
	#GOING TO MOVE TO A MANAGED STATIC OPTIONS ENDPOINT
	#FIRST STEP, REMOVE PUBLIC ACCESS TO AUTO-GENERATED SCHEMA
	#& GET THE STATIC ENDPOINT RIGHT
	if 'auto' in request.query_params:
		if request.query_params['auto'].lower() in ['true','1','y']:
			auto=True
	
	if auto==True:
		schema=options_walker({},'',self.get_serializer())
	else:
		schema=flatfile
	
	hierarchical=True
	if 'hierarchical' in request.query_params:
		if request.query_params['hierarchical'].lower() in ['false','0','n']:
			hierarchical=False
	
	unwound={}
	if hierarchical==True:
		for i in schema:
			payload=schema[i]
			keychain=i.split('__')
			key=keychain[0]
			unwound=addlevel(unwound,keychain,payload)
		schema=unwound
	
	return schema