# Generated by Django 3.2 on 2021-05-28 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_flight_assist_retard'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight_assist',
            name='annulation',
            field=models.FloatField(blank=True, db_column='ANNULATION', default='0', null=True),
        ),
    ]
