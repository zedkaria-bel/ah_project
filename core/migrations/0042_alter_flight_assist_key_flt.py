# Generated by Django 3.2 on 2021-05-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_flight_assist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_assist',
            name='key_flt',
            field=models.TextField(db_column='KEY_FLT', primary_key=True, serialize=False),
        ),
    ]
