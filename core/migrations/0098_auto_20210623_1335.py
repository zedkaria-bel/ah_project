# Generated by Django 3.2 on 2021-06-23 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_flight_assist_heure_demande'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight_assist',
            name='major_abs_demande',
            field=models.FloatField(blank=True, db_column='MAJORATION ABSENCE DEMANDE', null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='major_jourferie',
            field=models.FloatField(blank=True, db_column='MAJORATION JOUR FERIE', null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='major_night',
            field=models.FloatField(blank=True, db_column='MAJORATION NUIT', null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='major_standby',
            field=models.FloatField(blank=True, db_column='MAJORATION STANDBY', null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='major_weekend',
            field=models.FloatField(blank=True, db_column='MAJORATION WEEKEND', null=True),
        ),
    ]
