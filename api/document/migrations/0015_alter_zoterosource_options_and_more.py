# Generated by Django 4.2.1 on 2023-08-08 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0014_alter_zoterovoyageconnection_page_range'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zoterosource',
            options={'ordering': ['id']},
        ),
        migrations.AlterUniqueTogether(
            name='zoterosource',
            unique_together=set(),
        ),
    ]