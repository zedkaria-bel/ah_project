# Generated by Django 3.2 on 2021-06-29 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0113_auto_20210629_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historique_regular_fact',
            name='date_last_add',
        ),
    ]
