# Generated by Django 3.2 on 2021-06-09 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_fiche_touchee_escale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='escales',
            name='fiche_from',
        ),
        migrations.RemoveField(
            model_name='escales',
            name='fiche_to',
        ),
        migrations.AddField(
            model_name='escales',
            name='nb_fiche_total',
            field=models.PositiveIntegerField(blank=True, db_column='NB FICHE TOTALES', default=0, null=True),
        ),
    ]