# Generated by Django 3.2 on 2021-05-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_flight_assist_n_facture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_assist',
            name='mtow_tonnes_field',
            field=models.FloatField(blank=True, db_column='MTOW (Tonnes)', null=True),
        ),
    ]
