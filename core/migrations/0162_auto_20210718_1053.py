# Generated by Django 3.2 on 2021-07-18 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0161_auto_20210717_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='comp_dispatcher',
            name='dte_begin',
            field=models.DateTimeField(auto_now_add=True, db_column='DATE BEGIN', null=True),
        ),
        migrations.AddField(
            model_name='comp_dispatcher',
            name='dte_end',
            field=models.DateField(blank=True, db_column='DATE END', null=True),
        ),
        migrations.AddField(
            model_name='tarif_occas',
            name='dte_begin',
            field=models.DateTimeField(auto_now_add=True, db_column='DATE BEGIN', null=True),
        ),
        migrations.AddField(
            model_name='tarif_occas',
            name='dte_end',
            field=models.DateField(blank=True, db_column='DATE END', null=True),
        ),
    ]
