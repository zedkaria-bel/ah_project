# Generated by Django 3.2 on 2021-05-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210501_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMP_DISPATCHER',
            fields=[
                ('comp_dispatcher', models.TextField(db_column='COMPANY DISPATCHER', primary_key=True, serialize=False)),
                ('solde', models.FloatField(blank=True, null=True)),
                ('estimated_solde', models.FloatField(blank=True, null=True)),
                ('date_last_update', models.DateField(auto_now=True, null=True)),
            ],
        ),
    ]
