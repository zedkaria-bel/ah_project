# Generated by Django 3.2 on 2021-05-15 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_flight_assist_key_flt'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight_assist',
            name='n_facture',
            field=models.FloatField(blank=True, db_column='N° FACTURE', null=True),
        ),
    ]