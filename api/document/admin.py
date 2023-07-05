from django.contrib import admin
from document.models import *

class SourcePageAdmin(admin.ModelAdmin):
	readonly_fields=['page_url','image_filename','iiif_manifest_url','iiif_baseimage_url']
	search_fields=['page_url','image_filename']
	list_display=['page_url','image_filename']
	model=SourcePage

class SourcePageConnectionInline(admin.StackedInline):
	model=SourcePageConnection
	extra=0
	fields=['source_page']
	classes = ['collapse']

class ZoteroSourceAdmin(admin.ModelAdmin):
	model=ZoteroSource
	readonly_fields=['item_url','zotero_url','legacy_source']
	autocomplete_fields=('voyages','enslaved_people','enslavers')
	list_display=('zotero_title','zotero_date')

admin.site.register(ZoteroSource, ZoteroSourceAdmin)
admin.site.register(SourcePage,SourcePageAdmin)

# admin.site.register(SourcePage)
# admin.site.register(SourcePageConnectionInline)