# Generated by Django 4.2.1 on 2023-06-30 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_sourcepage_human_reviewed_sourcepage_last_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='zoterosource',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]