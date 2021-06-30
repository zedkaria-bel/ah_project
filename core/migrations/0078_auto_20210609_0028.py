# Generated by Django 3.2 on 2021-06-09 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_auto_20210608_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight_assist',
            name='acu',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='asu',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='camion_elev',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='dcs',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='gpu',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='guichet_nbr',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='heure_guichet',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='pist_autre_serv_1',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='pist_autre_serv_2',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='pist_autre_serv_3',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='piste_autre_serv_1_nb',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='piste_autre_serv_2_nb',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='piste_autre_serv_3_nb',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='platforme',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='psg_autre_serv_1',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='psg_autre_serv_1_nb',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='psg_autre_serv_2',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='psg_autre_serv_2_nb',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='push_back',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='toilet_service',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='um',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='water_service',
        ),
        migrations.RemoveField(
            model_name='flight_assist',
            name='wch',
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ACC_SALON',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ACU',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='AGENT_COORD',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='AGENT_OP_QUALIF',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='AGENT_SERV_PASSAGE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='AGENT_SERV_PISTE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ARRANGEMENT_CAB',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ASSIST_TRANSIT',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ASSIST_UM',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ASSIST_VIP',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ASSIST_WCH',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ASU',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='CAMION_ELEV',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='CHARIOT_BAG',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='CIVIERE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='COMM_SOL_COCKPIT',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='CONTAINER_PALETTE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='DB_MANIP_ULD',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='DEPORTEE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='DOSS_VOL_IMP',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ELEV_FOURCHE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='GPU',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='HUM',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='ID_BAG',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='NET_CABINE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='OUV_DOSS_BAG',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='PASSERELLE_PSG',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='PLATEFORME',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='PLEIN_WATER',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='PORTE_CONTAINER_PALETTE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='PUSH_BACK',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='RECONC_BAG_BRS',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='TAPIS_BAG',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='TOWING',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='TRACT_CHARIOT',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='USE_DCS',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='VEHICULE_TRANSP_PISTE',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='VIDE_TOILET',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='VIP_BUS',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='flight_assist',
            name='fiche_phys_received',
            field=models.BooleanField(db_column='FICHE PHYS RECUS', default=False, null=True),
        ),
        migrations.AlterField(
            model_name='flight_assist',
            name='obs',
            field=models.TextField(blank=True, db_column='OBS', null=True),
        ),
    ]