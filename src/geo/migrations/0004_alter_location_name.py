# Generated by Django 4.0.2 on 2022-05-31 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_remove_location_parent_of_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Location name'),
        ),
    ]