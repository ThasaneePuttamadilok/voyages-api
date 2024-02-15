# Generated by Django 4.2.1 on 2024-02-15 17:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0006_page_is_british_library_page_transkribus_pageid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='iiif_manifest_url',
        ),
        migrations.RemoveField(
            model_name='page',
            name='transcription',
        ),
        migrations.AddField(
            model_name='source',
            name='bib',
            field=models.TextField(blank=True, help_text='Formatted bibliography for the Document', null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='manifest_content',
            field=models.JSONField(blank=True, help_text='DCTerms imported from Zotero -- NOT the full manifest', null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='source_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='document.sourcetype'),
        ),
        migrations.AddField(
            model_name='source',
            name='thumbnail',
            field=models.TextField(blank=True, help_text='URL for a thumbnail of the Document', null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='zotero_url',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='docsparsedate',
            name='year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2050)]),
        ),
        migrations.AlterField(
            model_name='source',
            name='has_published_manifest',
            field=models.BooleanField(default=False, verbose_name='Is there a published manifest?'),
        ),
        migrations.AlterField(
            model_name='source',
            name='item_url',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='title',
            field=models.CharField(max_length=1000, verbose_name='Title'),
        ),
    ]
