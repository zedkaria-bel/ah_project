# Generated by Django 3.2 on 2021-06-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_flight_assist_fiche_received'),
    ]

    operations = [
        migrations.CreateModel(
            name='TARIF_OCCAS',
            fields=[
                ('auto_id', models.AutoField(primary_key=True, serialize=False)),
                ('MTOW_10_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_10_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_10_30_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_10_30_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_30_50_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_30_50_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_50_80_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_50_80_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_80_150_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_80_150_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_150_250_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_150_250_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_250_COM', models.FloatField(blank=True, default=None, null=True)),
                ('MTOW_250_TECH', models.FloatField(blank=True, default=None, null=True)),
                ('ASSIST_WCH', models.FloatField(blank=True, default=None, null=True)),
                ('ASSIST_UM', models.FloatField(blank=True, default=None, null=True)),
                ('ASSIST_TRANSIT', models.FloatField(blank=True, default=None, null=True)),
                ('ACC_SALON', models.FloatField(blank=True, default=None, null=True)),
                ('ASSIST_VIP', models.FloatField(blank=True, default=None, null=True)),
                ('USE_DCS', models.FloatField(blank=True, default=None, null=True)),
                ('DEPORTEE', models.FloatField(blank=True, default=None, null=True)),
                ('AGENT_SERV_PASSAGE', models.FloatField(blank=True, default=None, null=True)),
                ('CIVIERE', models.FloatField(blank=True, default=None, null=True)),
                ('HUM', models.FloatField(blank=True, default=None, null=True)),
                ('OUV_DOSS_BAG', models.FloatField(blank=True, default=None, null=True)),
                ('DOSS_VOL_IMP', models.FloatField(blank=True, default=None, null=True)),
                ('AGENT_COORD', models.FloatField(blank=True, default=None, null=True)),
                ('COMM_SOL_COCKPIT', models.FloatField(blank=True, default=None, null=True)),
                ('AGENT_OP_QUALIF', models.FloatField(blank=True, default=None, null=True)),
                ('GPU', models.FloatField(blank=True, default=None, null=True)),
                ('ASU_MOY_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('ASU_BIG_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('ACU', models.FloatField(blank=True, default=None, null=True)),
                ('VIDE_TOILET_MOY_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('VIDE_TOILET_BIG_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('PLEIN_WATER_MOY_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('PLEIN_WATER_BIG_PORT', models.FloatField(blank=True, default=None, null=True)),
                ('NET_CABINE_100', models.FloatField(blank=True, default=None, null=True)),
                ('NET_CABINE_200', models.FloatField(blank=True, default=None, null=True)),
                ('NET_CABINE_300', models.FloatField(blank=True, default=None, null=True)),
                ('ARRANGEMENT_CAB_100', models.FloatField(blank=True, default=None, null=True)),
                ('ARRANGEMENT_CAB_200', models.FloatField(blank=True, default=None, null=True)),
                ('ARRANGEMENT_CAB_300', models.FloatField(blank=True, default=None, null=True)),
                ('RECONC_BAG_BRS', models.FloatField(blank=True, default=None, null=True)),
                ('ID_BAG_100', models.FloatField(blank=True, default=None, null=True)),
                ('ID_BAG_200', models.FloatField(blank=True, default=None, null=True)),
                ('PASSERELLE_PSG', models.FloatField(blank=True, default=None, null=True)),
                ('CAMION_ELEV', models.FloatField(blank=True, default=None, null=True)),
                ('VIP_BUS', models.FloatField(blank=True, default=None, null=True)),
                ('VEHICULE_TRANSP_PISTE', models.FloatField(blank=True, default=None, null=True)),
                ('PUSH_BACK', models.FloatField(blank=True, default=None, null=True)),
                ('TOWING', models.FloatField(blank=True, default=None, null=True)),
                ('CHARIOT_BAG', models.FloatField(blank=True, default=None, null=True)),
                ('TRACT_CHARIOT', models.FloatField(blank=True, default=None, null=True)),
                ('TAPIS_BAG', models.FloatField(blank=True, default=None, null=True)),
                ('PLATEFORME', models.FloatField(blank=True, default=None, null=True)),
                ('PORTE_CONTAINER_PALETTE', models.FloatField(blank=True, default=None, null=True)),
                ('CONTAINER_PALETTE', models.FloatField(blank=True, default=None, null=True)),
                ('ELEV_FOURCHE', models.FloatField(blank=True, default=None, null=True)),
                ('AGENT_SERV_PISTE', models.FloatField(blank=True, default=None, null=True)),
                ('DB_MANIP_ULD', models.FloatField(blank=True, default=None, null=True)),
                ('assist_night', models.PositiveIntegerField(blank=True, db_column='ASSIST NIGHT', default=None, null=True)),
                ('assist_weekend', models.PositiveIntegerField(blank=True, db_column='ASSIST WEEKEND', default=None, null=True)),
                ('assist_jourferie', models.PositiveIntegerField(blank=True, db_column='ASSIST JOUR FERIE', default=None, null=True)),
                ('standby', models.PositiveIntegerField(blank=True, db_column='STAND BY', default=None, null=True)),
                ('abs_demande', models.PositiveIntegerField(blank=True, db_column='ABSENCE DEMANDE', default=None, null=True)),
                ('rtr_1_3', models.PositiveIntegerField(blank=True, db_column='1 < RETARD <= 3', default=None, null=True)),
                ('rtr_3_5', models.PositiveIntegerField(blank=True, db_column='3 < RETARD <= 5', default=None, null=True)),
                ('rtr_5', models.PositiveIntegerField(blank=True, db_column='RETARD > 5', default=None, null=True)),
                ('cnl_12_24', models.PositiveIntegerField(blank=True, db_column='12 < CNL <= 24', default=None, null=True)),
                ('cnl_12', models.PositiveIntegerField(blank=True, db_column='CNL <= 12', default=None, null=True)),
                ('reduction', models.PositiveIntegerField(blank=True, db_column='REDUCTION', default=None, null=True)),
            ],
            options={
                'db_table': 'TARIF_OCCAS',
            },
        ),
    ]
