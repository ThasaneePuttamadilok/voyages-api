# Generated by Django 4.2.1 on 2024-01-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_source_bib_source_thumbnail_transcription'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='manifest_content',
            field=models.JSONField(null=True),
        ),
    ]
