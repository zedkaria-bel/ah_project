# Generated by Django 3.2 on 2021-06-14 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_historique_cnl_fiches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_assist',
            name='n_facture',
            field=models.TextField(blank=True, db_column='N° FACTURE', null=True),
        ),
    ]
