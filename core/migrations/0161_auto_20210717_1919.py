# Generated by Django 3.2 on 2021-07-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0160_bag_suivi_id_geo_deliv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bag_suivi',
            name='rib_key',
            field=models.TextField(blank=True, db_column='RIB KEY', null=True),
        ),
        migrations.AlterField(
            model_name='bag_suivi',
            name='rib_n',
            field=models.TextField(blank=True, db_column='RIB VALUE', null=True),
        ),
    ]