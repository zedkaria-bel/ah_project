# Generated by Django 3.2 on 2021-05-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210503_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='FLIGHT_OCCAS',
            fields=[
                ('key_flt', models.TextField(db_column='KEY_FLT', primary_key=True, serialize=False)),
                ('n_field', models.FloatField(blank=True, db_column='N°', null=True)),
                ('date_demande', models.DateTimeField(blank=True, db_column='DATE DEMANDE', null=True)),
                ('compagnie_dispatcher', models.TextField(blank=True, db_column='COMPAGNIE DISPATCHER', null=True)),
                ('reg', models.TextField(blank=True, db_column='REG', null=True)),
                ('mtow_tonnes_field', models.FloatField(blank=True, db_column='MTOW (Tonnes)', null=True)),
                ('nature_touchee', models.TextField(blank=True, db_column='NATURE TOUCHEE', null=True)),
                ('operateur', models.TextField(blank=True, db_column='OPERATEUR', null=True)),
                ('n_vol_arr', models.TextField(blank=True, db_column='N VOL ARR', null=True)),
                ('date_arrivee', models.DateTimeField(blank=True, db_column='DATE ARRIVEE', null=True)),
                ('heure_arr', models.TimeField(blank=True, db_column='HEURE ARR', null=True)),
                ('prov', models.TextField(blank=True, db_column='PROV', null=True)),
                ('escale_iata_field', models.TextField(blank=True, db_column='ESCALE (IATA)', null=True)),
                ('n_vol_dep', models.TextField(blank=True, db_column='N VOL DEP', null=True)),
                ('date_depart', models.DateTimeField(blank=True, db_column='DATE DEPART', null=True)),
                ('heure_dep', models.TimeField(blank=True, db_column='HEURE DEP', null=True)),
                ('dest', models.TextField(blank=True, db_column='DEST', null=True)),
                ('montant_prevus', models.FloatField(blank=True, db_column='MONTANT PREVUS', null=True)),
                ('mode_de_payement', models.TextField(blank=True, db_column='MODE DE PAYEMENT', null=True)),
                ('monnaie', models.TextField(blank=True, db_column='MONNAIE', null=True)),
                ('etat_du_vol', models.TextField(blank=True, db_column='ETAT DU VOL', null=True)),
                ('date_cnl', models.DateTimeField(blank=True, db_column='DATE CNL', null=True)),
                ('heure_cnl', models.TimeField(blank=True, db_column='HEURE CNL', null=True)),
                ('cnl_eta', models.TimeField(blank=True, db_column='CNL / ETA', null=True)),
                ('obs', models.FloatField(blank=True, db_column='OBS', null=True)),
                ('ata', models.FloatField(blank=True, db_column='ATA', null=True)),
                ('atd', models.FloatField(blank=True, db_column='ATD', null=True)),
                ('nbr_pax', models.FloatField(blank=True, db_column='NBR PAX', null=True)),
                ('cgo_kg_field', models.FloatField(blank=True, db_column='CGO (KG)', null=True)),
                ('n_fiche_touchee', models.FloatField(blank=True, db_column='N° FICHE TOUCHEE', null=True)),
                ('montant_facture', models.FloatField(blank=True, db_column='MONTANT FACTURE', null=True)),
                ('unnamed_31', models.FloatField(blank=True, db_column='Unnamed: 31', null=True)),
                ('n_facture', models.FloatField(blank=True, db_column='N° FACTURE', null=True)),
            ],
            options={
                'db_table': 'FLIGHT_OCCAS',
            },
        ),
        migrations.RenameField(
            model_name='comp_dispatcher',
            old_name='comp_dispatcher',
            new_name='company_dispatcher',
        ),
        migrations.RemoveField(
            model_name='comp_dispatcher',
            name='date_last_update',
        ),
        migrations.RemoveField(
            model_name='comp_dispatcher',
            name='estimated_solde',
        ),
        migrations.RemoveField(
            model_name='flight_fi',
            name='escale',
        ),
        migrations.AddField(
            model_name='chg_fi',
            name='status_x',
            field=models.TextField(blank=True, db_column='STATUS_x', null=True),
        ),
        migrations.AddField(
            model_name='comp_dispatcher',
            name='solde_estimee',
            field=models.FloatField(blank=True, db_column='SOLDE ESTIMEE', null=True),
        ),
        migrations.AddField(
            model_name='comp_dispatcher',
            name='solde_last_edit',
            field=models.DateTimeField(blank=True, db_column='SOLDE_LAST_EDIT', null=True),
        ),
        migrations.AddField(
            model_name='flight_fi',
            name='escale_iata_field',
            field=models.TextField(blank=True, db_column='ESCALE (IATA)', null=True),
        ),
        migrations.AlterField(
            model_name='comp_dispatcher',
            name='solde',
            field=models.FloatField(blank=True, db_column='SOLDE', null=True),
        ),
        migrations.AlterField(
            model_name='flight_fi',
            name='occas',
            field=models.TextField(blank=True, db_column='OCCAS', null=True),
        ),
    ]
