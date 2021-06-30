# Generated by Django 3.2 on 2021-05-03 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210503_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='CHG_FI',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('key_flt', models.TextField(db_column='KEY_FLT')),
                ('status_x', models.TextField(blank=True, db_column='STATUS_x', null=True)),
                ('ch_type_app', models.DateTimeField(blank=True, null=True)),
                ('ch_std', models.DateTimeField(blank=True, null=True)),
                ('ch_dest', models.DateTimeField(blank=True, null=True)),
                ('ch_config', models.DateTimeField(blank=True, null=True)),
                ('std_x', models.TextField(blank=True, db_column='STD_x', null=True)),
                ('std_y', models.TextField(blank=True, db_column='STD_y', null=True)),
                ('ac_x', models.TextField(blank=True, db_column='AC_x', null=True)),
                ('ac_y', models.TextField(blank=True, db_column='AC_y', null=True)),
                ('arr_x', models.TextField(blank=True, db_column='ARR_x', null=True)),
                ('arr_y', models.TextField(blank=True, db_column='ARR_y', null=True)),
                ('ac_config1_x', models.TextField(blank=True, db_column='AC CONFIG1_x', null=True)),
                ('ac_config1_y', models.TextField(blank=True, db_column='AC CONFIG1_y', null=True)),
                ('ac_config2_x', models.TextField(blank=True, db_column='AC CONFIG2_x', null=True)),
                ('ac_config2_y', models.TextField(blank=True, db_column='AC CONFIG2_y', null=True)),
                ('ac_config3_x', models.TextField(blank=True, db_column='AC CONFIG3_x', null=True)),
                ('ac_config3_y', models.TextField(blank=True, db_column='AC CONFIG3_y', null=True)),
                ('ac_config4_x', models.TextField(blank=True, db_column='AC CONFIG4_x', null=True)),
                ('ac_config4_y', models.TextField(blank=True, db_column='AC CONFIG4_y', null=True)),
            ],
            options={
                'db_table': 'CHG_FI',
                'unique_together': {('id', 'key_flt')},
            },
        ),
        migrations.CreateModel(
            name='CHG_SSIM',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('key_flt', models.TextField(db_column='KEY_FLT')),
                ('ch_type_app', models.TextField(blank=True, null=True)),
                ('ch_std', models.TextField(blank=True, null=True)),
                ('ch_dest', models.TextField(blank=True, null=True)),
                ('ch_config', models.TextField(blank=True, null=True)),
                ('aircraft_type_x', models.TextField(blank=True, db_column='Aircraft_Type_x', null=True)),
                ('aircraft_type_y', models.TextField(blank=True, db_column='Aircraft_Type_y', null=True)),
                ('std_utc_x', models.TextField(blank=True, db_column='STD_UTC_x', null=True)),
                ('std_utc_y', models.TextField(blank=True, db_column='STD_UTC_y', null=True)),
                ('arrival_station_x', models.TextField(blank=True, db_column='Arrival_Station_x', null=True)),
                ('arrival_station_y', models.TextField(blank=True, db_column='Arrival_Station_y', null=True)),
                ('aircraft_configuration_x', models.TextField(blank=True, db_column='Aircraft_Configuration_x', null=True)),
                ('aircraft_configuration_y', models.TextField(blank=True, db_column='Aircraft_Configuration_y', null=True)),
            ],
            options={
                'db_table': 'CHG_SSIM',
                'unique_together': {('id', 'key_flt')},
            },
        ),
        migrations.CreateModel(
            name='COMP_DISPATCHER',
            fields=[
                ('company_dispatcher', models.TextField(db_column='COMPANY DISPATCHER', primary_key=True, serialize=False)),
                ('solde', models.FloatField(blank=True, db_column='SOLDE', null=True)),
                ('solde_estimee', models.FloatField(blank=True, db_column='SOLDE ESTIMEE', null=True)),
                ('solde_last_edit', models.DateTimeField(blank=True, db_column='SOLDE_LAST_EDIT', null=True)),
            ],
            options={
                'db_table': 'COMP_DISPATCHER',
            },
        ),
        migrations.CreateModel(
            name='FLIGHT_FI',
            fields=[
                ('key_flt', models.TextField(db_column='KEY_FLT', primary_key=True, serialize=False)),
                ('status', models.TextField(blank=True, db_column='STATUS', null=True)),
                ('occas', models.TextField(blank=True, db_column='OCCAS', null=True)),
                ('escale_iata_field', models.TextField(blank=True, db_column='ESCALE (IATA)', null=True)),
                ('date', models.TextField(blank=True, db_column='DATE', null=True)),
                ('route_ac', models.TextField(blank=True, db_column='ROUTE_AC', null=True)),
                ('flt', models.TextField(blank=True, db_column='FLT', null=True)),
                ('type', models.TextField(blank=True, db_column='TYPE', null=True)),
                ('reg', models.TextField(blank=True, db_column='REG', null=True)),
                ('fc', models.TextField(blank=True, db_column='FC', null=True)),
                ('ac', models.TextField(blank=True, db_column='AC', null=True)),
                ('chr', models.TextField(blank=True, db_column='CHR', null=True)),
                ('dep', models.TextField(blank=True, db_column='DEP', null=True)),
                ('arr', models.TextField(blank=True, db_column='ARR', null=True)),
                ('std', models.TextField(blank=True, db_column='STD', null=True)),
                ('sta', models.TextField(blank=True, db_column='STA', null=True)),
                ('etd', models.TextField(blank=True, db_column='ETD', null=True)),
                ('eta', models.TextField(blank=True, db_column='ETA', null=True)),
                ('tkof', models.TextField(blank=True, db_column='TKof', null=True)),
                ('tdwn', models.TextField(blank=True, db_column='TDwn', null=True)),
                ('st', models.TextField(blank=True, db_column='ST', null=True)),
                ('atd', models.TextField(blank=True, db_column='ATD', null=True)),
                ('ata', models.TextField(blank=True, db_column='ATA', null=True)),
                ('block', models.TextField(blank=True, db_column='BLOCK', null=True)),
                ('flthr', models.TextField(blank=True, db_column='FLThr', null=True)),
                ('c1', models.TextField(blank=True, db_column='C1', null=True)),
                ('dly1', models.TextField(blank=True, db_column='DLY1', null=True)),
                ('sub1', models.TextField(blank=True, db_column='Sub1', null=True)),
                ('c2', models.TextField(blank=True, db_column='C2', null=True)),
                ('dly2', models.TextField(blank=True, db_column='DLY2', null=True)),
                ('sub2', models.TextField(blank=True, db_column='Sub2', null=True)),
                ('c3', models.TextField(blank=True, db_column='C3', null=True)),
                ('dly3', models.TextField(blank=True, db_column='DLY3', null=True)),
                ('sub3', models.TextField(blank=True, db_column='Sub3', null=True)),
                ('c4', models.TextField(blank=True, db_column='C4', null=True)),
                ('dly4', models.TextField(blank=True, db_column='DLY4', null=True)),
                ('sub4', models.TextField(blank=True, db_column='Sub4', null=True)),
                ('c5', models.TextField(blank=True, db_column='C5', null=True)),
                ('dly5', models.TextField(blank=True, db_column='DLY5', null=True)),
                ('sub5', models.TextField(blank=True, db_column='Sub5', null=True)),
                ('c6', models.TextField(blank=True, db_column='C6', null=True)),
                ('dly6', models.TextField(blank=True, db_column='DLY6', null=True)),
                ('sub6', models.TextField(blank=True, db_column='Sub6', null=True)),
                ('c7', models.TextField(blank=True, db_column='C7', null=True)),
                ('dly7', models.TextField(blank=True, db_column='DLY7', null=True)),
                ('sub7', models.TextField(blank=True, db_column='Sub7', null=True)),
                ('c8', models.TextField(blank=True, db_column='C8', null=True)),
                ('dly8', models.TextField(blank=True, db_column='DLY8', null=True)),
                ('sub8', models.TextField(blank=True, db_column='Sub8', null=True)),
                ('c1a', models.TextField(blank=True, db_column='C1A', null=True)),
                ('dly1a', models.TextField(blank=True, db_column='DLY1A', null=True)),
                ('sub9', models.TextField(blank=True, db_column='Sub9', null=True)),
                ('c2a', models.TextField(blank=True, db_column='C2A', null=True)),
                ('dly2a', models.TextField(blank=True, db_column='DLY2A', null=True)),
                ('sb10', models.TextField(blank=True, db_column='Sb10', null=True)),
                ('cargo', models.TextField(blank=True, db_column='Cargo', null=True)),
                ('mail', models.TextField(blank=True, db_column='Mail', null=True)),
                ('payld', models.TextField(blank=True, db_column='Payld', null=True)),
                ('bags', models.TextField(blank=True, db_column='Bags', null=True)),
                ('exp_pax_f', models.TextField(blank=True, db_column='EXP PAX F', null=True)),
                ('exp_pax_c', models.TextField(blank=True, db_column='EXP PAX C', null=True)),
                ('exp_pax_y', models.TextField(blank=True, db_column='EXP PAX Y', null=True)),
                ('exp_pax_inf', models.TextField(blank=True, db_column='EXP PAX INF', null=True)),
                ('act_pax_f', models.TextField(blank=True, db_column='ACT PAX F', null=True)),
                ('act_pax_c', models.TextField(blank=True, db_column='ACT PAX C', null=True)),
                ('act_pax_y', models.TextField(blank=True, db_column='ACT PAX Y', null=True)),
                ('act_pax_inf', models.TextField(blank=True, db_column='ACT PAX INF', null=True)),
                ('exp_ttl', models.TextField(blank=True, db_column='EXP TTL', null=True)),
                ('pax_ttl', models.TextField(blank=True, db_column='PAX TTL', null=True)),
                ('seats_ttl', models.TextField(blank=True, db_column='SEATS TTL', null=True)),
                ('lf_field', models.TextField(blank=True, db_column='LF %', null=True)),
                ('ac_config1', models.TextField(blank=True, db_column='AC CONFIG1', null=True)),
                ('ac_config2', models.TextField(blank=True, db_column='AC CONFIG2', null=True)),
                ('ac_config3', models.TextField(blank=True, db_column='AC CONFIG3', null=True)),
                ('ac_config4', models.TextField(blank=True, db_column='AC CONFIG4', null=True)),
                ('log_page_field', models.TextField(blank=True, db_column='Log_Page#', null=True)),
                ('character_seats_f', models.TextField(blank=True, db_column='Character Seats F', null=True)),
                ('character_seats_c', models.TextField(blank=True, db_column='Character Seats C', null=True)),
                ('character_seats_y', models.TextField(blank=True, db_column='Character Seats Y', null=True)),
                ('character_seats_inf', models.TextField(blank=True, db_column='Character Seats INF', null=True)),
                ('code_share_and_seats_f', models.TextField(blank=True, db_column='Code Share and Seats F', null=True)),
                ('code_share_and_seats_c', models.TextField(blank=True, db_column='Code Share and Seats C', null=True)),
                ('code_share_and_seats_y', models.TextField(blank=True, db_column='Code Share and Seats Y', null=True)),
                ('code_share_and_seats_inf', models.TextField(blank=True, db_column='Code Share and Seats INF', null=True)),
                ('dist', models.TextField(blank=True, db_column='Dist', null=True)),
                ('dstand', models.TextField(blank=True, db_column='DStand', null=True)),
                ('astand', models.TextField(blank=True, db_column='AStand', null=True)),
                ('change_reason', models.TextField(blank=True, db_column='Change reason', null=True)),
                ('init', models.TextField(blank=True, db_column='Init', null=True)),
                ('uplf_w', models.TextField(blank=True, db_column='Uplf W', null=True)),
                ('ramp', models.TextField(blank=True, db_column='Ramp', null=True)),
                ('stdn', models.TextField(blank=True, db_column='Stdn', null=True)),
                ('burn', models.TextField(blank=True, db_column='Burn', null=True)),
                ('uplf_v', models.TextField(blank=True, db_column='Uplf V', null=True)),
                ('usg_lts', models.TextField(blank=True, db_column='USG/LTS', null=True)),
                ('tank', models.TextField(blank=True, db_column='Tank', null=True)),
                ('zfw', models.TextField(blank=True, db_column='ZFW', null=True)),
                ('fpburn', models.TextField(blank=True, db_column='FPBurn', null=True)),
                ('sgrav', models.TextField(blank=True, db_column='SGrav', null=True)),
                ('miles', models.TextField(blank=True, db_column='Miles', null=True)),
                ('rt_base', models.TextField(blank=True, db_column='Rt base', null=True)),
                ('dgate', models.TextField(blank=True, db_column='DGate', null=True)),
                ('agate', models.TextField(blank=True, db_column='AGate', null=True)),
                ('orig_arr_station', models.TextField(blank=True, db_column='Orig.ARR Station', null=True)),
                ('d_closed', models.TextField(blank=True, db_column='D.Closed', null=True)),
                ('ch_type_app', models.TextField(blank=True, null=True)),
                ('ch_std', models.TextField(blank=True, null=True)),
                ('ch_dest', models.TextField(blank=True, null=True)),
                ('ch_config', models.TextField(blank=True, null=True)),
                ('fi_file', models.DateTimeField(blank=True, db_column='FI_FILE', null=True)),
            ],
            options={
                'db_table': 'FLIGHT_FI',
            },
        ),
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
        migrations.CreateModel(
            name='FLIGHT_SSIM',
            fields=[
                ('key_flt', models.TextField(db_column='KEY_FLT', primary_key=True, serialize=False)),
                ('status', models.TextField(blank=True, db_column='STATUS', null=True)),
                ('ssim_period', models.TextField(blank=True, null=True)),
                ('index_commercial', models.TextField(blank=True, null=True)),
                ('st_ssim', models.TextField(blank=True, db_column='ST_SSIM', null=True)),
                ('airline', models.TextField(blank=True, db_column='Airline', null=True)),
                ('flight_number', models.TextField(blank=True, db_column='Flight_Number', null=True)),
                ('itinirary_variation_indicator', models.TextField(blank=True, db_column='Itinirary_Variation_Indicator', null=True)),
                ('leg_sequence_number', models.TextField(blank=True, db_column='Leg_Sequence_Number', null=True)),
                ('service_type', models.TextField(blank=True, db_column='Service_Type', null=True)),
                ('start_period', models.TextField(blank=True, db_column='Start_period', null=True)),
                ('end_period', models.TextField(blank=True, db_column='End_period', null=True)),
                ('monday', models.TextField(blank=True, db_column='Monday', null=True)),
                ('tuesday', models.TextField(blank=True, db_column='Tuesday', null=True)),
                ('wednesday', models.TextField(blank=True, db_column='Wednesday', null=True)),
                ('thursday', models.TextField(blank=True, db_column='Thursday', null=True)),
                ('friday', models.TextField(blank=True, db_column='Friday', null=True)),
                ('saturday', models.TextField(blank=True, db_column='Saturday', null=True)),
                ('sunday', models.TextField(blank=True, db_column='Sunday', null=True)),
                ('departure_station', models.TextField(blank=True, db_column='Departure_Station', null=True)),
                ('pax_std_utc', models.TextField(blank=True, db_column='PAX_STD_UTC', null=True)),
                ('std_utc', models.TextField(blank=True, db_column='STD_UTC', null=True)),
                ('std_variation_sign', models.TextField(blank=True, db_column='STD_Variation_Sign', null=True)),
                ('std_variation_utc', models.TextField(blank=True, db_column='STD_Variation_UTC', null=True)),
                ('arrival_station', models.TextField(blank=True, db_column='Arrival_Station', null=True)),
                ('sta_utc', models.TextField(blank=True, db_column='STA_UTC', null=True)),
                ('pax_sta_utc', models.TextField(blank=True, db_column='PAX_STA_UTC', null=True)),
                ('sta_variation_sign', models.TextField(blank=True, db_column='STA_Variation_Sign', null=True)),
                ('sta_variation_utc', models.TextField(blank=True, db_column='STA_Variation_UTC', null=True)),
                ('aircraft_type', models.TextField(blank=True, db_column='Aircraft_Type', null=True)),
                ('fly_next_number', models.TextField(blank=True, null=True)),
                ('aircraft_configuration', models.TextField(blank=True, db_column='Aircraft_Configuration', null=True)),
                ('fly_date', models.DateField(blank=True, null=True)),
                ('arrival_date', models.DateField(blank=True, null=True)),
                ('vol_commercial_number', models.TextField(blank=True, null=True)),
                ('vol_commercial_airline', models.TextField(blank=True, null=True)),
                ('code_ssim', models.TextField(blank=True, null=True)),
                ('day_op', models.FloatField(blank=True, null=True)),
                ('ch_type_app', models.TextField(blank=True, null=True)),
                ('ch_std', models.TextField(blank=True, null=True)),
                ('ch_dest', models.TextField(blank=True, null=True)),
                ('ch_config', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FLIGHT_SSIM',
            },
        ),
        migrations.DeleteModel(
            name='ChgFi',
        ),
        migrations.DeleteModel(
            name='ChgSsim',
        ),
        migrations.DeleteModel(
            name='CompDispatcher',
        ),
        migrations.DeleteModel(
            name='FlightFi',
        ),
        migrations.DeleteModel(
            name='FlightOccas',
        ),
        migrations.DeleteModel(
            name='FlightSsim',
        ),
    ]
