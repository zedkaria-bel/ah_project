# Generated by Django 3.2 on 2021-06-29 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0110_auto_20210629_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historique_regular_fact',
            name='_id',
        ),
    ]
