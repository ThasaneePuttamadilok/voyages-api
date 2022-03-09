# Generated by Django 3.2.6 on 2022-02-01 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0003_auto_20220131_2155'),
        ('past', '0008_auto_20220201_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enslaveridentitysourceconnection',
            name='identity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enslaver_identity', to='past.enslaveridentity'),
        ),
        migrations.AlterField(
            model_name='enslaveridentitysourceconnection',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enslaver_source', to='voyage.voyagesources'),
        ),
    ]
