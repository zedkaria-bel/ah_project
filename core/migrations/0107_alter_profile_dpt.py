# Generated by Django 3.2 on 2021-06-28 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_alter_profile_poste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dpt',
            field=models.TextField(blank=True, choices=[(1, 'DPT CONTRATS ET ASSISTANCE AU SOL'), (2, 'CONTRÔLE DU FONCTIONNEMENT DES ESCALES'), (3, 'DPT LOGISTIQUE DES ESCALES'), (4, 'DPT RECHERCHES ET INDEMNISATION DES BAGAGES')], db_column='DPT', null=True),
        ),
    ]
