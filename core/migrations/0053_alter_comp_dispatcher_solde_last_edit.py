# Generated by Django 3.2 on 2021-05-22 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_flight_assist_capacite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp_dispatcher',
            name='solde_last_edit',
            field=models.DateTimeField(auto_now=True, db_column='SOLDE_LAST_EDIT', null=True),
        ),
    ]
