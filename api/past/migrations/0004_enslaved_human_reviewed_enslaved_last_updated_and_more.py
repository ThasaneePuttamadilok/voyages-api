# Generated by Django 4.2.1 on 2023-06-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('past', '0003_alter_moderncountry_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='enslaved',
            name='human_reviewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='enslaved',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='enslaveralias',
            name='human_reviewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='enslaveralias',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='enslaveridentity',
            name='human_reviewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='enslaveridentity',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]