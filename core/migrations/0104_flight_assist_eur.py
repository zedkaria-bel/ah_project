# Generated by Django 3.2 on 2021-06-26 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0103_historique_regular_fact_escale'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight_assist',
            name='eur',
            field=models.FloatField(blank=True, db_column='EUR', null=True),
        ),
    ]