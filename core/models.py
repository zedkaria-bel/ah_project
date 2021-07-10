# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.shortcuts import reverse
import datetime
from django.core.exceptions import ValidationError
from .CONST import monnaie, poste, service_passager, service_ramp_piste, causes, dpt, TYPE, status

def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")


class CHG_FI(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, primary_key = True)  # Field name made lowercase.
    key_flt = models.TextField(db_column='KEY_FLT')  # Field name made lowercase.
    status_x = models.TextField(db_column='STATUS_x', blank=True, null=True)  # Field name made lowercase.
    ch_type_app = models.DateTimeField(blank=True, null=True)
    ch_std = models.DateTimeField(blank=True, null=True)
    ch_dest = models.DateTimeField(blank=True, null=True)
    ch_config = models.DateTimeField(blank=True, null=True)
    std_x = models.TextField(db_column='STD_x', blank=True, null=True)  # Field name made lowercase.
    std_y = models.TextField(db_column='STD_y', blank=True, null=True)  # Field name made lowercase.
    ac_x = models.TextField(db_column='AC_x', blank=True, null=True)  # Field name made lowercase.
    ac_y = models.TextField(db_column='AC_y', blank=True, null=True)  # Field name made lowercase.
    arr_x = models.TextField(db_column='ARR_x', blank=True, null=True)  # Field name made lowercase.
    arr_y = models.TextField(db_column='ARR_y', blank=True, null=True)  # Field name made lowercase.
    ac_config1_x = models.TextField(db_column='AC CONFIG1_x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config1_y = models.TextField(db_column='AC CONFIG1_y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config2_x = models.TextField(db_column='AC CONFIG2_x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config2_y = models.TextField(db_column='AC CONFIG2_y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config3_x = models.TextField(db_column='AC CONFIG3_x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config3_y = models.TextField(db_column='AC CONFIG3_y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config4_x = models.TextField(db_column='AC CONFIG4_x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config4_y = models.TextField(db_column='AC CONFIG4_y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        db_table = 'CHG_FI'
        unique_together = (('id', 'key_flt'),)


class CHG_SSIM(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, primary_key = True)  # Field name made lowercase.
    key_flt = models.TextField(db_column='KEY_FLT')  # Field name made lowercase.
    status = models.TextField(db_column='STATUS_x', blank=True, null=True)
    ch_type_app = models.TextField(blank=True, null=True)
    ch_std = models.TextField(blank=True, null=True)
    ch_dest = models.TextField(blank=True, null=True)
    ch_config = models.TextField(blank=True, null=True)
    aircraft_type_x = models.TextField(db_column='Aircraft_Type_x', blank=True, null=True)  # Field name made lowercase.
    aircraft_type_y = models.TextField(db_column='Aircraft_Type_y', blank=True, null=True)  # Field name made lowercase.
    std_utc_x = models.TextField(db_column='STD_UTC_x', blank=True, null=True)  # Field name made lowercase.
    std_utc_y = models.TextField(db_column='STD_UTC_y', blank=True, null=True)  # Field name made lowercase.
    arrival_station_x = models.TextField(db_column='Arrival_Station_x', blank=True, null=True)  # Field name made lowercase.
    arrival_station_y = models.TextField(db_column='Arrival_Station_y', blank=True, null=True)  # Field name made lowercase.
    aircraft_configuration_x = models.TextField(db_column='Aircraft_Configuration_x', blank=True, null=True)  # Field name made lowercase.
    aircraft_configuration_y = models.TextField(db_column='Aircraft_Configuration_y', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'CHG_SSIM'
        unique_together = (('id', 'key_flt'),)


class EXCHANGE(models.Model):
    auto_id = models.AutoField(primary_key=True)
    usd = models.FloatField(db_column='USD', null=None)
    dzd = models.FloatField(db_column='DZD', null=None)
    eur = models.FloatField(db_column='EUR', null=None)
    status = models.TextField(db_column='STATUS', null=True)
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    date_last_edit = models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True, blank=True)

    class Meta:
        db_table = 'EXCHANGE'


class TARIF_OCCAS(models.Model):
    auto_id = models.AutoField(primary_key=True)
    MTOW_10_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_30_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_30_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_30_50_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_30_50_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_50_80_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_50_80_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_80_150_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_80_150_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_150_250_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_150_250_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_250_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_250_TECH = models.FloatField(blank=True, null=True, default=None)
    ASSIST_WCH = models.FloatField(blank=True, null=True, default=None)
    ASSIST_UM = models.FloatField(blank=True, null=True, default=None)
    ASSIST_TRANSIT = models.FloatField(blank=True, null=True, default=None)
    ACC_SALON = models.FloatField(blank=True, null=True, default=None)
    ASSIST_VIP = models.FloatField(blank=True, null=True, default=None)
    USE_DCS = models.FloatField(blank=True, null=True, default=None)
    DEPORTEE = models.FloatField(blank=True, null=True, default=None)
    AGENT_SERV_PASSAGE = models.FloatField(blank=True, null=True, default=None)
    CIVIERE = models.FloatField(blank=True, null=True, default=None)
    HUM = models.FloatField(blank=True, null=True, default=None)
    OUV_DOSS_BAG = models.FloatField(blank=True, null=True, default=None)
    DOSS_VOL_IMP = models.FloatField(blank=True, null=True, default=None)
    AGENT_COORD = models.FloatField(blank=True, null=True, default=None)
    COMM_SOL_COCKPIT = models.FloatField(blank=True, null=True, default=None)
    AGENT_OP_QUALIF = models.FloatField(blank=True, null=True, default=None)
    GPU = models.FloatField(blank=True, null=True, default=None)
    ASU_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    ASU_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    ACU = models.FloatField(blank=True, null=True, default=None)
    VIDE_TOILET_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    VIDE_TOILET_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    PLEIN_WATER_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    PLEIN_WATER_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_100 = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_200 = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_300 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_100 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_200 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_300 = models.FloatField(blank=True, null=True, default=None)
    RECONC_BAG_BRS = models.FloatField(blank=True, null=True, default=None)
    ID_BAG_100 = models.FloatField(blank=True, null=True, default=None)
    ID_BAG_200 = models.FloatField(blank=True, null=True, default=None)
    PASSERELLE_PSG = models.FloatField(blank=True, null=True, default=None)
    CAMION_ELEV = models.FloatField(blank=True, null=True, default=None)
    VIP_BUS = models.FloatField(blank=True, null=True, default=None)
    VEHICULE_TRANSP_PISTE = models.FloatField(blank=True, null=True, default=None)
    PUSH_BACK = models.FloatField(blank=True, null=True, default=None)
    TOWING = models.FloatField(blank=True, null=True, default=None)
    CHARIOT_BAG = models.FloatField(blank=True, null=True, default=None)
    TRACT_CHARIOT = models.FloatField(blank=True, null=True, default=None)
    TAPIS_BAG = models.FloatField(blank=True, null=True, default=None)
    PLATEFORME = models.FloatField(blank=True, null=True, default=None)
    PORTE_CONTAINER_PALETTE = models.FloatField(blank=True, null=True, default=None)
    CONTAINER_PALETTE = models.FloatField(blank=True, null=True, default=None)
    ELEV_FOURCHE = models.FloatField(blank=True, null=True, default=None)
    AGENT_SERV_PISTE = models.FloatField(blank=True, null=True, default=None)
    DB_MANIP_ULD = models.FloatField(blank=True, null=True, default=None)
    assist_night = models.PositiveIntegerField(db_column = 'ASSIST NIGHT', blank = True, null = True, default=None)
    assist_weekend = models.PositiveIntegerField(db_column = 'ASSIST WEEKEND', blank = True, null = True, default=None)
    assist_jourferie = models.PositiveIntegerField(db_column = 'ASSIST JOUR FERIE', blank = True, null = True, default=None)
    standby = models.PositiveIntegerField(db_column = 'STAND BY', blank = True, null = True, default=None)
    abs_demande = models.PositiveIntegerField(db_column = 'ABSENCE DEMANDE', blank = True, null = True, default=None)
    rtr_1_3 = models.PositiveIntegerField(db_column = '1 < RETARD <= 3', blank = True, null = True, default=None)
    rtr_3_5 = models.PositiveIntegerField(db_column = '3 < RETARD <= 5', blank = True, null = True, default=None)
    rtr_5 = models.PositiveIntegerField(db_column = 'RETARD > 5', blank = True, null = True, default=None)
    cnl_12_24 = models.PositiveIntegerField(db_column = '12 < CNL <= 24', blank = True, null = True, default=None)
    cnl_12 = models.PositiveIntegerField(db_column = 'CNL <= 12', blank = True, null = True, default=None)
    reduction = models.PositiveIntegerField(db_column = 'REDUCTION', blank = True, null = True, default=None)
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    date_last_edit = models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True, blank=True)
    status = models.TextField(db_column='STATUS', null=True, default='actual')

    class Meta:
        db_table = 'TARIF_OCCAS'
    
    def __str__(self):
        return self.company_dispatcher
    
    def save(self, *args, **kwargs):
        #this line below save every fields of the model instance
        super(TARIF_OCCAS, self).save(*args, **kwargs)


class COMP_DISPATCHER(models.Model):
    company_dispatcher = models.TextField(db_column='COMPANY DISPATCHER', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    solde = models.FloatField(db_column='SOLDE', blank=True, null=True)  # Field name made lowercase.
    solde_estimee = models.FloatField(db_column='SOLDE ESTIMEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    solde_last_edit = models.DateTimeField(db_column='SOLDE_LAST_EDIT', blank=True, null=True)  # Field name made lowercase.
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    monnaie = models.TextField(db_column='MONNAIE', blank=True, choices=monnaie)
    activite = models.TextField(db_column='ACTIVITE', blank=True, null=True)
    slug = models.SlugField(blank=True)
    solde_date = models.DateField(db_column='SOLDE DATE', blank=True, null=True)
    MTOW_10_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_30_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_10_30_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_30_50_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_30_50_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_50_80_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_50_80_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_80_150_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_80_150_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_150_250_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_150_250_TECH = models.FloatField(blank=True, null=True, default=None)
    MTOW_250_COM = models.FloatField(blank=True, null=True, default=None)
    MTOW_250_TECH = models.FloatField(blank=True, null=True, default=None)
    ASSIST_WCH = models.FloatField(blank=True, null=True, default=None)
    ASSIST_UM = models.FloatField(blank=True, null=True, default=None)
    ASSIST_TRANSIT = models.FloatField(blank=True, null=True, default=None)
    ACC_SALON = models.FloatField(blank=True, null=True, default=None)
    ASSIST_VIP = models.FloatField(blank=True, null=True, default=None)
    USE_DCS = models.FloatField(blank=True, null=True, default=None)
    DEPORTEE = models.FloatField(blank=True, null=True, default=None)
    AGENT_SERV_PASSAGE = models.FloatField(blank=True, null=True, default=None)
    CIVIERE = models.FloatField(blank=True, null=True, default=None)
    HUM = models.FloatField(blank=True, null=True, default=None)
    OUV_DOSS_BAG = models.FloatField(blank=True, null=True, default=None)
    DOSS_VOL_IMP = models.FloatField(blank=True, null=True, default=None)
    AGENT_COORD = models.FloatField(blank=True, null=True, default=None)
    COMM_SOL_COCKPIT = models.FloatField(blank=True, null=True, default=None)
    AGENT_OP_QUALIF = models.FloatField(blank=True, null=True, default=None)
    GPU = models.FloatField(blank=True, null=True, default=None)
    ASU_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    ASU_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    ACU = models.FloatField(blank=True, null=True, default=None)
    VIDE_TOILET_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    VIDE_TOILET_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    PLEIN_WATER_MOY_PORT = models.FloatField(blank=True, null=True, default=None)
    PLEIN_WATER_BIG_PORT = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_100 = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_200 = models.FloatField(blank=True, null=True, default=None)
    NET_CABINE_300 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_100 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_200 = models.FloatField(blank=True, null=True, default=None)
    ARRANGEMENT_CAB_300 = models.FloatField(blank=True, null=True, default=None)
    RECONC_BAG_BRS = models.FloatField(blank=True, null=True, default=None)
    ID_BAG_100 = models.FloatField(blank=True, null=True, default=None)
    ID_BAG_200 = models.FloatField(blank=True, null=True, default=None)
    PASSERELLE_PSG = models.FloatField(blank=True, null=True, default=None)
    CAMION_ELEV = models.FloatField(blank=True, null=True, default=None)
    VIP_BUS = models.FloatField(blank=True, null=True, default=None)
    VEHICULE_TRANSP_PISTE = models.FloatField(blank=True, null=True, default=None)
    PUSH_BACK = models.FloatField(blank=True, null=True, default=None)
    TOWING = models.FloatField(blank=True, null=True, default=None)
    CHARIOT_BAG = models.FloatField(blank=True, null=True, default=None)
    TRACT_CHARIOT = models.FloatField(blank=True, null=True, default=None)
    TAPIS_BAG = models.FloatField(blank=True, null=True, default=None)
    PLATEFORME = models.FloatField(blank=True, null=True, default=None)
    PORTE_CONTAINER_PALETTE = models.FloatField(blank=True, null=True, default=None)
    CONTAINER_PALETTE = models.FloatField(blank=True, null=True, default=None)
    ELEV_FOURCHE = models.FloatField(blank=True, null=True, default=None)
    AGENT_SERV_PISTE = models.FloatField(blank=True, null=True, default=None)
    DB_MANIP_ULD = models.FloatField(blank=True, null=True, default=None)
    assist_night = models.PositiveIntegerField(db_column = 'ASSIST NIGHT', blank = True, null = True, default=None)
    assist_weekend = models.PositiveIntegerField(db_column = 'ASSIST WEEKEND', blank = True, null = True, default=None)
    assist_jourferie = models.PositiveIntegerField(db_column = 'ASSIST JOUR FERIE', blank = True, null = True, default=None)
    standby = models.PositiveIntegerField(db_column = 'STAND BY', blank = True, null = True, default=None)
    abs_demande = models.PositiveIntegerField(db_column = 'ABSENCE DEMANDE', blank = True, null = True, default=None)
    rtr_1_3 = models.PositiveIntegerField(db_column = '1 < RETARD <= 3', blank = True, null = True, default=None)
    rtr_3_5 = models.PositiveIntegerField(db_column = '3 < RETARD <= 5', blank = True, null = True, default=None)
    rtr_5 = models.PositiveIntegerField(db_column = 'RETARD > 5', blank = True, null = True, default=None)
    cnl_12_24 = models.PositiveIntegerField(db_column = '12 < CNL <= 24', blank = True, null = True, default=None)
    cnl_12 = models.PositiveIntegerField(db_column = 'CNL <= 12', blank = True, null = True, default=None)
    reduction = models.PositiveIntegerField(db_column = 'REDUCTION', blank = True, null = True, default=None)
    class Meta:
        db_table = 'COMP_DISPACTHER'
    
    def __str__(self):
        return self.company_dispatcher
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_dispatcher.lower().replace(' ', ''))
        print(self.solde_estimee)
        #this line below save every fields of the model instance
        super(COMP_DISPATCHER, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:compagnie-detail', kwargs = {
            'slug' : self.slug
        })


class FLIGHT_FI(models.Model):
    key_flt = models.TextField(db_column='KEY_FLT', primary_key=True)  # Field name made lowercase.
    status = models.TextField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    occas = models.TextField(db_column='OCCAS', blank=True, null=True)  # Field name made lowercase.
    escale_iata_field = models.TextField(db_column='ESCALE (IATA)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    date = models.TextField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    route_ac = models.TextField(db_column='ROUTE_AC', blank=True, null=True)  # Field name made lowercase.
    flt = models.TextField(db_column='FLT', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    reg = models.TextField(db_column='REG', blank=True, null=True)  # Field name made lowercase.
    fc = models.TextField(db_column='FC', blank=True, null=True)  # Field name made lowercase.
    ac = models.TextField(db_column='AC', blank=True, null=True)  # Field name made lowercase.
    chr = models.TextField(db_column='CHR', blank=True, null=True)  # Field name made lowercase.
    dep = models.TextField(db_column='DEP', blank=True, null=True)  # Field name made lowercase.
    arr = models.TextField(db_column='ARR', blank=True, null=True)  # Field name made lowercase.
    std = models.TextField(db_column='STD', blank=True, null=True)  # Field name made lowercase.
    sta = models.TextField(db_column='STA', blank=True, null=True)  # Field name made lowercase.
    etd = models.TextField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.TextField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.
    tkof = models.TextField(db_column='TKof', blank=True, null=True)  # Field name made lowercase.
    tdwn = models.TextField(db_column='TDwn', blank=True, null=True)  # Field name made lowercase.
    st = models.TextField(db_column='ST', blank=True, null=True)  # Field name made lowercase.
    atd = models.TextField(db_column='ATD', blank=True, null=True)  # Field name made lowercase.
    ata = models.TextField(db_column='ATA', blank=True, null=True)  # Field name made lowercase.
    block = models.TextField(db_column='BLOCK', blank=True, null=True)  # Field name made lowercase.
    flthr = models.TextField(db_column='FLThr', blank=True, null=True)  # Field name made lowercase.
    c1 = models.TextField(db_column='C1', blank=True, null=True)  # Field name made lowercase.
    dly1 = models.TextField(db_column='DLY1', blank=True, null=True)  # Field name made lowercase.
    sub1 = models.TextField(db_column='Sub1', blank=True, null=True)  # Field name made lowercase.
    c2 = models.TextField(db_column='C2', blank=True, null=True)  # Field name made lowercase.
    dly2 = models.TextField(db_column='DLY2', blank=True, null=True)  # Field name made lowercase.
    sub2 = models.TextField(db_column='Sub2', blank=True, null=True)  # Field name made lowercase.
    c3 = models.TextField(db_column='C3', blank=True, null=True)  # Field name made lowercase.
    dly3 = models.TextField(db_column='DLY3', blank=True, null=True)  # Field name made lowercase.
    sub3 = models.TextField(db_column='Sub3', blank=True, null=True)  # Field name made lowercase.
    c4 = models.TextField(db_column='C4', blank=True, null=True)  # Field name made lowercase.
    dly4 = models.TextField(db_column='DLY4', blank=True, null=True)  # Field name made lowercase.
    sub4 = models.TextField(db_column='Sub4', blank=True, null=True)  # Field name made lowercase.
    c5 = models.TextField(db_column='C5', blank=True, null=True)  # Field name made lowercase.
    dly5 = models.TextField(db_column='DLY5', blank=True, null=True)  # Field name made lowercase.
    sub5 = models.TextField(db_column='Sub5', blank=True, null=True)  # Field name made lowercase.
    c6 = models.TextField(db_column='C6', blank=True, null=True)  # Field name made lowercase.
    dly6 = models.TextField(db_column='DLY6', blank=True, null=True)  # Field name made lowercase.
    sub6 = models.TextField(db_column='Sub6', blank=True, null=True)  # Field name made lowercase.
    c7 = models.TextField(db_column='C7', blank=True, null=True)  # Field name made lowercase.
    dly7 = models.TextField(db_column='DLY7', blank=True, null=True)  # Field name made lowercase.
    sub7 = models.TextField(db_column='Sub7', blank=True, null=True)  # Field name made lowercase.
    c8 = models.TextField(db_column='C8', blank=True, null=True)  # Field name made lowercase.
    dly8 = models.TextField(db_column='DLY8', blank=True, null=True)  # Field name made lowercase.
    sub8 = models.TextField(db_column='Sub8', blank=True, null=True)  # Field name made lowercase.
    c1a = models.TextField(db_column='C1A', blank=True, null=True)  # Field name made lowercase.
    dly1a = models.TextField(db_column='DLY1A', blank=True, null=True)  # Field name made lowercase.
    sub9 = models.TextField(db_column='Sub9', blank=True, null=True)  # Field name made lowercase.
    c2a = models.TextField(db_column='C2A', blank=True, null=True)  # Field name made lowercase.
    dly2a = models.TextField(db_column='DLY2A', blank=True, null=True)  # Field name made lowercase.
    sb10 = models.TextField(db_column='Sb10', blank=True, null=True)  # Field name made lowercase.
    cargo = models.TextField(db_column='Cargo', blank=True, null=True)  # Field name made lowercase.
    mail = models.TextField(db_column='Mail', blank=True, null=True)  # Field name made lowercase.
    payld = models.TextField(db_column='Payld', blank=True, null=True)  # Field name made lowercase.
    bags = models.TextField(db_column='Bags', blank=True, null=True)  # Field name made lowercase.
    exp_pax_f = models.TextField(db_column='EXP PAX F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    exp_pax_c = models.TextField(db_column='EXP PAX C', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    exp_pax_y = models.TextField(db_column='EXP PAX Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    exp_pax_inf = models.TextField(db_column='EXP PAX INF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    act_pax_f = models.TextField(db_column='ACT PAX F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    act_pax_c = models.TextField(db_column='ACT PAX C', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    act_pax_y = models.TextField(db_column='ACT PAX Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    act_pax_inf = models.TextField(db_column='ACT PAX INF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    exp_ttl = models.TextField(db_column='EXP TTL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pax_ttl = models.TextField(db_column='PAX TTL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    seats_ttl = models.TextField(db_column='SEATS TTL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lf_field = models.TextField(db_column='LF %', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ac_config1 = models.TextField(db_column='AC CONFIG1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config2 = models.TextField(db_column='AC CONFIG2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config3 = models.TextField(db_column='AC CONFIG3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ac_config4 = models.TextField(db_column='AC CONFIG4', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    log_page_field = models.TextField(db_column='Log_Page#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    character_seats_f = models.TextField(db_column='Character Seats F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.      
    character_seats_c = models.TextField(db_column='Character Seats C', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    character_seats_y = models.TextField(db_column='Character Seats Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.      
    character_seats_inf = models.TextField(db_column='Character Seats INF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.  
    code_share_and_seats_f = models.TextField(db_column='Code Share and Seats F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code_share_and_seats_c = models.TextField(db_column='Code Share and Seats C', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code_share_and_seats_y = models.TextField(db_column='Code Share and Seats Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code_share_and_seats_inf = models.TextField(db_column='Code Share and Seats INF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dist = models.TextField(db_column='Dist', blank=True, null=True)  # Field name made lowercase.
    dstand = models.TextField(db_column='DStand', blank=True, null=True)  # Field name made lowercase.
    astand = models.TextField(db_column='AStand', blank=True, null=True)  # Field name made lowercase.
    change_reason = models.TextField(db_column='Change reason', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    init = models.TextField(db_column='Init', blank=True, null=True)  # Field name made lowercase.
    uplf_w = models.TextField(db_column='Uplf W', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ramp = models.TextField(db_column='Ramp', blank=True, null=True)  # Field name made lowercase.
    stdn = models.TextField(db_column='Stdn', blank=True, null=True)  # Field name made lowercase.
    burn = models.TextField(db_column='Burn', blank=True, null=True)  # Field name made lowercase.
    uplf_v = models.TextField(db_column='Uplf V', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    usg_lts = models.TextField(db_column='USG/LTS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tank = models.TextField(db_column='Tank', blank=True, null=True)  # Field name made lowercase.
    zfw = models.TextField(db_column='ZFW', blank=True, null=True)  # Field name made lowercase.
    fpburn = models.TextField(db_column='FPBurn', blank=True, null=True)  # Field name made lowercase.
    sgrav = models.TextField(db_column='SGrav', blank=True, null=True)  # Field name made lowercase.
    miles = models.TextField(db_column='Miles', blank=True, null=True)  # Field name made lowercase.
    rt_base = models.TextField(db_column='Rt base', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dgate = models.TextField(db_column='DGate', blank=True, null=True)  # Field name made lowercase.
    agate = models.TextField(db_column='AGate', blank=True, null=True)  # Field name made lowercase.
    orig_arr_station = models.TextField(db_column='Orig.ARR Station', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.        
    d_closed = models.TextField(db_column='D.Closed', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ch_type_app = models.TextField(blank=True, null=True)
    ch_std = models.TextField(blank=True, null=True)
    ch_dest = models.TextField(blank=True, null=True)
    ch_config = models.TextField(blank=True, null=True)
    fi_file = models.DateTimeField(db_column='FI_FILE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'FLIGHT_FI'
    
    def __str__(self):
        return self.key_flt


class FLIGHT_OCCAS(models.Model):
    key_flt = models.TextField(db_column='KEY_FLT', primary_key=True)  # Field name made lowercase.
    n_field = models.FloatField(db_column='N°', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    date_demande = models.DateTimeField(db_column='DATE DEMANDE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compagnie_dispatcher = models.TextField(db_column='COMPAGNIE DISPATCHER', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.    
    type_avion = models.TextField(db_column='TYPE AVION', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reg = models.TextField(db_column='REG', blank=True, null=True)  # Field name made lowercase.
    mtow_tonnes_field = models.FloatField(db_column='MTOW (Tonnes)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nature_touchee = models.TextField(db_column='NATURE TOUCHEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    operateur = models.TextField(db_column='OPERATEUR', blank=True, null=True)  # Field name made lowercase.
    n_vol_arr = models.TextField(db_column='N VOL ARR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_arrivee = models.DateTimeField(db_column='DATE ARRIVEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    heure_arr = models.TimeField(db_column='HEURE ARR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prov = models.TextField(db_column='PROV', blank=True, null=True)  # Field name made lowercase.
    escale_iata_field = models.TextField(db_column='ESCALE (IATA)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    n_vol_dep = models.TextField(db_column='N VOL DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_depart = models.DateTimeField(db_column='DATE DEPART', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    heure_dep = models.TimeField(db_column='HEURE DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dest = models.TextField(db_column='DEST', blank=True, null=True)  # Field name made lowercase.
    montant_prevus = models.FloatField(db_column='MONTANT PREVUS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mode_de_payement = models.TextField(db_column='MODE DE PAYEMENT', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.        
    monnaie = models.TextField(db_column='MONNAIE', blank=True, null=True)  # Field name made lowercase.
    etat_du_vol = models.TextField(db_column='ETAT DU VOL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_cnl = models.DateTimeField(db_column='DATE CNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    heure_cnl = models.TimeField(db_column='HEURE CNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cnl_eta = models.TimeField(db_column='CNL / ETA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    obs = models.FloatField(db_column='OBS', blank=True, null=True)  # Field name made lowercase.
    ata = models.FloatField(db_column='ATA', blank=True, null=True)  # Field name made lowercase.
    atd = models.FloatField(db_column='ATD', blank=True, null=True)  # Field name made lowercase.
    nbr_pax = models.FloatField(db_column='NBR PAX', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cgo_kg_field = models.FloatField(db_column='CGO (KG)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    n_fiche_touchee = models.FloatField(db_column='N° FICHE TOUCHEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.        
    montant_facture = models.FloatField(db_column='MONTANT FACTURE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unnamed_31 = models.FloatField(db_column='Unnamed: 31', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    n_facture = models.FloatField(db_column='N° FACTURE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slug = models.SlugField(blank=True)
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    date_last_edit = models.DateTimeField(db_column='DATE LAST EDIT', null=True, blank=True)

    class Meta:
        db_table = 'FLIGHT_OCCAS'
    
    def save(self, *args, **kwargs):
        date_dep = self.date_depart.replace('-', '').replace('2021', '21')
        date_dep = date_dep[4:] + date_dep[2:4] + date_dep[:2]
        self.key_flt = date_dep + self.n_vol_dep + self.prov
        self.slug = slugify(self.key_flt)
        #this line below save every fields of the model instance
        super(FLIGHT_OCCAS, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:flight-detail', kwargs = {
            'slug' : self.slug
        })
    
    def get_absolute_add_url(self):
        return reverse('core:add-occas-flight', kwargs={
            'slug' : 1
        })
    
    def get_solde_est(self):
        comp = COMP_DISPATCHER.objects.get(company_dispatcher=self.compagnie_dispatcher)
        return comp.solde_estimee


class FLIGHT_SSIM(models.Model):
    key_flt = models.TextField(db_column='KEY_FLT', primary_key=True)  # Field name made lowercase.
    status = models.TextField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    ssim_period = models.TextField(blank=True, null=True)
    index_commercial = models.TextField(blank=True, null=True)
    st_ssim = models.TextField(db_column='ST_SSIM', blank=True, null=True)  # Field name made lowercase.
    airline = models.TextField(db_column='Airline', blank=True, null=True)  # Field name made lowercase.
    flight_number = models.TextField(db_column='Flight_Number', blank=True, null=True)  # Field name made lowercase.
    itinirary_variation_indicator = models.TextField(db_column='Itinirary_Variation_Indicator', blank=True, null=True)  # Field name made lowercase.
    leg_sequence_number = models.TextField(db_column='Leg_Sequence_Number', blank=True, null=True)  # Field name made lowercase.
    service_type = models.TextField(db_column='Service_Type', blank=True, null=True)  # Field name made lowercase.
    start_period = models.TextField(db_column='Start_period', blank=True, null=True)  # Field name made lowercase.
    end_period = models.TextField(db_column='End_period', blank=True, null=True)  # Field name made lowercase.
    monday = models.TextField(db_column='Monday', blank=True, null=True)  # Field name made lowercase.
    tuesday = models.TextField(db_column='Tuesday', blank=True, null=True)  # Field name made lowercase.
    wednesday = models.TextField(db_column='Wednesday', blank=True, null=True)  # Field name made lowercase.
    thursday = models.TextField(db_column='Thursday', blank=True, null=True)  # Field name made lowercase.
    friday = models.TextField(db_column='Friday', blank=True, null=True)  # Field name made lowercase.
    saturday = models.TextField(db_column='Saturday', blank=True, null=True)  # Field name made lowercase.
    sunday = models.TextField(db_column='Sunday', blank=True, null=True)  # Field name made lowercase.
    departure_station = models.TextField(db_column='Departure_Station', blank=True, null=True)  # Field name made lowercase.
    pax_std_utc = models.TextField(db_column='PAX_STD_UTC', blank=True, null=True)  # Field name made lowercase.
    std_utc = models.TextField(db_column='STD_UTC', blank=True, null=True)  # Field name made lowercase.
    std_variation_sign = models.TextField(db_column='STD_Variation_Sign', blank=True, null=True)  # Field name made lowercase.
    std_variation_utc = models.TextField(db_column='STD_Variation_UTC', blank=True, null=True)  # Field name made lowercase.
    arrival_station = models.TextField(db_column='Arrival_Station', blank=True, null=True)  # Field name made lowercase.
    sta_utc = models.TextField(db_column='STA_UTC', blank=True, null=True)  # Field name made lowercase.
    pax_sta_utc = models.TextField(db_column='PAX_STA_UTC', blank=True, null=True)  # Field name made lowercase.
    sta_variation_sign = models.TextField(db_column='STA_Variation_Sign', blank=True, null=True)  # Field name made lowercase.
    sta_variation_utc = models.TextField(db_column='STA_Variation_UTC', blank=True, null=True)  # Field name made lowercase.
    aircraft_type = models.TextField(db_column='Aircraft_Type', blank=True, null=True)  # Field name made lowercase.
    fly_next_number = models.TextField(blank=True, null=True)
    aircraft_configuration = models.TextField(db_column='Aircraft_Configuration', blank=True, null=True)  # Field name made lowercase.
    fly_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    vol_commercial_number = models.TextField(blank=True, null=True)
    vol_commercial_airline = models.TextField(blank=True, null=True)
    code_ssim = models.TextField(blank=True, null=True)
    day_op = models.FloatField(blank=True, null=True)
    ch_type_app = models.TextField(blank=True, null=True)
    ch_std = models.TextField(blank=True, null=True)
    ch_dest = models.TextField(blank=True, null=True)
    ch_config = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'FLIGHT_SSIM'


class FLIGHT_ASSIST(models.Model):
    key_flt = models.TextField(db_column='KEY_FLT', primary_key=True)  # Field name made lowercase.
    n_field = models.IntegerField(db_column='N°', blank=True, null=True)
    date_demande = models.DateField(db_column='DATE DEMANDE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    heure_demande = models.TimeField(db_column='HEURE DEMANDE', blank=True, null=True)
    etat_du_vol = models.TextField(db_column='ETAT DU VOL', blank=True, null=True)  # Field name made lowercase.
    reponse = models.BooleanField(db_column='REPONSE', blank=True, null=True, default=False)
    date_cnl = models.DateField(db_column='DATE CNL', blank=True, null=True, validators=[validate_date])  # Field name made lowercase. Field renamed to remove unsuitable characters.
    heure_cnl = models.TimeField(db_column='HEURE CNL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cnl_eta = models.DurationField(db_column='CNL / ETA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    obs = models.TextField(db_column='OBS', blank=True, null=True)  # Field name made lowercase.
    monnaie = models.TextField(db_column='MONNAIE', blank=True, null=True)  # Field name made lowercase.
    escale = models.TextField(db_column='ESCALE (IATA)', blank=True, null=True)  # Field name made lowercase.
    date_arrivee = models.DateField(db_column='DATE ARRIVEE', blank=True, null=True, validators=[validate_date])  # Field name made lowercase. Field renamed to remove unsuitable characters.
    act_dte_arr = models.DateField(db_column='ACT DTE ARR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prov = models.TextField(db_column='PROV', blank=True, null=True)  # Field name made lowercase.
    n_vol_arr = models.TextField(db_column='N° VOL ARRIV', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sta = models.TimeField(db_column='STA', blank=True, null=True)  # Field name made lowercase.
    ata = models.TimeField(db_column='ATA', blank=True, null=True)  # Field name made lowercase.
    pax_arriv = models.PositiveIntegerField(default = 0, db_column='PAX ARRIV', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cargo_arriv = models.PositiveIntegerField(default = 0, db_column='CARGO ARRIV', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_depart = models.DateField(db_column='DATE DEPART', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.    
    act_dte_dep = models.DateField(db_column='ACT DTE DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dest = models.TextField(db_column='DEST', blank=True, null=True)  # Field name made lowercase.
    n_vol_dep = models.TextField(db_column='N° VOL DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    std = models.TimeField(db_column='STD', blank=True, null=True)  # Field name made lowercase.
    atd = models.TimeField(db_column='ATD', blank=True, null=True)  # Field name made lowercase.
    pax_dep = models.PositiveIntegerField(default = 0, db_column='PAX DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cargo_dep = models.PositiveIntegerField(default = 0, db_column='CARGO DEP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    compagnie_dispatcher = models.TextField(db_column='COMPAGNIE DISPATCHER', blank=True, null=True)
    n_fiche_touchee = models.TextField(db_column='N° FICHE TOUCHEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fiche_received = models.BooleanField(db_column='FICHE RECUS', null=True, default=False)
    fiche_scannee_conforme_recieved = models.BooleanField(db_column='FICHE CONFORME RECUS', null=True, default=False)
    fiche_phys_received = models.BooleanField(db_column='FICHE PHYS RECUS', null=True, default=False)
    nature_touchee = models.TextField(db_column='NATURE TOUCHEE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    operateur = models.TextField(db_column='OPERATEUR', blank=True, null=True)  # Field name made lowercase.
    type_avion = models.TextField(db_column='TYPE AVION', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mtow_tonnes_field = models.FloatField(db_column='MTOW (Tonnes)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    reg = models.TextField(db_column='REG', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    parking = models.TextField(db_column='PARKING', blank=True, null=True)  # Field name made lowercase.
    mode_paiement = models.TextField(db_column='MODE PAIEMENT', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fiche_touchee_file = models.FileField(upload_to='fiches/', null=True, blank=True)
    capacite = models.PositiveIntegerField(db_column='CAPACITE', blank=True, null=True, default = 0)
    montant_prevus = models.FloatField(default=0, db_column='MONTANT PREVUS', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.    
    ASSIST_WCH = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ASSIST_UM = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ASSIST_TRANSIT = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ACC_SALON = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ASSIST_VIP = models.PositiveIntegerField(default = 0, blank=True, null=True)
    USE_DCS = models.PositiveIntegerField(default = 0, blank=True, null=True)
    DEPORTEE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    AGENT_SERV_PASSAGE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    CIVIERE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    HUM = models.PositiveIntegerField(default = 0, blank=True, null=True)
    OUV_DOSS_BAG = models.PositiveIntegerField(default = 0, blank=True, null=True)
    DOSS_VOL_IMP = models.PositiveIntegerField(default = 0, blank=True, null=True)
    AGENT_COORD = models.PositiveIntegerField(default = 0, blank=True, null=True)
    COMM_SOL_COCKPIT = models.PositiveIntegerField(default = 0, blank=True, null=True)
    AGENT_OP_QUALIF = models.PositiveIntegerField(default = 0, blank=True, null=True)
    GPU = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ASU = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ACU = models.PositiveIntegerField(default = 0, blank=True, null=True)
    VIDE_TOILET = models.PositiveIntegerField(default = 0, blank=True, null=True)
    PLEIN_WATER = models.PositiveIntegerField(default = 0, blank=True, null=True)
    NET_CABINE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ARRANGEMENT_CAB = models.PositiveIntegerField(default = 0, blank=True, null=True)
    RECONC_BAG_BRS = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ID_BAG = models.PositiveIntegerField(default = 0, blank=True, null=True)
    PASSERELLE_PSG = models.PositiveIntegerField(default = 0, blank=True, null=True)
    CAMION_ELEV = models.PositiveIntegerField(default = 0, blank=True, null=True)
    VIP_BUS = models.PositiveIntegerField(default = 0, blank=True, null=True)
    VEHICULE_TRANSP_PISTE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    PUSH_BACK = models.PositiveIntegerField(default = 0, blank=True, null=True)
    TOWING = models.PositiveIntegerField(default = 0, blank=True, null=True)
    CHARIOT_BAG = models.PositiveIntegerField(default = 0, blank=True, null=True)
    TRACT_CHARIOT = models.PositiveIntegerField(default = 0, blank=True, null=True)
    TAPIS_BAG = models.PositiveIntegerField(default = 0, blank=True, null=True)
    PLATEFORME = models.PositiveIntegerField(default = 0, blank=True, null=True)
    PORTE_CONTAINER_PALETTE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    CONTAINER_PALETTE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    ELEV_FOURCHE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    AGENT_SERV_PISTE = models.PositiveIntegerField(default = 0, blank=True, null=True)
    DB_MANIP_ULD = models.PositiveIntegerField(default = 0, blank=True, null=True)
    assist_jourferie = models.BooleanField(db_column = 'ASSIST JOUR FERIE', blank = True, null = True, default=None)
    tarif_de_base = models.FloatField(db_column='TARIF DE BASE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    majoration = models.FloatField(db_column='MAJORATION', blank=True, null=True)  # Field name made lowercase.
    major_night = models.FloatField(db_column='MAJORATION NUIT', blank=True, null=True)
    major_weekend = models.FloatField(db_column='MAJORATION WEEKEND', blank=True, null=True)
    major_jourferie = models.FloatField(db_column='MAJORATION JOUR FERIE', blank=True, null=True)
    major_standby = models.FloatField(db_column='MAJORATION STANDBY', blank=True, null=True)
    major_abs_demande = models.FloatField(db_column='MAJORATION ABSENCE DEMANDE', blank=True, null=True)
    retard = models.FloatField(db_column='RETARD', default= '0', blank=True, null=True)  # Field name made lowercase.
    annulation = models.FloatField(db_column='ANNULATION', default= '0', blank=True, null=True)
    reduction = models.FloatField(db_column='REDUCTION', blank=True, null=True)  # Field name made lowercase.
    dcs = models.FloatField(db_column='DCS', default= '0', blank=True, null=True)  # Field name made lowercase.
    extra_service = models.FloatField(db_column='EXTRA SERVICE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    montant_globale = models.FloatField(db_column='MONTANT GLOBALE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    n_facture = models.TextField(db_column='N° FACTURE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dzd = models.FloatField(db_column='DZD', blank=True, null=True)  # Field name made lowercase.
    eur = models.FloatField(db_column='EUR', blank=True, null=True)
    slug = models.SlugField(blank=True)
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    date_last_edit = models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True, blank=True)
    
    class Meta:
        db_table = 'FLIGHT_ASSIST'
    
    def save(self, *args, **kwargs):
        date_arr = str(self.date_arrivee)
        # print('date arr : ' + date_arr)
        date_arr = date_arr.replace('-', '').replace('2021', '21')
        date_arr = date_arr[4:] + date_arr[2:4] + date_arr[:2]
        self.key_flt = date_arr + self.n_vol_arr + self.escale + self.prov
        # print(self.key_flt)
        self.slug = slugify(self.key_flt)
        #this line below save every fields of the model instance
        try:
            obj = FLIGHT_ASSIST.objects.filter(n_field = self.n_field).exclude(key_flt=self.key_flt).get()
            obj.delete()
            super(FLIGHT_ASSIST, self).save(*args, **kwargs)
        except FLIGHT_ASSIST.DoesNotExist:
            super(FLIGHT_ASSIST, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:flight-detail', kwargs = {
            'slug' : self.slug
        })
    
    def get_absolute_add_url(self):
        return reverse('core:add-occas-flight', kwargs={
            'slug' : 1
        })
    
    def get_absolute_url_post_vol(self):
        return reverse('core:post-vol', kwargs={
            'slug': self.slug
        })
    
    def get_solde_est(self):
        comp = COMP_DISPATCHER.objects.get(company_dispatcher=self.compagnie_dispatcher)
        return comp.solde_estimee



class ESCALES(models.Model):
    escale = models.TextField(db_column='ESCALE', primary_key=True)
    full_name = models.TextField(db_column='FULL NAME', blank=True, null=True)
    nb_fiche_total = models.PositiveIntegerField(db_column='NB FICHE TOTALES', default = 0, blank = True, null = True)
    nb_fiche_remain = models.PositiveIntegerField(db_column='NB FICHE RESTANTES', default = 0, blank = True, null = True)
    date_last_affect = models.DateField(db_column='DATE LAST AFFECT', null=True, blank=True)

    class Meta:
        db_table = 'ESCALES'


class FICHE_TOUCHEE(models.Model):
    n_fiche = models.IntegerField(db_column='N° FICHE', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    key_flt = models.ForeignKey(FLIGHT_ASSIST, on_delete=models.CASCADE, db_column='KEY_FLT', blank=True, null=True)  # Field name made lowercase.
    escale = models.ForeignKey(ESCALES, on_delete=models.CASCADE, db_column='ESCALE', blank=True, null=True)
    cnl_cause_fiche = models.TextField(db_column='CAUSE CNL FICHE', blank=True, null=True)
    class Meta:
        db_table = 'FICHE_TOUCHEE'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    poste = models.TextField(choices = poste, blank = True)
    dpt = models.TextField(choices=dpt, db_column='DPT', null=True, blank=True)
    escale = models.ForeignKey(ESCALES, on_delete=models.CASCADE, null=True)


class HISTORIQUE_ADD_QUOTA(models.Model):
    date_last_add = models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', primary_key=True)
    fiches_from = models.PositiveIntegerField(db_column='FROM', blank=True, null=True)
    fiches_until = models.PositiveIntegerField(db_column='UNTIL', blank=True, null=True)

    class Meta:
        db_table = 'HISTORIQUE_ADD_QUOTA'


class HISTORIQUE_AFFECT_QUOTA(models.Model):
    date_last_add = models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', primary_key=True)
    escale = models.ForeignKey(ESCALES, on_delete=models.CASCADE, db_column='ESCALE', blank=True, null=True)
    fiches_from = models.PositiveIntegerField(db_column='FROM', blank=True, null=True)
    fiches_until = models.PositiveIntegerField(db_column='UNTIL', blank=True, null=True)

    class Meta:
        db_table = 'HISTORIQUE_AFFECT_QUOTA'


class HISTORIQUE_CNL_FICHES(models.Model):
    date_last_cnl = models.DateTimeField(auto_now=True, db_column='DATE LAST CNL', primary_key=True)
    fiches_from = models.PositiveIntegerField(db_column='FROM', blank=True, null=True)
    fiches_until = models.PositiveIntegerField(db_column='UNTIL', blank=True, null=True)
    cause = models.TextField(db_column='CAUSE CNL', null=True, blank=True)
    obs = models.TextField(db_column='OBS', null=True, blank=True)

    class Meta:
        db_table = 'HISTORIQUE_CNL_FICHES'


class HISTORIQUE_REGULAR_FACT(models.Model):
    _id = models.PositiveIntegerField(db_column='ID', primary_key=True)
    date_last_add = models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', blank=True, null=True)
    company = models.ForeignKey(COMP_DISPATCHER, on_delete=models.CASCADE, db_column='COMPANY', blank=True, null=True)
    from_date = models.DateField(db_column='FROM', blank=True, null=True)
    until_date = models.DateField(db_column='UNTIL', blank=True, null=True)
    escale = models.ForeignKey(ESCALES, on_delete=models.CASCADE, db_column='ESCALE', blank=True, null=True)
    user_add = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER', blank=True, null=True)
    montant = models.FloatField(db_column='MONTANT', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    type_fact = models.TextField(db_column='TYPE FACT', blank=True, null=True)

    class Meta:
        db_table = 'HISTORIQUE_REGULAR_FACT'


class HISTORIQUE_OP_COMPANY(models.Model):
    _id = models.AutoField(primary_key=True)
    date_last_add = models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', blank=True, null=True)
    company = models.ForeignKey(COMP_DISPATCHER, on_delete=models.CASCADE, db_column='COMPANY', blank=True, null=True)
    old_solde = models.FloatField(db_column='OLD_SOLDE', blank=True, null=True)
    date_old_solde = models.DateField(db_column='OLD SOLDE DATE', blank=True, null=True)
    date_new_solde = models.DateField(db_column='NEW SOLDE DATE', blank=True, null=True)
    new_solde = models.FloatField(db_column='NEW_SOLDE', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    user_add = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER', blank=True, null=True)

    class Meta:
        db_table = 'HISTORIQUE_OP_COMPANY'


# DPT BAGAGES

class BAG_RL(models.Model):
    code = models.AutoField(primary_key=True)
    rl = models.TextField(db_column='RL', null=True, blank=True)

    class Meta:
        db_table = 'BAG_RL'

class BAG_ID_CHART(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(db_column='LABEL', null=True, blank=True)
    sub_cat = models.TextField(db_column='SUB_CAT', null=True, blank=True)
    cat = models.TextField(db_column='CAT', null=True, blank=True)

    class Meta:
        db_table = 'BAG_ID_CHART'

class BAG_MRD_TYPE_DMG(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(db_column='LABEL', null=True, blank=True)
    desc = models.TextField(db_column='DESC', null=True, blank=True)

    class Meta:
        db_table = 'BAG_MRD_TYPE_DMG'

class BAG_SUIVI(models.Model):
    _id = models.AutoField(primary_key=True)
    date_claim = models.DateTimeField(auto_now=True, db_column='DTE RECL', null=True, blank=True)
    escale_claim = models.TextField(db_column='STATION', blank=True, null=True)
    file_type = models.TextField(db_column='FILE TYPE', null=True, blank=True, choices=TYPE)
    ref = models.PositiveIntegerField(db_column='REF', blank=True, null=True)
    flt = models.TextField(db_column='FLT', null=True, blank=True)
    dte_flt = models.TextField(db_column='FLT_DATE', null=True, blank=True)
    fs = models.TextField(db_column='FS', null=True, blank=True)
    ft = models.TextField(db_column='FT', null=True, blank=True)
    rl = models.ForeignKey(BAG_RL, db_column='RL', null=True, blank=True, on_delete=models.CASCADE)
    prov = models.TextField(db_column='PROV', null=True, blank=True)
    dest = models.TextField(db_column='DEST', blank=True, null=True)
    status =  models.TextField(choices=status, blank=True, null=True)
    n_file = models.TextField(db_column='N° FILE', blank=True, null=True)
    pax_gender = models.TextField(db_column='GENDER', blank=True, null=True)
    pax_first_name = models.TextField(db_column='PRENOM', null=True, blank=True)
    pax_last_name = models.TextField(db_column='NOM', null=True, blank=True)
    pax_age = models.PositiveIntegerField(db_column='AGE', null=True, blank=True)
    pax_adr_pax = models.TextField(db_column='ADRESSE PAX', blank=True, null=True)
    pax_phone = models.CharField(db_column='PHONE', null=True, blank=True, max_length=10)
    pax_mail = models.TextField(db_column='MAIL', null=True, blank=True)
    pax_zip_code = models.PositiveIntegerField(db_column='ZIP', null=True, blank=True)
    pax_reg = models.TextField(db_column='REGION', blank=True, null=True)
    pax_country_res = models.TextField(db_column='COUNTRY RES', blank=True, null=True)
    pax_delivery_adr = models.TextField(db_column='DELIVERY ADDRESS', blank=True, null=True)
    pax_stay_until = models.DateField(db_column='DLV ADR STAYS UNTIL', blank=True, null=True)
    other_delivery_phone = models.CharField(db_column='OTHER PHONE', blank=True, null=True, max_length=10)
    other_delivery_mail = models.TextField(db_column='OTHER MAIL', blank=True, null=True)
    other_delivery_adr = models.TextField(db_column='OTHER ADDRESS', blank=True, null=True)
    carte_fid = models.PositiveIntegerField(db_column='CARTE FID', blank=True, null=True)
    file_conforme = models.BooleanField(db_column='CONFORME', default=False, blank=True, null=True)
    file_complet = models.BooleanField(db_column='COMPLET', default=False, blank=True, null=True)
    dte_prop = models.DateField(db_column='DATE PROPOSITION', blank=True, null=True)
    esc_dest = models.TextField(db_column='DESTINATAIRE', blank=True, null=True)
    montant_dzd = models.FloatField(db_column='DZD', blank=True, null=True)
    montant_eur = models.FloatField(db_column='EUR', blank=True, null=True)
    montant_usd = models.FloatField(db_column='USD', blank=True, null=True)
    accord = models.BooleanField(default=False, blank=True, null=True)
    dte_sign = models.DateField(db_column='DATE SIGN', blank=True, null=True)
    dpt_dest = models.TextField(db_column='DPT DESTINATAIRE', blank=True, null=True)
    dte_send_payment =  models.DateField(db_column='DATE SEND PAYMENT', blank=True, null=True)
    dte_recept = models.DateField(db_column='DATE RECEPT PAYMENT', blank=True, null=True)
    bord_env_ref = models.TextField(db_column='REF BORD ENV', blank=True, null=True)
    bord_env_accord = models.BooleanField(default=False, blank=True, null=True)
    rib_n = models.PositiveIntegerField(db_column = 'RIB VALUE', blank=True, null=True)
    rib_key = models.PositiveIntegerField(db_column = 'RIB KEY', blank=True, null=True)
    payment_status = models.TextField(db_column='PAYMENT STATUS', blank=True, null=True)
    obs = models.TextField(db_column='OBS', blank=True, null=True)
    search_status = models.TextField(db_column='SEARCH STATUS', blank=True, null=True)
    user_last_edit = models.TextField(db_column='USER LAST EDIT',null=True, blank=True)
    date_last_edit = models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True, blank=True)

    class Meta:
        db_table = 'BAG_SUIVI'
    

class BAG_DETAILS(models.Model):
    _id = models.AutoField(primary_key=True)
    suivi = models.ForeignKey(BAG_SUIVI, null=True, blank=True, on_delete=models.CASCADE)
    bag_weight = models.FloatField(db_column='WEIGHT', null=True, blank=True)
    bag_brand = models.TextField(db_column='BRAND NAME', blank=True, null=True)
    bag_details = models.TextField(db_column='DETAILS', blank=True, null=True)
    bag_phone = models.CharField(db_column='PHONE ON BAG', null=True, blank=True, max_length=10)
    bag_adr = models.TextField(db_column='ADRESS ON BAG', null=True, blank=True)
    bag_id = models.TextField(db_column='BAG ID', null=True, blank=True)
    content_dmg = models.TextField(db_column='CONTENT DMG', null=True, blank=True)
    bag_dmg_mrd = models.TextField(db_column='BAG DMG ID MRD', null=True, blank=True)
    n_tag = models.PositiveIntegerField(db_column='TAG', blank=True, null=True)
    etkt = models.PositiveIntegerField(db_column='ETKT', blank=True, null=True)

    class Meta:
        db_table = 'BAG_DETAILS'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        # pylint: disable=E1101
        Profile.objects.create(user=instance)
        instance.profile.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

escales = ESCALES.objects.all()