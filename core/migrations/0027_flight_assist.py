# Generated by Django 3.2 on 2021-05-07 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210504_0220'),
    ]

    operations = [
        migrations.CreateModel(
            name='FLIGHT_ASSIST',
            fields=[
                ('key_flt', models.IntegerField(db_column='KEY_FLT', primary_key=True, serialize=False)),
                ('status', models.TextField(blank=True, db_column='STATUS', null=True)),
                ('monnaie', models.TextField(blank=True, db_column='MONNAIE', null=True)),
                ('escale', models.TextField(blank=True, db_column='ESCALE', null=True)),
                ('act_dte_arr', models.DateTimeField(blank=True, db_column='ACT DTE ARR', null=True)),
                ('prov', models.TextField(blank=True, db_column='PROV', null=True)),
                ('n_vol_arriv', models.TextField(blank=True, db_column='N° VOL ARRIV', null=True)),
                ('sta', models.TextField(blank=True, db_column='STA', null=True)),
                ('ata', models.TextField(blank=True, db_column='ATA', null=True)),
                ('pax_arriv', models.TextField(blank=True, db_column='PAX ARRIV', null=True)),
                ('cargo_arriv', models.TextField(blank=True, db_column='CARGO ARRIV', null=True)),
                ('act_dte_dep', models.TextField(blank=True, db_column='ACT DTE DEP', null=True)),
                ('dest', models.TextField(blank=True, db_column='DEST', null=True)),
                ('n_vol_dep', models.TextField(blank=True, db_column='N° VOL DEP', null=True)),
                ('std', models.TextField(blank=True, db_column='STD', null=True)),
                ('atd', models.TextField(blank=True, db_column='ATD', null=True)),
                ('pax_dep', models.TextField(blank=True, db_column='PAX     DEP', null=True)),
                ('cargo_dep', models.TextField(blank=True, db_column='CARGO DEP', null=True)),
                ('cie_a_facturer', models.TextField(blank=True, db_column='Cie A FACTURER', null=True)),
                ('n_fiche_touchee', models.TextField(blank=True, db_column='N° FICHE TOUCHEE', null=True)),
                ('nature_touchee', models.TextField(blank=True, db_column='NATURE TOUCHEE', null=True)),
                ('type_avion', models.TextField(blank=True, db_column='TYPE AVION', null=True)),
                ('mtow_tn_field', models.TextField(blank=True, db_column='MTOW (Tn)', null=True)),
                ('matricule_avion_field', models.TextField(blank=True, db_column='MATRICULE  AVION ', null=True)),
                ('parking', models.TextField(blank=True, db_column='PARKING', null=True)),
                ('mode_paiement', models.TextField(blank=True, db_column='MODE PAIEMENT', null=True)),
                ('um', models.FloatField(blank=True, db_column='UM', null=True)),
                ('wch', models.FloatField(blank=True, db_column='WCH', null=True)),
                ('medical_lift', models.FloatField(blank=True, db_column='MEDICAL LIFT', null=True)),
                ('gpu_mn_field', models.FloatField(blank=True, db_column='GPU (MN)', null=True)),
                ('asu', models.FloatField(blank=True, db_column='ASU', null=True)),
                ('acu', models.FloatField(blank=True, db_column='ACU', null=True)),
                ('toilet_service', models.FloatField(blank=True, db_column='TOILET SERVICE', null=True)),
                ('water_service', models.FloatField(blank=True, db_column='WATER SERVICE', null=True)),
                ('push_back_field', models.FloatField(blank=True, db_column='PUSH BACK ', null=True)),
                ('towing', models.FloatField(blank=True, db_column='TOWING', null=True)),
                ('chariot_bag', models.FloatField(blank=True, db_column='CHARIOT BAG', null=True)),
                ('step_auto', models.FloatField(blank=True, db_column='STEP AUTO', null=True)),
                ('step_tract', models.FloatField(blank=True, db_column='STEP TRACT', null=True)),
                ('tracteur', models.FloatField(blank=True, db_column='TRACTEUR', null=True)),
                ('net_cab', models.FloatField(blank=True, db_column='NET CAB', null=True)),
                ('headset', models.FloatField(blank=True, db_column='HEADSET', null=True)),
                ('navette_piste', models.FloatField(blank=True, db_column='NAVETTE PISTE', null=True)),
                ('manut_tnao', models.TextField(blank=True, db_column='MANUT/TNAO', null=True)),
                ('tapis_bag', models.FloatField(blank=True, db_column='TAPIS BAG', null=True)),
                ('hum', models.FloatField(blank=True, db_column='HUM', null=True)),
                ('f_c', models.FloatField(blank=True, db_column='F/C', null=True)),
                ('deportees', models.FloatField(blank=True, db_column='DEPORTEES', null=True)),
                ('tarif_de_base', models.FloatField(blank=True, db_column='TARIF DE BASE', null=True)),
                ('majoration', models.FloatField(blank=True, db_column='MAJORATION', null=True)),
                ('reduction', models.FloatField(blank=True, db_column='REDUCTION', null=True)),
                ('dcs', models.FloatField(blank=True, db_column='DCS', null=True)),
                ('extra_service', models.FloatField(blank=True, db_column='EXTRA SERVICE', null=True)),
                ('montant_globale', models.FloatField(blank=True, db_column='MONTANT GLOBALE', null=True)),
                ('dzd', models.FloatField(blank=True, db_column='DZD', null=True)),
            ],
            options={
                'db_table': 'FLIGHT_ASSIST',
            },
        ),
    ]