# Generated by Django 4.0.2 on 2022-07-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0003_remove_doc_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='citation',
            field=models.CharField(max_length=500, null=True),
        ),
    ]