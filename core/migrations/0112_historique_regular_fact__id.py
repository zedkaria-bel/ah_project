# Generated by Django 3.2 on 2021-06-29 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_remove_historique_regular_fact__id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historique_regular_fact',
            name='_id',
            field=models.PositiveIntegerField(blank=True, db_column='ID', null=True),
        ),
    ]
