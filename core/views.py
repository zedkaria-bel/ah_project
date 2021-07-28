from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db.models import Max, Min, Sum, Q
from django.shortcuts import reverse
from django.contrib import messages
from sqlalchemy import create_engine
import datetime
from django.utils import timezone
from django.utils.safestring import mark_safe
from .CONST import *
from .ssim import ssim_df
from django.db.models.fields import BLANK_CHOICE_DASH
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.utils.text import slugify
import calendar
import pandas as pd
import numpy as np
import json
import re
from django_pandas.io import read_frame
from .models import (
    FLIGHT_ASSIST,
    FLIGHT_OCCAS,
    COMP_DISPATCHER,
    FLIGHT_FI,
    FICHE_TOUCHEE,
    TARIF_OCCAS,
    EXCHANGE,
    ESCALES,
    HISTORIQUE_ADD_QUOTA,
    HISTORIQUE_AFFECT_QUOTA,
    HISTORIQUE_CNL_FICHES,
    HISTORIQUE_REGULAR_FACT,
    HISTORIQUE_OP_COMPANY,
    BAG_SUIVI, BAG_ID_CHART, BAG_MRD_TYPE_DMG, BAG_RL, BAG_DETAILS, BAG_FLIGHTS,
    BAG_HIST_INDEMN,
    User,
)
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
import requests

escales = ESCALES.objects.all()

# FUNCTIONS ****************************************

def check_holiday_date(obj):
    if obj.assist_jourferie:
        return True
    return False

def assist_night(obj, etat):
    if etat == 'actual':
        if (obj.ata.hour >= datetime.datetime.strptime(NIGHT[0], '%H:%M').hour or obj.ata.hour <= datetime.datetime.strptime(NIGHT[1], '%H:%M').hour) or (obj.atd.hour >= datetime.datetime.strptime(NIGHT[0], '%H:%M').hour or obj.atd.hour <= datetime.datetime.strptime(NIGHT[1], '%H:%M').hour):
            return True
    else:
        if (datetime.datetime.strptime(obj.sta, '%H:%M').hour >= datetime.datetime.strptime(NIGHT[0], '%H:%M').hour or datetime.datetime.strptime(obj.sta, '%H:%M').hour <= datetime.datetime.strptime(NIGHT[1], '%H:%M').hour) or (datetime.datetime.strptime(obj.std, '%H:%M').hour >= datetime.datetime.strptime(NIGHT[0], '%H:%M').hour or datetime.datetime.strptime(obj.std, '%H:%M').hour <= datetime.datetime.strptime(NIGHT[1], '%H:%M').hour):
            return True
    return False

def assist_weekend(obj, etat):
    if etat == 'actual':
        if obj.act_dte_arr.weekday() == 4 or obj.act_dte_arr.weekday() == 5 or obj.act_dte_dep.weekday() == 4 or obj.act_dte_dep.weekday() == 5:
            return True
    else:
        # print(obj.date_arrivee, datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d').weekday())
        if datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d').weekday() == 4 or datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d').weekday() == 5 or datetime.datetime.strptime(obj.date_depart, '%Y-%m-%d').weekday() == 4 or datetime.datetime.strptime(obj.date_depart, '%Y-%m-%d').weekday() == 5:
            return True
    return False

def assist_standby(obj, etat):
    if etat == 'actual':   
        # act_dte_dep = datetime.datetime.strptime(obj.act_dte_dep, '%Y-%m-%d')
        # atd = datetime.datetime.strptime(obj.atd, '%H:%M')
        # act_dte_arr = datetime.datetime.strptime(obj.act_dte_arr, '%Y-%m-%d')
        # ata = datetime.datetime.strptime(obj.ata, '%H:%M')
        if datetime.datetime.combine(obj.act_dte_dep, obj.atd) - datetime.datetime.combine(obj.act_dte_arr, obj.ata) >= datetime.timedelta(hours=6):
            return True
    else:
        sta = datetime.datetime.strptime(obj.sta, '%H:%M')
        std = datetime.datetime.strptime(obj.std, '%H:%M')
        date_depart = datetime.datetime.strptime(obj.date_depart, '%Y-%m-%d')
        date_arrivee = datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d')
        if datetime.datetime.combine(date_depart.date(), std.time()) - datetime.datetime.combine(date_arrivee.date(), sta.time()) >= datetime.timedelta(hours=6):
            return True
    return False

def get_absence_demande_peno(obj):
    comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
    if datetime.datetime.combine(obj.date_arrivee, obj.sta) - datetime.datetime.combine(obj.date_demande, obj.heure_demande) < datetime.timedelta(hours=24):
        return True
    return False

def check_retard(obj):
    # act_dte_arr = datetime.datetime.strptime(obj.act_dte_arr, '%Y-%m-%d')
    # ata = datetime.datetime.strptime(obj.ata, '%H:%M')
    # sta = datetime.datetime.strptime(obj.sta, '%H:%M')
    # date_arrivee = datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d')
    if datetime.datetime.combine(obj.act_dte_arr, obj.ata) - datetime.datetime.combine(obj.date_arrivee, obj.sta) > datetime.timedelta(hours=5):
        return 50
    elif datetime.datetime.combine(obj.act_dte_arr, obj.ata) - datetime.datetime.combine(obj.date_arrivee, obj.sta) > datetime.timedelta(hours=3):
        return 30
    elif datetime.datetime.combine(obj.act_dte_arr, obj.ata) - datetime.datetime.combine(obj.date_arrivee, obj.sta) > datetime.timedelta(hours=1):
        return 15
    return 0

def get_tarif_de_base(obj):
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    if comp.activite == 'OCCASIONNEL':
        if obj.act_dte_arr is not None:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
        else:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.date_arrivee, dte_end__gte = obj.date_arrivee)
    tarif_base = 0
    # MTOW - NATURE TOUCHEE ------------------------------------------------------------------------------>
    if float(obj.mtow_tonnes_field) <= 10:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_10_TECH)
        else:
            tarif_base += (comp.MTOW_10_COM)
    elif float(obj.mtow_tonnes_field) <= 30:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_10_30_TECH)
        else:
            tarif_base += (comp.MTOW_10_30_COM)
    elif float(obj.mtow_tonnes_field) <= 50:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_30_50_TECH)
        else:
            tarif_base += (comp.MTOW_30_50_COM)
    elif float(obj.mtow_tonnes_field) <= 80:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_50_80_TECH)
        else:
            tarif_base += (comp.MTOW_50_80_COM)
    elif float(obj.mtow_tonnes_field) <= 150:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_80_150_TECH)
        else:
            tarif_base += (comp.MTOW_80_150_COM)
    elif float(obj.mtow_tonnes_field) <= 250:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_150_250_TECH)
        else:
            tarif_base += (comp.MTOW_150_250_COM)
    else:
        if obj.nature_touchee == 'TECH':
            tarif_base += (comp.MTOW_250_TECH)
        else:
            tarif_base += (comp.MTOW_250_COM)
    return tarif_base

def get_extra_services_tarif(obj):
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    if comp.activite == 'OCCASIONNEL':
        if obj.act_dte_arr is not None:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
        else:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.date_arrivee, dte_end__gte = obj.date_arrivee)
    extra_service = 0
    extra_service = (obj.ASSIST_UM * (comp.ASSIST_UM)) + (obj.ASSIST_WCH * (comp.ASSIST_WCH)) + (obj.ASSIST_TRANSIT * (comp.ASSIST_TRANSIT)) + \
    (obj.ACC_SALON * (comp.ACC_SALON)) + (obj.ASSIST_VIP * (comp.ASSIST_VIP)) + (obj.USE_DCS * (comp.USE_DCS)) + (obj.DEPORTEE * (comp.DEPORTEE)) + \
    (obj.AGENT_SERV_PASSAGE * (comp.AGENT_SERV_PASSAGE)) + (obj.CIVIERE * (comp.CIVIERE)) + (obj.HUM * (comp.HUM)) + (obj.OUV_DOSS_BAG * (comp.OUV_DOSS_BAG)) + \
    (obj.DOSS_VOL_IMP * (comp.DOSS_VOL_IMP)) + (obj.AGENT_COORD * (comp.AGENT_COORD)) + (obj.COMM_SOL_COCKPIT * (comp.COMM_SOL_COCKPIT)) + \
    (obj.AGENT_OP_QUALIF * (comp.AGENT_OP_QUALIF)) + (round((obj.GPU / 60), 2) * (comp.GPU)) + (obj.ACU * (comp.ACU)) + (obj.RECONC_BAG_BRS * (comp.RECONC_BAG_BRS)) + \
    (obj.PASSERELLE_PSG * (comp.PASSERELLE_PSG)) + (obj.CAMION_ELEV * (comp.CAMION_ELEV)) + (obj.VIP_BUS * (comp.VIP_BUS)) + (obj.VEHICULE_TRANSP_PISTE * (comp.VEHICULE_TRANSP_PISTE)) + \
    (obj.PUSH_BACK * (comp.PUSH_BACK)) + (obj.TOWING * (comp.TOWING)) + (obj.CHARIOT_BAG * (comp.CHARIOT_BAG)) + (obj.TRACT_CHARIOT * (comp.TRACT_CHARIOT)) + \
    (obj.TAPIS_BAG * (comp.TAPIS_BAG)) + (obj.PLATEFORME * (comp.PLATEFORME)) + (obj.PORTE_CONTAINER_PALETTE * (comp.PORTE_CONTAINER_PALETTE)) + \
    (obj.CONTAINER_PALETTE * (comp.CONTAINER_PALETTE)) + (obj.ELEV_FOURCHE * (comp.ELEV_FOURCHE)) + (obj.AGENT_SERV_PISTE * (comp.AGENT_SERV_PISTE)) + \
    (obj.DB_MANIP_ULD * (comp.DB_MANIP_ULD))
    if obj.capacite < 200:
        extra_service += (obj.ASU * (comp.ASU_MOY_PORT)) + (obj.VIDE_TOILET * (comp.VIDE_TOILET_MOY_PORT)) + (obj.PLEIN_WATER * (comp.PLEIN_WATER_MOY_PORT))
    else:
        extra_service += (obj.ASU * (comp.ASU_BIG_PORT)) + (obj.VIDE_TOILET * (comp.VIDE_TOILET_BIG_PORT)) + (obj.PLEIN_WATER * (comp.PLEIN_WATER_BIG_PORT)) + (obj.ID_BAG * (comp.ID_BAG_200))
    if obj.capacite <= 100:
        extra_service += (obj.NET_CABINE * (comp.NET_CABINE_100)) + (obj.ARRANGEMENT_CAB * (comp.ARRANGEMENT_CAB_100))
    elif obj.capacite <= 200:
        extra_service += (obj.NET_CABINE * (comp.NET_CABINE_200)) + (obj.ARRANGEMENT_CAB * (comp.ARRANGEMENT_CAB_200)) + (obj.ID_BAG * (comp.ID_BAG_100))
    elif obj.capacite <= 300:
        extra_service += (obj.NET_CABINE * (comp.NET_CABINE_300)) + (obj.ARRANGEMENT_CAB * (comp.ARRANGEMENT_CAB_300))
    return round(extra_service, 2)

def get_majoration(obj, etat):
    # MAJORATION
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    act = comp.activite
    if comp.activite == 'OCCASIONNEL':
        if etat == 'sched':
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.date_arrivee, dte_end__gte = obj.date_arrivee)
        else:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
    major_1 = 0
    if assist_night(obj, etat):
        major_1 += comp.assist_night
        obj.major_night = comp.assist_night
    else:
        obj.major_night = 0
    if assist_weekend(obj, etat):
        major_1 += comp.assist_weekend
        obj.major_weekend = comp.assist_weekend
    else:
        obj.major_weekend = 0
    if act == 'OCCASIONNEL' and get_absence_demande_peno(obj):
        major_1 += comp.abs_demande
        obj.major_abs_demande = comp.abs_demande
    else:
        obj.major_abs_demande = 0
    if obj.ata is not None:
        if assist_standby(obj, etat):
            major_1 += comp.standby
            obj.major_standby = comp.standby
        else:
            obj.major_standby = 0
    if etat == 'sched':
        if check_holiday_date(obj):
            major_1 += comp.assist_jourferie
            obj.major_jourferie = comp.assist_jourferie
        else:
            obj.major_jourferie = 0
    else:
        if check_holiday_date(obj):
            major_1 += comp.assist_jourferie
            obj.major_jourferie = comp.assist_jourferie
        else:
            obj.major_jourferie = 0
    if major_1 > 50:
        major_1 = 50
    return major_1

def get_penalite_cnl(obj):
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    if comp.activite == 'OCCASIONNEL':
        if obj.act_dte_arr is not None:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
        else:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.date_arrivee, dte_end__gte = obj.date_arrivee)
    major_cnl = 0
    if obj.etat_du_vol == 'ANNULE':
        if obj.cnl_eta <= datetime.timedelta(hours=12):
            major_cnl = comp.cnl_12
        elif obj.cnl_eta <= datetime.timedelta(hours=24):
            major_cnl = comp.cnl_12_24
    return major_cnl

def get_reduction(obj):
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    if comp.activite == 'OCCASIONNEL':
        if obj.act_dte_arr is not None:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.act_dte_arr, dte_end__gte = obj.act_dte_arr)
        else:
            comp = TARIF_OCCAS.objects.get(dte_begin__lte = obj.date_arrivee, dte_end__gte = obj.date_arrivee)
    reduct = 0
    if obj.nature_touchee == 'PAX' and (obj.escale == 'ALG' or obj.escale == 'ORN' or obj.escale == 'CZL'):
        if (obj.pax_arriv == 0 and obj.cargo_arriv == 0) or (obj.pax_dep == 0 and obj.cargo_dep == 0):
            reduct = comp.reduction
    return reduct

def get_montant_prevus(obj):
    montant = get_tarif_de_base(obj)
    major_1 = get_majoration(obj, 'sched')
    print(montant, major_1)
    montant = montant * (1 + (major_1 / 100)) * 1.19
    return round(montant, 2)
# FUNCTIONS ****************************************


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    elif request.user.profile.escale is not None:
        return redirect(reverse('core:agent-summary', kwargs = {
            'activite' : 'contrat'
        }))
    elif request.user.profile.dpt == 'DPT RECHERCHES ET INDEMNISATION DES BAGAGES':
        return redirect(reverse('core:luggage-view', kwargs = {
            'opt' : 'ahl'
        }))
    else:
        context = {
            'title' : 'ACCEUIL',
            'user' : request.user
        }
        return render(request, 'core/home.html', context)

def get_back(request):
    return redirect(request.META.get('HTTP_REFERER'))

class RequestSummary(ListView):
    template_name = 'core/request_summary.html'
    ordering = ['-date_demande', '-date_arrivee']

    def get_queryset(self):
        if self.kwargs['activite'] == 'occas':
            comp = COMP_DISPATCHER.objects.filter(activite='OCCASIONNEL').values_list('company_dispatcher')
            qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = comp)
        else:
            comp = COMP_DISPATCHER.objects.filter(activite='CONTRACTUEL').values_list('company_dispatcher')
            qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = comp)
        if 'qs' in self.kwargs:
            if self.kwargs['qs'] == 'awaiting-billing':
                qs = qs.filter(montant_globale__isnull = False, n_facture__isnull = True)
            else:
                exc = ['OPERE', 'NO OP', 'ANNULE']
                if self.kwargs['activite'] == 'occas':
                    qs = qs.exclude(etat_du_vol__in = exc)
                else:
                    qs = qs.filter(date_arrivee = datetime.datetime.now().date()).exclude(etat_du_vol__in = exc)
        if self.request.GET.get('etat_du_vol') and self.request.GET.get('etat_du_vol') != 'all':
            qs = qs.filter(etat_du_vol = self.request.GET.get('etat_du_vol'))
        if self.request.GET.get('nature_touchee') and self.request.GET.get('nature_touchee') != 'all':
            qs = qs.filter(nature_touchee = self.request.GET.get('nature_touchee'))
        if self.request.GET.get('escale') and self.request.GET.get('escale') != 'all':
            qs = qs.filter(escale = self.request.GET.get('escale'))
        if self.request.GET.get('compagnie_dispatcher') and self.request.GET.get('compagnie_dispatcher') != 'all':
            qs = qs.filter(compagnie_dispatcher = self.request.GET.get('compagnie_dispatcher'))
        if self.request.GET.get('fiche_received') and self.request.GET.get('fiche_received') != 'all':
            if self.request.GET.get('fiche_received') == 'oui':
                qs = qs.filter(fiche_received = True)
            else:
                qs = qs.filter(Q(fiche_received = False) | Q(fiche_received__isnull = True ))
        if self.request.GET.get('fiche_phys_received') and self.request.GET.get('fiche_phys_received') != 'all':
            if self.request.GET.get('fiche_phys_received') == 'oui':
                qs = qs.filter(fiche_phys_received = True)
            else:
                qs = qs.filter(Q(fiche_phys_received = False) | Q(fiche_phys_received__isnull = True))
        if self.request.GET.get('date_arrivee_1') and self.request.GET.get('date_arrivee_1') != '':
            date_1 = datetime.datetime.strptime(self.request.GET.get('date_arrivee_1'), '%Y-%m-%d')
        else:
            date_1 = None
        if self.request.GET.get('date_arrivee_2') and self.request.GET.get('date_arrivee_2') != '':
            date_2 = datetime.datetime.strptime(self.request.GET.get('date_arrivee_2'), '%Y-%m-%d')
        else:
            date_2 = None
        if date_1 and date_2:
            qs = qs.filter(date_arrivee__gte = date_1, date_arrivee__lte = date_2)
        elif date_1 and not date_2:
            qs = qs.filter(date_arrivee = date_1)
        elif not date_1 and date_2:
            qs = qs.filter(date_arrivee = date_2)
        return qs.order_by('-date_arrivee')

    def get_context_data(self, *args,**kwargs):
        context = super(RequestSummary, self).get_context_data(*args, **kwargs)
        context['act'] = self.kwargs['activite']
        context['etat_du_vol'] = FLIGHT_STATUS
        context['nature'] = NATURE
        context['escales'] = list(ESCALES.objects.all())
        if 'qs' in self.kwargs:
            if self.kwargs['qs'] == 'awaiting-billing':
                context['qs'] = self.kwargs['qs']
        else:
            context['qs'] = None
        if self.request.GET.get('etat_du_vol') and self.request.GET.get('etat_du_vol') != 'all':
            context['filter_etat'] = self.request.GET.get('etat_du_vol')
        if self.request.GET.get('nature_touchee') and self.request.GET.get('nature_touchee') != 'all':
            context['filter_nature'] = self.request.GET.get('nature_touchee')
        if self.request.GET.get('escale') and self.request.GET.get('escale') != 'all':
            context['filter_escale'] = self.request.GET.get('escale')
        if self.request.GET.get('compagnie_dispatcher') and self.request.GET.get('compagnie_dispatcher') != 'all':
            context['filter_cmp'] = self.request.GET.get('compagnie_dispatcher')
        if self.request.GET.get('fiche_received') and self.request.GET.get('fiche_received') != 'all':
            context['filter_fiche_rec'] = self.request.GET.get('fiche_received')
        if self.request.GET.get('fiche_phys_received') and self.request.GET.get('fiche_phys_received') != 'all':
            context['filter_fiche_phys_received'] = self.request.GET.get('fiche_phys_received')
        if self.request.GET.get('date_arrivee_1') and self.request.GET.get('date_arrivee_1') != '':
            context['filter_date_arrivee_1'] = datetime.datetime.strptime(self.request.GET.get('date_arrivee_1'), '%Y-%m-%d')
        if self.request.GET.get('date_arrivee_2') and self.request.GET.get('date_arrivee_2') != '':
            context['filter_date_arrivee_2'] = datetime.datetime.strptime(self.request.GET.get('date_arrivee_2'), '%Y-%m-%d')
        if self.kwargs['activite'] == 'occas':
            if 'qs' in self.kwargs:
                if self.kwargs['qs'] == 'awaiting-billing':
                    context['title'] = 'état des vols occasionnels non encore facturés'.upper()
                else:
                    context['title'] = 'les vols occasionnels programmés'.upper()
            else:
                context['title'] = 'éTAT DES VOLS OCCASIONNELS'.upper()
            context['companies'] = list(COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL'))
        else:
            if 'qs' in self.kwargs:
                if self.kwargs['qs'] == 'awaiting-billing':
                    context['title'] = 'etat des vols réguliers non encore facturés'.upper()
                else:
                    context['title'] = 'les vols réguliers prévus pour aujourd\'hui - '.upper() + str(datetime.datetime.now().date())
            else:
                context['title'] = 'éTAT DES VOLS réguliers'.upper()
            context['companies'] = list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL'))
        return context

class FlightOccas(DetailView):
    model = FLIGHT_ASSIST
    template_name = 'core/flight_occas_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FlightOccas, self).get_context_data(*args, **kwargs)
        context['title'] = 'DETAIL DU VOL : '.upper() + self.get_object().pk
        context['obj'] = FLIGHT_ASSIST.objects.get(key_flt=self.get_object().pk.upper())
        context['obj_esc'] = context['obj'].escale
        context['comp'] = COMP_DISPATCHER.objects.get(company_dispatcher=context['obj'].compagnie_dispatcher)
        context['monnaie'] = context['comp'].monnaie
        context['nature'] = NATURE
        context['etat_du_vol'] = FLIGHT_STATUS
        context['payment'] = PAYMENT
        context['readonly'] = 'readonly'
        context['escales'] = list(ESCALES.objects.all())
        srv = tuple((BLANK_CHOICE_DASH + list(service_passager)))
        context['services_psg'] = list(map(list, srv))
        ramp = tuple((BLANK_CHOICE_DASH + list(service_ramp_piste)))
        context['services_ramp'] = list(map(list, ramp))
        flt = FLIGHT_ASSIST.objects.get(key_flt=self.get_object().pk.upper())
        context['comp'] = COMP_DISPATCHER.objects.get(company_dispatcher=flt.compagnie_dispatcher)
        context['monnaie'] = context['comp'].monnaie
        context['act'] = context['comp'].activite
        if flt.montant_globale is not None:
            context['montant_majoration'] = (flt.majoration * flt.tarif_de_base) / 100
            context['montant_reduction'] = (flt.tarif_de_base * flt.reduction) / 100
            context['montant_retard'] = (flt.tarif_de_base * flt.retard) / 100
            context['montant_annulation'] = (flt.tarif_de_base * flt.annulation) / 100
            echg = EXCHANGE.objects.get(status='actual')
            context['montant_eur'] = flt.eur
            context['montant_usd'] = flt.montant_globale
            context['montant_dzd'] = flt.dzd
            # if context['comp'].activite == 'OCCASIONNEL':
            #     context['montant_eur'] = round(flt.montant_globale * echg.eur, 2)
            #     context['montant_usd'] = flt.montant_globale
            #     context['montant_dzd'] = flt.dzd
            # else:
            #     if context['monnaie'] == 'USD':
            #         context['montant_eur'] = round(flt.montant_globale * echg.eur, 2)
            #         context['montant_usd'] = flt.montant_globale
            #         context['montant_dzd'] = flt.dzd
            #     elif context['monnaie'] == 'EUR':
            #         context['montant_eur'] = flt.montant_globale
            #         context['montant_usd'] = round(flt.montant_globale / echg.eur, 2)
            #         context['montant_dzd'] = flt.dzd
            #     else:
            #         context['montant_dzd'] = flt.montant_globale
            #         context['montant_usd'] = round(flt.montant_globale / echg.dzd, 2)
            #         context['montant_eur'] = flt.montant_globale
        return context

def add_vol_occas_view(request):
    context = {
        'title': "AJOUT D'UN NOUVEL VOL OCCASIONNEL",
        'monnaie' : MONNAIE,
        'nature' : NATURE,
        'etat_du_vol' : FLIGHT_STATUS,
        'payment' : PAYMENT,
        'company' : BLANK_CHOICE_DASH + list(COMP_DISPATCHER.objects.all()),
        'escales' : list(ESCALES.objects.all())
    }
    return render(request, 'core/flight_occas_detail.html', context)

@login_required
def valid_company(request):
    if request.is_ajax():
        if request.method == 'POST':
            # print(request.POST)
            try:
                obj = COMP_DISPATCHER.objects.get(company_dispatcher=request.POST.get('company').upper())
            except COMP_DISPATCHER.DoesNotExist:
                obj = False
            if obj:
                if obj.activite == 'OCCASIONNEL':
                    if str(obj.solde_estimee).startswith('-'):
                        status = 'alert-danger'
                    else:
                        status = 'alert-success'
                    monnaie = ''
                    exch = EXCHANGE.objects.get(status='actual')
                    other_currency = 'USD'
                    other_montant = 0
                    if obj.monnaie == 'EUR':
                        other_currency = 'EUR'
                        # print('Current EUR exchange : ' + str(data['conversion_rates']['EUR']))
                        other_montant = round(obj.solde_estimee * exch.eur, 2)
                    elif obj.monnaie == 'DZD':
                        other_currency = 'DZD'
                        # print('Current DZD exchange : ' + str(data['conversion_rates']['DZD']))
                        other_montant = round(obj.solde_estimee * exch.dzd, 2)
                    data = {
                        'exs' : True,
                        'activite' : obj.activite,
                        'status': status,
                        'solde' : obj.solde,
                        'solde_est' : obj.solde_estimee,
                        'monnaie' : obj.monnaie,
                        'other_currency' : other_currency,
                        'other_montant' : other_montant,
                    }
                else:
                    data = {
                        'exs' : True,
                        'activite' : obj.activite,
                        'monnaie' : obj.monnaie,
                    }
            else:
                data = {
                    'exs' : False
                }
            return JsonResponse(data)

@login_required
def valid_date(request):
    if request.is_ajax():
        if request.method == 'POST':
            datetime_check = False
            date_check = False
            actual_check = False
            # print(request.POST)
            if request.user.profile.poste == 'CHEF D\'ESCALE':
                if request.POST.get('ata') != '' and request.POST.get('atd') != '':
                    actual_check = True
                    ata = datetime.datetime.strptime(request.POST.get('ata'), '%H:%M').time()
                    atd = datetime.datetime.strptime(request.POST.get('atd'), '%H:%M').time()
                if request.POST.get('act_dte_dep') != '' and request.POST.get('act_dte_arr') != '':
                    date_check = True
                    arr = datetime.datetime.strptime(request.POST.get('act_dte_arr'), '%Y-%m-%d').date()
                    dep = datetime.datetime.strptime(request.POST.get('act_dte_dep'), '%Y-%m-%d').date()
            if( request.user.profile.poste != 'CHEF D\'ESCALE' and request.POST.get('sta') != '' and request.POST.get('std') != '' ):
                datetime_check = True
                sta = datetime.datetime.strptime(request.POST.get('sta'), '%H:%M').time()
                std = datetime.datetime.strptime(request.POST.get('std'), '%H:%M').time()
            if( request.user.profile.poste != 'CHEF D\'ESCALE' and (request.POST.get('date_arrivee') != '' and request.POST.get('date_depart') != '' )):
                date_check = True
                arr = datetime.datetime.strptime(request.POST.get('date_arrivee'), '%Y-%m-%d').date()
                dep = datetime.datetime.strptime(request.POST.get('date_depart'), '%Y-%m-%d').date()
            # print(request.POST)
            etat = False
            etat_date = False
            etat_dt = False
            if(request.POST.get('actual') != '' and len(request.POST.get('actual')) < 11 ):
                if(request.POST.get('change') == 'time'):
                    time_in = datetime.datetime.strptime(request.POST.get('actual'), '%H:%M').time()
                    if request.POST.get('ata') == request.POST.get('actual') and request.POST.get('act_dte_arr') != '':
                        dt = datetime.datetime.strptime(request.POST.get('act_dte_arr'), '%Y-%m-%d').date()
                        if datetime.datetime.combine(dt, time_in) > datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'):
                            etat = True
                    if request.POST.get('atd') == request.POST.get('actual') and request.POST.get('act_dte_dep') != '':
                        dt = datetime.datetime.strptime(request.POST.get('act_dte_dep'), '%Y-%m-%d').date()
                        if datetime.datetime.combine(dt, time_in) > datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'):
                            etat = True
                    # if request.POST.get('sta') == request.POST.get('actual') and request.POST.get('sta') != '':
                    #     dt = datetime.datetime.strptime(request.POST.get('date_arrivee'), '%Y-%m-%d').date()
                    #     if datetime.datetime.combine(dt, time_in) < datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'):
                    #         etat = True
                    # if request.POST.get('std') == request.POST.get('actual') and request.POST.get('std') != '':
                    #     dt = datetime.datetime.strptime(request.POST.get('date_depart'), '%Y-%m-%d').date()
                    #     if datetime.datetime.combine(dt, time_in) < datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'):
                    #         etat = True
                else:
                    date_in = datetime.datetime.strptime(request.POST.get('actual'), '%Y-%m-%d').date()
                    # print(date_in)
                    if datetime_check and date_check:
                        # print(request.user.profile.poste, datetime.datetime.combine(arr, ata))
                        if request.user.profile.poste == 'CHEF D\'ESCALE' and (datetime.datetime.combine(arr, ata) > timezone.now() or datetime.datetime.combine(dep, atd) > timezone.now()):
                            print('1')
                            etat = True
                    if request.POST.get('demande') == 'true':
                        if date_in > timezone.now().date() or date_in < timezone.now().date() - datetime.timedelta(days=8):
                            print('2')
                            etat = True
                    else:
                        if (request.user.profile.poste == 'CHEF D\'ESCALE' and (date_in > timezone.now().date() or (date_in < timezone.now().date() - datetime.timedelta(days=15) or date_in < timezone.now().date() - datetime.timedelta(days=15)) ) ):
                            print('3')
                            etat = True
            # print('date check : ' + str(date_check))

            if date_check:
                if dep < arr:
                    etat_date = True
                # print('dt check : ' + str(datetime_check))
                # print(datetime_check)
                if datetime_check:
                    # print('TRUEX')
                    # print(datetime.datetime.combine(dep, std), datetime.datetime.combine(arr, sta))
                    if datetime.datetime.combine(dep, std) < datetime.datetime.combine(arr, sta):
                        etat_dt = True
                if actual_check:
                    if datetime.datetime.combine(dep, atd) < datetime.datetime.combine(arr, ata):
                        etat_dt = True
            data = {
                'etat': etat,
                'etat_date': etat_date,
                'etat_dt': etat_dt
            }
            return JsonResponse(data)

@login_required
def valid_fiche(request):
    if request.is_ajax():
        if request.method == 'POST':
            get = False
            plage = False
            cnl = False
            msg = ''
            if 'n_fiche_touchee' in request.POST:
                if request.POST.get('n_fiche_touchee') != '':
                    fiche = request.POST.get('n_fiche_touchee')
                else:
                    fiche = None
            if request.POST.get('n_fiche_touchee_1') != '':
                fiche_1 = request.POST.get('n_fiche_touchee_1')
            else:
                fiche_1 = None
            if request.POST.get('n_fiche_touchee_2') != '':
                fiche_2 = request.POST.get('n_fiche_touchee_2')
            else:
                fiche_2 = None
            if request.user.profile.escale is None:
                list_fiches = FICHE_TOUCHEE.objects.all().values_list('n_fiche', flat=True)
            else:
                L = [fiche]
                list_fiches = FICHE_TOUCHEE.objects.filter(escale=request.user.profile.escale.escale).values_list('n_fiche', flat=True)
            list_fiches = list(list_fiches)
            if fiche_1 != None:
                cnl = True
                if fiche_2 != None:
                    if int(fiche_1) >= int(fiche_2):
                        get = True
                        msg = 'Les fiches doivent êtres indiquées à partir du plus petit jusqu\'au plus grand !'
                    if request.user.profile.escale is not None and (fiche is not None and int(fiche) >= int(fiche_1) and int(fiche) <= int(fiche_2)):
                        get = True
                        msg = 'Les fiches annulées doivent être différentes de celle que vous allez envoyé !'
                    plage = True
                    if request.user.profile.escale is not None and (int(fiche_1) not in list_fiches or int(fiche_2) not in list_fiches):
                        get = True
                        msg = 'Cette escale ne contient pas certaines fiches indiquées !'
                    if request.user.profile.escale is not None:
                        for f in range(int(fiche_1), int(fiche_2)+1):
                            L.append(f)
                else:
                    if int(fiche) == int(fiche_1):
                        get = True
                        msg = 'Les fiches annulées doivent être différentes de celle que vous allez envoyé !'
                    else:
                        if request.user.profile.escale is not None:
                            L.append(fiche_1)
                if get:
                    data = {
                        'exist' : get,
                        'msg': msg
                    }
                    return JsonResponse(data)
            fiches = [int(x) for x in L if x is not None]
            for fiche in fiches:
                if fiche not in list_fiches:
                    get = True
                    msg = 'La fiche N° ' + str(fiche) + ' n\'existe pas pour cette escale !'
                else:
                    obj = FICHE_TOUCHEE.objects.get(n_fiche=fiche)
                    if obj.status == 'CONSOMME'.upper() or obj.status == 'ANNULE':
                        get = True
                        if plage:
                            msg = 'Interval de fiches incorrect ! La fiche N° ' + str(fiche) + ' n\'est plus disponible !'
                        else:
                            msg = 'La fiche N° ' + str(fiche) + ' n\'est plus disponible !'
            data = {
                'exist' : get,
                'msg': msg
            }
            return JsonResponse(data)
            
@login_required
def valid_services(request):
    if request.is_ajax():
        if request.method == 'POST':
            # print(request.POST)
            data = {
                'same': False
            }
            same = False
            if request.POST.get('srv') == 'ramp':
                # print(request.POST)
                # print(request.POST.get('pist_autre_serv_1'), request.POST.get('pist_autre_serv_2'), request.POST.get('pist_autre_serv_3'))
                if request.POST.get('pist_autre_serv_1') == request.POST.get('pist_autre_serv_2'):
                    if request.POST.get('pist_autre_serv_1') != '---------' and request.POST.get('pist_autre_serv_2') != '---------':
                        same = True
                elif request.POST.get('pist_autre_serv_1') == request.POST.get('pist_autre_serv_3'):
                    if request.POST.get('pist_autre_serv_1') != '---------' and request.POST.get('pist_autre_serv_3') != '---------':
                        same = True
                elif request.POST.get('pist_autre_serv_2') == request.POST.get('pist_autre_serv_3'):
                    if request.POST.get('pist_autre_serv_2') != '---------' and request.POST.get('pist_autre_serv_3') != '---------':
                        same = True
                data = {
                    'same': same
                }
            else:
                # print(request.POST.get('psg_autre_serv_1'), request.POST.get('psg_autre_serv_2'))
                if request.POST.get('psg_autre_serv_1') != '---------' and request.POST.get('psg_autre_serv_2') != '---------':
                    if request.POST.get('psg_autre_serv_1') == request.POST.get('psg_autre_serv_2'):
                        data = {
                            'same': True
                        }
            return JsonResponse(data)

@login_required
def valid_uniq_flt(request):
    if request.is_ajax():
        if request.method == 'POST':
            work = False
            exist = False
            msg = ''
            arr = ''
            if request.POST.get('std') != '' and request.POST.get('date_depart') != '' and request.POST.get('escale') != '':
                heure_dep = datetime.datetime.strptime(request.POST.get('std'), '%H:%M')
                date_dep = datetime.datetime.strptime(request.POST.get('date_depart'), '%Y-%m-%d')
                escale = request.POST.get('escale')
                try:
                    key = FLIGHT_ASSIST.objects.get(
                        date_depart = date_dep,
                        escale = escale,
                        std = heure_dep
                    )
                    exist = True
                    arr = 'dep'
                    msg = 'Ce créneau de départ pour cette escale est dejà réservé !'
                except FLIGHT_ASSIST.DoesNotExist:
                    pass
            if request.POST.get('mode') == 'arr':
                if request.POST.get('date_arrivee') != '' and request.POST.get('sta') != '' and request.POST.get('escale') != '':
                    work = True
                    heure_arr = datetime.datetime.strptime(request.POST.get('sta'), '%H:%M')
                    date_arr = datetime.datetime.strptime(request.POST.get('date_arrivee'), '%Y-%m-%d')
                    escale = request.POST.get('escale')
                    try:
                        key = FLIGHT_ASSIST.objects.get(
                            date_arrivee = date_arr,
                            escale = escale,
                            sta = heure_arr
                        )
                        exist = True
                        arr = 'arr'
                        msg = 'Ce créneau d\'arrivée pour cette escale est dejà réservé !'
                    except FLIGHT_ASSIST.DoesNotExist:
                        pass
                if work and request.POST.get('n_vol_arr') != '' and request.POST.get('prov') != '':
                    nvol = request.POST.get('n_vol_arr')
                    prov = request.POST.get('prov')
                    try:
                        key = FLIGHT_ASSIST.objects.get(
                            n_vol_arr = nvol,
                            date_arrivee = date_arr,
                            prov = prov,
                            escale = escale
                        )
                        exist = True
                        arr = 'arr'
                        msg = 'Ce vol est déjà programmé !'
                    except FLIGHT_ASSIST.DoesNotExist:
                        pass
            data = {
                'exist' : exist,
                'msg': msg
            }
            return JsonResponse(data)

class AddVolOccas(View):
    def post(self, request):
        # print(request.POST)
        dic = dict(request.POST)
        # print(request.POST)
        del dic['csrfmiddlewaretoken']
        dic_values = dic.items()
        # print(dic_values)
        # print('\n' + dic_values)
        for key, value in dic_values:
            if not value[0] or value[0] == '---------':
                dic[key] = None
            else:
                dic[key] = value[0]
        if 'fiche_received' in dic:
            if dic['fiche_received'] == 'on':
                dic['fiche_received'] = 'True'
            else:
                dic['fiche_received'] = 'False'
        if 'assist_jourferie' in dic:
            if dic['assist_jourferie'] == 'on':
                dic['assist_jourferie'] = 'True'
            else:
                dic['assist_jourferie'] = 'False'
        if 'fiche_phys_received' in dic:
            if dic['fiche_phys_received'] == 'on':
                dic['fiche_phys_received'] = 'True'
            else:
                dic['fiche_phys_received'] = 'False'
        print(dic)
        if request.POST.get('n_field') != '0':
            obj = FLIGHT_ASSIST.objects.get(n_field=request.POST.get('n_field'))
            if obj.n_facture is None and 'n_facture' in dic and dic['n_facture'] is not None and (dic['etat_du_vol'] == 'OPERE' or dic['etat_du_vol'] == 'ANNULE'):
                print('1er')
                obj.n_facture = dic['n_facture']
                obj.reponse = True
                obj.save()
                return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                            'slug': obj.slug
                        }))
            if obj.tarif_de_base is None and 'tarif_de_base' in dic and (dic['tarif_de_base'] != '0' or dic['extra_service'] != '0'):
                print('2e')
                obj = FLIGHT_ASSIST.objects.get(n_field=request.POST.get('n_field'))
                obj.tarif_de_base = float(dic['tarif_de_base'])
                obj.majoration = float(dic['majoration'])
                obj.major_night = float(dic['major_night'])
                obj.major_weekend = float(dic['major_weekend'])
                obj.major_jourferie = float(dic['major_jourferie'])
                obj.major_standby = float(dic['major_standby'])
                obj.major_abs_demande = 0
                # obj.majoration = get_majoration(obj, 'actual')
                obj.retard = float(dic['retard'])
                obj.reduction = int(float(dic['reduction']))
                obj.extra_service = float(dic['extra_service'])
                obj.annulation = float(dic['annulation'])
                prc_totale = (obj.majoration + obj.retard + obj.annulation) - obj.reduction
                montant = obj.tarif_de_base * (1 + (prc_totale / 100)) + obj.extra_service
                # EXCHANGE
                echg = EXCHANGE.objects.exclude(status='actual').filter(date_begin__lte = obj.act_dte_arr, date_end__gte = obj.act_dte_arr).first()
                if echg is None:
                    echg = EXCHANGE.objects.get(status='actual')
                if obj.monnaie == 'USD':
                    obj.montant_globale = round(montant, 2)
                    obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                    obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                elif obj.monnaie == 'EUR':
                    obj.eur = round(montant, 2)
                    obj.montant_globale = round(obj.eur / float(echg.eur), 2)
                    obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                else:
                    obj.dzd = round(montant, 2)
                    obj.montant_globale = round(obj.eur / float(echg.dzd), 2)
                    obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                obj.n_facture = None
                obj.reponse = False
                obj.save()
                messages.success(request, 'Le vol a correctement été facturé.')
                return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                    'slug': obj.slug
                }))
            if 'tarif_de_base' in dic and (str(obj.tarif_de_base) != dic['tarif_de_base'] or str(obj.extra_service) != dic['extra_service'] or str(obj.reduction) != dic['reduction'] or str(obj.retard) != dic['retard'] or str(obj.annulation) != dic['annulation'] or str(obj.major_night) != dic['major_night'] or str(obj.major_jourferie) != dic['major_jourferie'] or str(obj.major_standby) != dic['major_standby'] or str(obj.major_weekend) != dic['major_weekend'] or str(obj.majoration) != dic['majoration']):
                print('3e')
                obj, created = FLIGHT_ASSIST.objects.update_or_create(
                    n_field=request.POST.get('n_field'),
                    defaults = dic,
                )
                obj.tarif_de_base = float(dic['tarif_de_base'])
                obj.majoration = float(dic['majoration'])
                obj.major_night = float(dic['major_night'])
                obj.major_weekend = float(dic['major_weekend'])
                obj.major_jourferie = float(dic['major_jourferie'])
                obj.major_standby = float(dic['major_standby'])
                obj.major_abs_demande = 0
                # obj.majoration = get_majoration(obj, 'actual')
                obj.retard = float(dic['retard'])
                obj.reduction = int(float(dic['reduction']))
                obj.extra_service = float(dic['extra_service'])
                obj.annulation = float(dic['annulation'])
                prc_totale = (obj.majoration + obj.retard + obj.annulation) - obj.reduction
                montant = obj.tarif_de_base * (1 + (prc_totale / 100)) + obj.extra_service
                # EXCHANGE
                echg = EXCHANGE.objects.exclude(status='actual').filter(date_begin__lte = obj.act_dte_arr, date_end__gte = obj.act_dte_arr).first()
                if echg is None:
                    echg = EXCHANGE.objects.get(status='actual')
                if obj.monnaie == 'USD':
                    obj.montant_globale = round(montant, 2)
                    obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                    obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                elif obj.monnaie == 'EUR':
                    obj.eur = round(montant, 2)
                    obj.montant_globale = round(obj.eur / float(echg.eur), 2)
                    obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                else:
                    obj.dzd = round(montant, 2)
                    obj.montant_globale = round(obj.eur / float(echg.dzd), 2)
                    obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                obj.n_facture = None
                obj.reponse = False
                obj.save()
                # CHECK IF CORRECTION
                try:
                    obj = HISTORIQUE_REGULAR_FACT.objects.get(
                        escale = ESCALES.objects.get(escale = obj.escale),
                        company = COMP_DISPATCHER.objects.get(company_dispatcher = obj.compagnie_dispatcher),
                        from_date__lte = obj.act_dte_arr,
                        until_date__gte = obj.act_dte_arr
                    )
                    qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher = obj.company, act_dte_arr__isnull = False, escale = obj.escale.escale).order_by('act_dte_arr')
                    qs = qs.filter(act_dte_arr__gte = obj.from_date, act_dte_arr__lte = obj.until_date)
                    sum = 0
                    if obj.company.monnaie == 'EUR':
                        for row in qs:
                            row.n_facture = None
                            row.save()
                            sum += row.eur
                    elif obj.company.monnaie == 'USD':
                        for row in qs:
                            row.n_facture = None
                            row.save()
                            sum += row.montant_globale
                    else:
                        for row in qs:
                            row.n_facture = None
                            row.save()
                            sum += row.dzd
                    obj.montant = round(sum, 2)
                    obj.type_fact = 'CORRECTION'
                    obj.n_facture = None
                    obj.user_add = request.user
                    obj.save()
                    return HttpResponseRedirect(reverse('core:fact-regular-detail', kwargs={
                        'slug': obj.slug
                    }))
                except HISTORIQUE_REGULAR_FACT.DoesNotExist:
                    messages.success(request, 'Le vol a correctement été facturé. Veuillez renseigner le N° de la facture.')
                    return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                            'slug': obj.slug
                        }))
        max_n = FLIGHT_ASSIST.objects.aggregate(Max('n_field'))
        # print(max_n)
        created = False
        try:
            print(request.POST.get('n_field'))
            obj = FLIGHT_ASSIST.objects.get(n_field=int(request.POST.get('n_field')))
            # print(obj)
        except FLIGHT_ASSIST.DoesNotExist:
            print('CREATE')
            obj, created = FLIGHT_ASSIST.objects.get_or_create(
                n_field = request.POST.get('n_field'),
                defaults = dic,
            )
        # print(obj, created)
        if created:
            # print('CREEER')
            obj.n_field = list(max_n.values())[0] + 1
            obj.montant_prevus = get_montant_prevus(obj)
            obj.save()
            print(obj.montant_prevus)
            # EDIT COMPANY SOLDE ESTIMEE
            comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
            if comp.activite == 'OCCASIONNEL':
                # print(comp.solde_estimee, obj.montant_prevus)
                comp.solde_estimee = round(comp.solde_estimee - obj.montant_prevus, 2)
                # print(comp.solde_estimee)
                comp.save()
                # print(comp.solde_estimee)
                if comp.solde_estimee < 0:
                    messages.error(request, mark_safe('Le solde estimé de la compagnie <b>' + comp.company_dispatcher + '</b> à l\'issue de ce vol est de <b>' + str(comp.solde_estimee) + ' ' + comp.monnaie +  '</b> !'))
                    comp.solde_estimee = round(comp.solde_estimee + obj.montant_prevus, 2)
                    comp.save()
                    # return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                    #     'slug': obj.slug
                    # }))
            # print('END CREEER')
        else:
            exist = False
            # print(FLIGHT_ASSIST.objects.get(n_field=request.POST.get('n_field')))
            if FLIGHT_ASSIST.objects.filter(date_arrivee=request.POST.get('date_arrivee'),sta=request.POST.get('sta'),escale=request.POST.get('escale')).exclude(n_field=request.POST.get('n_field')).exists():
                exist = True
                # print('ARRIVEEc XX')
                messages.error(request, 'Le créneau d\'arrivée n\'est pas disponible !')
            if FLIGHT_ASSIST.objects.filter(date_depart=request.POST.get('date_depart'),std=request.POST.get('std'),escale=request.POST.get('escale')).exclude(n_field=request.POST.get('n_field')).exists():
                exist = True
                # print('DEP XX')
                messages.error(request, 'Le créneau de départ n\'est pas disponible !')
            if not exist:
                # if 'tarif_de_base' in dic:    
                #     if dic['tarif_de_base'] == '0':
                #         dic['tarif_de_base'] = None
                #         dic['dcs'] = None
                #         dic['majoration'] = None
                #         dic['reduction'] = None
                obj, created = FLIGHT_ASSIST.objects.update_or_create(
                    n_field=request.POST.get('n_field'),
                    defaults = dic,
                )
                print(obj.montant_globale)
                comp = COMP_DISPATCHER.objects.get(company_dispatcher = obj.compagnie_dispatcher)
                if obj.montant_globale is None and obj.montant_prevus is None and comp.activite == 'OCCASIONNEL':
                    old_prevus = obj.montant_prevus
                    obj.montant_prevus = get_montant_prevus(obj)
                    print(obj.montant_prevus)
                    obj.save()
                    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
                    comp.save()
                    if comp.activite == 'OCCASIONNEL':
                        if comp.solde_estimee < 0:
                            messages.error(request, mark_safe('Le solde estimé de la compagnie <b>' + comp.company_dispatcher + '</b> à l\'issue de ce vol est de <b>' + str(comp.solde_estimee) + ' ' + comp.monnaie +  '</b> !'))
                            # comp.solde_estimee = round(comp.solde_estimee + obj.montant_prevus, 2)
                            # comp.save()
                            obj.montant_prevus = old_prevus
                            return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                                'slug': obj.slug
                            }))
                # TREAT THE CNL CASE
                # return redirect('core:home-view')
                if obj.etat_du_vol == 'ANNULE':
                    # print(timezone.now().date(), timezone.now().time())
                    obj.date_cnl = datetime.datetime.today().date()
                    obj.heure_cnl = datetime.datetime.now().time()
                    # print(obj.date_cnl, obj.heure_cnl)
                    cmb_cnl = datetime.datetime.combine(obj.date_cnl, obj.heure_cnl)
                    date_arr = datetime.datetime.strptime(obj.date_arrivee, '%Y-%m-%d').date()
                    heure_arr = datetime.datetime.strptime(obj.sta, '%H:%M').time()
                    cmb_arr = datetime.datetime.combine(date_arr, heure_arr)
                    # print(cmb_arr, cmb_cnl)
                    # print('THE DIFF : ' + str(abs(cmb_arr - cmb_cnl)))
                    obj.cnl_eta = abs(cmb_arr - cmb_cnl)
                    montant = get_tarif_de_base(obj)
                    obj.tarif_de_base = montant
                    major_cnl = get_penalite_cnl(obj)
                    obj.annulation = major_cnl
                    print(montant, major_cnl)
                    obj.montant_globale = round(montant * (1 + (major_cnl / 100)), 2)
                    obj.extra_service = 0
                    obj.major_night = 0
                    obj.major_jourferie = 0
                    obj.major_standby = 0
                    obj.major_weekend = 0
                    obj.major_abs_demande = 0
                    obj.majoration = 0
                    obj.retard = 0
                    obj.reduction = 0
                    # CURRENCY EXCHANGE
                    echg = EXCHANGE.objects.exclude(status='actual').filter(date_begin__lte = obj.date_arrivee, date_end__gte = obj.date_arrivee).first()
                    if echg is None:
                        echg = EXCHANGE.objects.get(status='actual')
                    montant = obj.montant_globale
                    if obj.monnaie == 'USD':
                        obj.montant_globale = round(montant, 2)
                        obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                        obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                    elif obj.monnaie == 'EUR':
                        obj.eur = round(montant, 2)
                        obj.montant_globale = round(obj.eur / float(echg.eur), 2)
                        obj.dzd = round(obj.montant_globale * float(echg.dzd), 2)
                    else:
                        obj.dzd = round(montant, 2)
                        obj.montant_globale = round(obj.eur / float(echg.dzd), 2)
                        obj.eur = round(obj.montant_globale * float(echg.eur), 2)
                    # Where USD is the base currency you want to use
                    # url = 'https://v6.exchangerate-api.com/v6/86fd92bcca154241892eb414/latest/USD'
                    # Making our request
                    # response = requests.get(url)
                    # data = response.json()
                    # obj.dzd = round(obj.montant_globale * float(data['conversion_rates']['DZD']), 2)
                    obj.save()
                    # MAJ DU SOLDE DE LA COMPAGNIE
                    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
                    if comp.activite == 'OCCASIONNEL':
                        comp.solde -= round(obj.montant_globale, 2)
                        comp.save()
                    obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
                    obj.save()
                    return HttpResponseRedirect(reverse('core:flight-detail', kwargs = {
                                'slug' : obj.slug
                            }))
                elif obj.date_cnl is not None:
                    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
                    comp.solde += obj.montant_globale
                    obj.montant_globale = None
                    obj.n_facture = None
                    obj.date_cnl = None
                    obj.heure_cnl=  None
                    obj.cnl_eta = None
                    obj.reponse = False
                    obj.save()
                    comp.save()
            else:
                return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                    'slug': obj.slug
                }))
        obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
        obj.save()
        if 'major_abs_demande' not in dic:
            dic['major_abs_demande'] = obj.major_abs_demande
        if obj.montant_globale is not None and (obj.montant_globale != dic['montant_globale'] or obj.tarif_de_base != dic['tarif_de_base'] or obj.extra_service != dic['extra_service'] or obj.major_night != dic['major_night'] or obj.major_weekend != dic['major_weekend'] or obj.major_jourferie != dic['major_jourferie'] or obj.major_standby != dic['major_standby'] or obj.major_abs_demande != dic['major_abs_demande'] or obj.major_abs_demande != dic['major_abs_demande'] or obj.majoration != dic['majoration'] or obj.reduction != dic['reduction'] or obj.retard != dic['retard'] or obj.annulation != dic['annulation'] ):
            return HttpResponseRedirect(reverse('core:facturation-occas', kwargs={
                'n_field': obj.n_field
            }))
        return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
                    'slug': obj.slug
                }))

class agent_flight_summary(ListView):
    paginate_by = 20
    template_name = 'core/agent_summary.html'

    def get_queryset(self):
        if self.kwargs['activite'] == 'occas':
            comp = COMP_DISPATCHER.objects.filter(activite='OCCASIONNEL').values_list('company_dispatcher')
            qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = comp)
        else:
            comp = COMP_DISPATCHER.objects.filter(activite='CONTRACTUEL').values_list('company_dispatcher')
            qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = comp)
        if self.request.GET.get('compagnie_dispatcher') and self.request.GET.get('compagnie_dispatcher') != 'all':
            qs = qs.filter(compagnie_dispatcher = self.request.GET.get('compagnie_dispatcher'))
        if self.request.GET.get('date_arrivee_1') and self.request.GET.get('date_arrivee_1') != '':
            date_1 = datetime.datetime.strptime(self.request.GET.get('date_arrivee_1'), '%Y-%m-%d')
        else:
            date_1 = None
        if self.request.GET.get('date_arrivee_2') and self.request.GET.get('date_arrivee_2') != '':
            date_2 = datetime.datetime.strptime(self.request.GET.get('date_arrivee_2'), '%Y-%m-%d')
        else:
            date_2 = None
        if date_1 and date_2:
            qs = qs.filter(date_arrivee__gte = date_1, date_arrivee__lte = date_2)
        elif date_1 and not date_2:
            qs = qs.filter(date_arrivee = date_1)
        elif not date_1 and date_2:
            qs = qs.filter(date_arrivee = date_2)
        return qs.filter(escale=self.request.user.profile.escale.escale).exclude(etat_du_vol__in = ['ANNULE', 'NO OP']).exclude(etat_du_vol = 'OPERE', ata__isnull = False).order_by('-date_arrivee')

    def get_context_data(self, *args,**kwargs):
        context = super(agent_flight_summary, self).get_context_data(*args, **kwargs)
        esc = ESCALES.objects.get(escale=self.request.user.profile.escale.escale)
        context['act'] = self.kwargs['activite']
        context['etat_du_vol'] = FLIGHT_STATUS
        context['nature'] = NATURE
        if context['act'] == 'occas':
            vols = 'OCCASIONNELS'
            context['companies'] = list(COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL'))
        else:
            vols = 'Réguliers'.upper()
            context['companies'] = list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL'))
        context['title'] = 'LISTE DES VOLS ' + vols + ' à COMPLETER - ESCALE : '.upper() + esc.full_name
        if self.request.GET.get('compagnie_dispatcher') and self.request.GET.get('compagnie_dispatcher') != 'all':
            context['filter_cmp'] = self.request.GET.get('compagnie_dispatcher')
        if self.request.GET.get('date_arrivee_1') and self.request.GET.get('date_arrivee_1') != '':
            context['filter_date_arrivee_1'] = datetime.datetime.strptime(self.request.GET.get('date_arrivee_1'), '%Y-%m-%d')
        if self.request.GET.get('date_arrivee_2') and self.request.GET.get('date_arrivee_2') != '':
            context['filter_date_arrivee_2'] = datetime.datetime.strptime(self.request.GET.get('date_arrivee_2'), '%Y-%m-%d')
        return context

class post_vol(DetailView):
    model = FLIGHT_ASSIST
    template_name = 'core/post_vol.html'

    def get_context_data(self, *args,**kwargs):
        context = super(post_vol, self).get_context_data(*args, **kwargs)
        esc = ESCALES.objects.get(escale=self.request.user.profile.escale.escale)
        context['title'] = 'Compléter les informations concernant ce vol - ESCALE : '.upper() + esc.full_name.upper()
        context['obj'] = FLIGHT_ASSIST.objects.get(key_flt=self.get_object().pk)
        context['services'] = BLANK_CHOICE_DASH + list(service_passager)
        context['ramps'] = BLANK_CHOICE_DASH + list(service_ramp_piste)
        context['causes'] = causes
        context['natures'] = list(NATURE)
        return context

class validReleveTouchee(View):
    def post(self, request):
        dic = dict(request.POST)
        print(request.POST)
        del dic['csrfmiddlewaretoken']
        dic_values = dic.items()
        for key, value in dic_values:
            if value[0] == '---------':
                dic[key] = None
            else:
                dic[key] = value[0]
        if 'assist_jourferie' in dic:
            if dic['assist_jourferie'] == 'on':
                dic['assist_jourferie'] = 'True'
            else:
                dic['assist_jourferie'] = 'False'
        if request.POST.get('n_fiche_touchee') != '':
            fiche = request.POST.get('n_fiche_touchee')
        else:
            fiche = None
        if request.POST.get('n_fiche_touchee_1') != '':
            fiche_1 = request.POST.get('n_fiche_touchee_1')
        else:
            fiche_1 = None
        if request.POST.get('n_fiche_touchee_2') != '':
            fiche_2 = request.POST.get('n_fiche_touchee_2')
        else:
            fiche_2 = None
        # print(request.POST.get('cnl_cause_fiche'))
        # print(request.POST.get('obs'))
        L = [fiche]
        if fiche_1 != None:
            if fiche_2 != None:
                for f in range(int(fiche_1), int(fiche_2)+1):
                    L.append(f)
            else:
                L.append(fiche_1)
        fiches = [int(x) for x in L if x is not None]
        print('fiche_touchee_file' in request.FILES)
        if 'fiche_touchee_file' in request.FILES:
            myfile = request.FILES['fiche_touchee_file']
            print(myfile.name, myfile.size)
            dic['fiche_touchee_file'] = myfile
        else:
            dic['fiche_touchee_file'] = None
        obj, created = FLIGHT_ASSIST.objects.update_or_create(
            n_field=request.POST.get('n_field'),
            defaults = dic
        )
        # print('A' + obj.fiche_touchee_file.name + 'A')
        obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
        obj.etat_du_vol = 'OPERE'
        if obj.fiche_touchee_file.name is not None :
            obj.fiche_received = True
        else:
            obj.fiche_received = False
        print(obj.fiche_touchee_file, type(obj.fiche_touchee_file))
        obj.save()
        # FICHES CONSOMMEES ET ANNULEES
        # print(fiches, fiches[0])
        f = FICHE_TOUCHEE.objects.get(n_fiche=int(fiches[0]))
        f.status = 'CONSOMME'
        f.key_flt = obj
        f.key_flt.key_flt = obj.key_flt.replace('-', '')
        f.save()
        fiches.pop(0)
        for fiche in fiches:
            f = FICHE_TOUCHEE.objects.get(n_fiche=int(fiche))
            # print(fiche)
            f.status = 'ANNULE'
            f.cnl_cause_fiche = request.POST.get('cnl_cause_fiche')
            f.save()
            # print('END//')
        comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
        # if comp.activite == 'CONTRACTUEL':
        #     return redirect('core:agent-summary')
        return HttpResponseRedirect(reverse('core:facturation-occas', kwargs={
            'n_field': obj.n_field
        }))

def facturation_occas(request, n_field):
    obj = FLIGHT_ASSIST.objects.get(n_field=n_field)
    # TARIF DE BASE ------------------------------------------------------------------------------>
    tarif_base = get_tarif_de_base(obj)
    obj.tarif_de_base = tarif_base
    # SERVICES ------------------------------------------------------------------------------>
    extra_service = get_extra_services_tarif(obj)
    obj.extra_service = extra_service
    # COND SPEC ------------------------------------------------------------------------------>
    major_1 = get_majoration(obj, 'actual')
    obj.majoration = major_1
    # RETARD ------------------------------------------------------------------------------>
    major_rtr = check_retard(obj)
    obj.retard = major_rtr
    # ANNULATION ------------------------------------------------------------------------------>
    major_cnl = get_penalite_cnl(obj)
    obj.annulation = major_cnl
    # REDUCTION ------------------------------------------------------------------------------>
    reduct = get_reduction(obj)
    obj.reduction = reduct
    percent_tot = (((major_1 + major_rtr + major_cnl) - reduct) / 100) + 1
    montant = (tarif_base * percent_tot) + extra_service
    # obj.montant_globale = round(montant, 2)
    # # CURRENCY EXCHANGE
    # # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/86fd92bcca154241892eb414/latest/USD'
    # # Making our request
    # response = requests.get(url)
    # data = response.json()
    # if obj.monnaie == 'EUR':
    #     obj.montant_globale = round(montant * float(data['conversion_rates']['EUR']), 2)
    # else:
    #     obj.montant_globale = round(montant, 2)
    dzd_exch = EXCHANGE.objects.exclude(status='actual').filter(date_begin__lte = obj.date_arrivee, date_end__gte = obj.date_arrivee).first()
    if dzd_exch is None:
        dzd_exch = EXCHANGE.objects.get(status='actual')
    if obj.monnaie == 'USD':
        obj.montant_globale = round(montant, 2)
        obj.dzd = round(obj.montant_globale * float(dzd_exch.dzd), 2)
        obj.eur = round(obj.montant_globale * float(dzd_exch.eur), 2)
    elif obj.monnaie == 'EUR':
        obj.eur = round(montant, 2)
        obj.montant_globale = round(obj.eur / float(dzd_exch.eur), 2)
        obj.dzd = round(obj.montant_globale * float(dzd_exch.dzd), 2)
    else:
        obj.dzd = round(montant, 2)
        obj.montant_globale = round(obj.eur / float(dzd_exch.dzd), 2)
        obj.eur = round(obj.montant_globale * float(dzd_exch.eur), 2)
    obj.save()
    # MAJ DU SOLDE DE LA COMPAGNIE
    comp = COMP_DISPATCHER.objects.get(company_dispatcher=obj.compagnie_dispatcher)
    if comp.activite == 'OCCASIONNEL':
        comp.solde -= round(obj.montant_globale, 2)
        comp.save()
    messages.success(request, 'Facturation effectué avec succès.')
    if request.user.profile.poste == 'CHEF D\'ESCALE':
        if comp.activite == 'OCCASIONNEL':
            act = 'occas'
        else:
            act = 'contrat'
        return redirect(reverse('core:agent-summary', kwargs = {
            'activite' : act
        }))
    else:
        return HttpResponseRedirect(reverse('core:flight-detail', kwargs={
            'slug': obj.slug
        }))

class CompaniesSummary(ListView):
    model = COMP_DISPATCHER
    template_name = 'core/gestion_companies.html'
    ordering = ['company_dispatcher']

    def get_context_data(self, *args,**kwargs):
        context = super(CompaniesSummary, self).get_context_data(*args, **kwargs)
        context['title'] = 'COMPAGNIES EN ACCORD AVEC AIR ALGERIE'
        context['back'] = "{% url 'core:home-view' %}"
        return context

def add_company(request):
    context = {
        'title' : "AJOUT D'UNE NOUVELLE COMPAGNIE",
        'monnaie' : BLANK_CHOICE_DASH + MONNAIE,
        'activite' : BLANK_CHOICE_DASH + ['OCCASIONNEL', 'CONTRACTUEL'],
        'back' : "{% url 'core:home-view' %}"
    }
    return render(request, 'core/add_company.html', context)

class ValidNewCompany(View):
    def post(self, request):
        dic = dict(request.POST)
        del dic['csrfmiddlewaretoken']
        dic_values = dic.items()
        for key, value in dic_values:
            if value[0] == '---------' or value[0] == '':
                dic[key] = None
            else:
                dic[key] = value[0].upper()
        print(dic)
        created = False
        try:
            obj = COMP_DISPATCHER.objects.get(company_dispatcher=request.POST.get('company_dispatcher'))
        except COMP_DISPATCHER.DoesNotExist:
            obj, created = COMP_DISPATCHER.objects.get_or_create(
                company_dispatcher=request.POST.get('company_dispatcher'),
                defaults = dic
            )
        if created:
            if obj.activite == 'OCCASIONNEL':
                obj.solde_estimee = 0
            obj.slug = slugify(obj.company_dispatcher.lower().replace(' ', ''))
            messages.success(request, 'La compagnie a été ajoutée avec succès')
        else:
            # COMP_DISPATCHER.objects.filter(company_dispatcher=request.POST.get('company_dispatcher')).delete()
            old_solde = obj.solde
            date_old_solde = obj.solde_date
            obj, created = COMP_DISPATCHER.objects.update_or_create(
                company_dispatcher=request.POST.get('company_dispatcher'),
                defaults = dic,
            )
            hist_comp = HISTORIQUE_OP_COMPANY.objects.create(
                company = obj,
                old_solde = old_solde,
                date_old_solde = date_old_solde,
                new_solde = obj.solde,
                date_new_solde = obj.solde_date,
                user_add = request.user
            )
            hist_comp.save()
            messages.success(request, 'La compagnie a été modifié avec succès')
        obj.solde_last_edit = timezone.now()
        obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
        # voir si ajouter vol new compagnie idrect possible ou pas
        obj.save()
        return redirect('core:home-view')

@login_required
def valid_new_company_name(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                obj = COMP_DISPATCHER.objects.get(company_dispatcher=request.POST.get('company_dispatcher').upper())
            except COMP_DISPATCHER.DoesNotExist:
                obj = False
            if obj:
                data = {
                    'exs' : True,
                    'status': 'alert-danger',
                }
            else:
                data = {
                    'exs' : False,
                    'status': 'alert-success',
                }
            return JsonResponse(data)

class CompanyDetail(DetailView):
    model = COMP_DISPATCHER
    template_name = 'core/add_company.html'

    def get_context_data(self, *args,**kwargs):
        context = super(CompanyDetail, self).get_context_data(*args, **kwargs)
        context['title'] = 'détail de la compagnie'.upper()
        context['obj'] = COMP_DISPATCHER.objects.get(slug = self.kwargs['slug'])
        # context['flight_fi'] = FLIGHT_FI.objects.only('key_flt')
        return context

def price_list_actual(request):
    context = {
        'obj': TARIF_OCCAS.objects.get(status='actual'),
        'title': 'LA PRICE LIST DES VOLS OCCASIONNELS      —    ' + str(timezone.now().year),
        'hist': True,
    }
    return render(request, 'core/price_list.html', context)

class price_list(DetailView):
    model = TARIF_OCCAS
    template_name = 'core/price_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(price_list, self).get_context_data(*args, **kwargs)
        context['obj'] = TARIF_OCCAS.objects.get(auto_id = self.kwargs['pk'])
        context['title'] = 'LA PRICE LIST DES VOLS OCCASIONNELS      —    ' + str(timezone.now().year)
        return context

class ValidPriceList(View):
    def post(self, request):
        dic = dict(request.POST)
        del dic['csrfmiddlewaretoken']
        dic_values = dic.items()
        for key, value in dic_values:
            dic[key] = value[0]
        old_obj = TARIF_OCCAS.objects.get(status = 'actual')
        old_obj.status = None
        old_obj.save()
        obj = TARIF_OCCAS(**dic)
        obj.status = 'actual'
        obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
        obj.save()
        messages.success(request, 'La price list a été modifié avec succès')
        return redirect('core:home-view')

class FichesTouchee(ListView):
    template_name = 'core/fiches_touchee.html'
    ordering = ['n_fiche']

    def get_context_data(self, *args,**kwargs):
        context = super(FichesTouchee, self).get_context_data(*args, **kwargs)
        context['title'] = 'GESTION DES FICHES DE TOUCHéeS'.upper()
        return context
    
    def get_queryset(self):
        return FICHE_TOUCHEE.objects.all().order_by('escale', 'n_fiche')

def gestion_affect_fiches(request):
    max_fiche = list(FICHE_TOUCHEE.objects.aggregate(Max('n_fiche')).values())
    last_affected = list(FICHE_TOUCHEE.objects.filter(escale__isnull = True).aggregate(Min('n_fiche')).values())
    max_fiches = list(FICHE_TOUCHEE.objects.aggregate(Max('n_fiche')).values())[0]
    print(last_affected[0])
    context = {
        'title': 'GESTION DES FICHES',
        'max_fiche' : max_fiche[0],
        'next_fiche': max_fiche[0] + 1,
        'escales' : BLANK_CHOICE_DASH + list(ESCALES.objects.all()),
        'last_affected': last_affected[0],
        'max' : max_fiches,
        'causes' : causes
    }
    return render(request, 'core/gestion_fiches.html', context)

class AddQuota(View):
    def post(self, request):
        if request.POST.get('n_fiche_touchee_2') != '':
            # print(request.POST.get('n_fiche_touchee_1'))
            fiche_2 = int(request.POST.get('n_fiche_touchee_2'))
            fiche_1 = int(request.POST.get('n_fiche_touchee_1'))
            for n_fiche in range(fiche_1, fiche_2 + 1):
                f = FICHE_TOUCHEE.objects.create(
                    n_fiche=n_fiche,
                    key_flt=None,
                    escale=None,
                    status='New',
                    cnl_cause_fiche=None
                )
                f.save()
            hist = HISTORIQUE_ADD_QUOTA.objects.create(
                fiches_from=fiche_1,
                fiches_until=fiche_2
            )
            hist.save()
            messages.success(request, 'Quota ajouté avec succès !')
            return redirect('core:gestion-fiches')

def valid_affect_quota(request):
    get = False
    msg = ''
    if request.POST.get('n_fiche_touchee_2') != '':
        fiche_2 = int(request.POST.get('n_fiche_touchee_2'))
        fiche_1 = int(request.POST.get('n_fiche_touchee_1'))
        max_fiche = list(FICHE_TOUCHEE.objects.aggregate(Max('n_fiche')).values())[0]
        if fiche_2 <= fiche_1:
            get = True
            msg = 'Les fiches doivent êtres indiquées à partir du plus petit jusqu\'au plus grand !'
        if fiche_2 > max_fiche:
            get = True
            msg = 'La dernière fiche disponible est la N° ' + str(max_fiche) + ' !'
    data = {
        'exist' : get,
        'msg': msg
    }
    return JsonResponse(data)

def valid_cnl_fiche(request):
    get = False
    msg = ''
    bg = False
    until = False
    max_fiche = list(FICHE_TOUCHEE.objects.aggregate(Max('n_fiche')).values())[0]
    min_fiche = list(FICHE_TOUCHEE.objects.aggregate(Min('n_fiche')).values())[0]
    if request.POST.get('n_fiche_touchee_2') != '':
        until = True
        fiche_2 = int(request.POST.get('n_fiche_touchee_2'))
        fiche_1 = int(request.POST.get('n_fiche_touchee_1'))
        try:
            f = FICHE_TOUCHEE.objects.get(n_fiche=fiche_2)
        except FICHE_TOUCHEE.DoesNotExist:
            get = True
            msg = 'La fiche ' + str(fiche_2) + ' n\'existe pas !'
            data = {
                'exist' : get,
                'msg': msg
            }
            return JsonResponse(data)

        if f.status == 'New':
            pass
        else:
            get = True
            msg = 'La fiche N° ' + str(fiche_2) + ' a déjà été consommée / annulée !'
            data = {
                'exist' : get,
                'msg': msg
            }
            return JsonResponse(data)
        if fiche_1 < min_fiche or fiche_2 < min_fiche:
            get = True
            msg = 'Les fiches doivent commencer à partir de la fiche N°' + str(min_fiche) + ' !'
        if fiche_1 > max_fiche or fiche_2 > max_fiche:
            get = True
            msg = 'La dernière fiche disponible est la N° ' + str(max_fiche) + ' !'
        if fiche_2 <= fiche_1:
            get = True
            msg = 'Les fiches doivent êtres indiquées à partir du plus petit jusqu\'au plus grand !'
    print('XXX')
    if request.POST.get('n_fiche_touchee_1') != '':
        bg = True
        fiche_1 = int(request.POST.get('n_fiche_touchee_1'))
        if fiche_1 < min_fiche:
            get = True
            msg = 'Les fiches doivent commencer à partir de la fiche N°' + str(min_fiche) + ' !'
        if fiche_1 > max_fiche:
            get = True
            msg = 'La dernière fiche disponible est la N° ' + str(max_fiche) + ' !'
        try:
            f = FICHE_TOUCHEE.objects.get(n_fiche=fiche_1)
        except FICHE_TOUCHEE.DoesNotExist:
            get = True
            msg = 'La fiche ' + str(fiche_1) + ' n\'existe pas !'
            data = {
                'exist' : get,
                'msg': msg
            }
            return JsonResponse(data)
        if f.status == 'New':
            pass
        else:
            get = True
            msg = 'La fiche N° ' + str(fiche_1) + ' a déjà été consommée / annulée !'
            data = {
                'exist' : get,
                'msg': msg
            }
            return JsonResponse(data)
    print(bg, until)
    if bg and until:
        print('IINN')
        for fiche in range(fiche_1, fiche_2 + 1):
            f = FICHE_TOUCHEE.objects.get(n_fiche=fiche)
            print(f.status)
            if f.status == 'New':
                pass
            else:
                get = True
                msg = 'La fiche N° ' + str(fiche) + ' a déjà été ' + f.status + ' !'
                break
    data = {
        'exist' : get,
        'msg': msg
    }
    return JsonResponse(data)

def valid_escale(request):
    get = False
    msg = ''
    tot = 0
    remain = 0
    esc = ''
    if request.POST.get('escale') != "('', '---------')":
        escale = request.POST.get('escale')
        tot = FICHE_TOUCHEE.objects.filter(escale=escale).count()
        remain = FICHE_TOUCHEE.objects.filter(escale=escale, status='New').count()
        get = True
    data = {
        'exist' : get,
        'msg': msg,
        'tot': tot,
        'remain': remain,
        'esc': esc
    }
    return JsonResponse(data)

class HistQuota(ListView):
    template_name = 'core/hist_quota.html'
    model = HISTORIQUE_ADD_QUOTA
    paginate_by = 30
    ordering = ['-date_last_add']

    def get_context_data(self, *args,**kwargs):
        context = super(HistQuota, self).get_context_data(*args, **kwargs)
        context['title'] = 'HISTORIQUE DES AJOUTS DES FICHES'.upper()
        return context

class AffectQuota(View):
    def post(self, request):
        if request.POST.get('n_fiche_touchee_2') != '':
            fiche_2 = int(request.POST.get('n_fiche_2'))
            fiche_1 = int(request.POST.get('n_fiche_1'))
            escale = request.POST.get('escale')
            for fiche in range(fiche_1, fiche_2 + 1):
                f = FICHE_TOUCHEE.objects.get(n_fiche=fiche)
                esc = ESCALES.objects.get(escale=escale)
                f.escale = esc
                f.escale.escale = escale
                f.save()
            hist = HISTORIQUE_AFFECT_QUOTA.objects.create(
                fiches_from=fiche_1,
                fiches_until=fiche_2,
                escale=esc
            )
            hist.save()
            messages.success(request, 'Affectation effectué avec succès !')
            return redirect('core:gestion-fiches')

class HistAffect(ListView):
    template_name = 'core/hist_affect.html'
    model = HISTORIQUE_AFFECT_QUOTA
    paginate_by = 30
    ordering = ['-date_last_add']

    def get_context_data(self, *args,**kwargs):
        context = super(HistAffect, self).get_context_data(*args, **kwargs)
        context['title'] = 'HISTORIQUE DES AFFECTATIONS DES FICHES'.upper()
        return context

class CNLFiches(View):
    def post(self, request):
        print(request.POST)
        fiche_1 = int(request.POST.get('n_fiche_touchee_1'))
        if request.POST.get('n_fiche_touchee_2') != '':
            fiche_2 = int(request.POST.get('n_fiche_touchee_2'))
        else:
            fiche_2 = fiche_1
        for fiche in range(fiche_1, fiche_2 + 1):
            f = FICHE_TOUCHEE.objects.get(n_fiche=fiche)
            f.status = 'ANNULE'
            f.cnl_cause_fiche = request.POST.get('cnl_cause_fiche')
            f.save()
        if fiche_2 == fiche_1:
            fiche_2 = None
        hist = HISTORIQUE_CNL_FICHES.objects.create(
            fiches_from=fiche_1,
            fiches_until=fiche_2,
            cause=request.POST.get('cnl_cause_fiche'),
            obs=request.POST.get('obs')
        )
        hist.save()
        messages.success(request, 'Annulation effectué avec succès !')
        return redirect('core:gestion-fiches')

class HistCNL(ListView):
    template_name = 'core/hist_cnl.html'
    model = HISTORIQUE_CNL_FICHES
    paginate_by = 30
    ordering = ['-date_last_cnl']

    def get_context_data(self, *args,**kwargs):
        context = super(HistCNL, self).get_context_data(*args, **kwargs)
        context['title'] = 'HISTORIQUE DES ANNULATIONS DES FICHES'.upper()
        return context

def add_schedule(request):
    context = {
        'title' : "AJOUT D'UN PROGRAMME DES VOLS (CONTRACTUEL) - SCHEDULE".upper(),
        'company': BLANK_CHOICE_DASH + list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL'))
    }
    return render(request, 'core/add_schedule.html', context)

class NewSchedule(View):
    def post(self, request):
        if request.FILES['file_pg']:
            myfile = request.FILES['file_pg']
            try:
                comp = COMP_DISPATCHER.objects.get(company_dispatcher = request.POST.get('compagnie_dispatcher'))
                monnaie = comp.monnaie
                escales = list(ESCALES.objects.all().values_list('escale', flat=True))
                n_max = list(FLIGHT_ASSIST.objects.aggregate(Max('n_field')).values())[0]
                df_out = pd.DataFrame()
                new_df = pd.DataFrame()
                df = ssim_df(myfile)
                # df.to_csv('myfile.csv')
                # df = pd.read_csv('myfile.csv')
                # GET ONLY DZ
                df = df.loc[(df['Departure_Station'].isin(escales)) | (df['Arrival_Station'].isin(escales))]
                # GET DATE DEMANDE FROM SSIM_PERIOD COLUMN
                row = df.loc[0]
                date_dem = row['ssim_period'][:2] + '-' + row['ssim_period'][2:5] + '-20' + row['ssim_period'][5:7]
                date_dem = datetime.datetime.strptime(date_dem, '%d-%b-%Y').date()
                df.sort_values(by=['fly_date', 'Flight_Number', 'STD_UTC'], inplace = True)
                uniq_date = df['fly_date'].unique()
                df['next_idx'] = 'x'
                df_out = df
                # print(df_out[['KEY_FLT', 'Flight_Number', 'Departure_Station', 'Arrival_Station', 'STD_UTC', 'STA_UTC', 'fly_date', 'next_idx']])
                for idx, row_copy in df.iterrows():
                    row = df_out.loc[idx]
                    if row.next_idx is not None:
                        print(df_out['Departure_Station'].values)
                        print('\n')
                        print(row['Arrival_Station'])
                        oneline_df = df_out.loc[ (df_out['next_idx'].values == 'x') & (idx != df_out.index[-1]) & (df_out['Departure_Station'].values == row['Arrival_Station']) & (df_out['Flight_Number'].str[0:3] == row['Flight_Number'][0:3]) & (df_out['STD_UTC'].astype(int).values > int(row['STD_UTC'])) ]
                        if oneline_df.shape[0] > 0:
                            for oneline_idx, oneline_row in oneline_df.iterrows():
                                row_2 = oneline_row
                                break
                            df_out.loc[idx, 'next_idx'] = row_2['KEY_FLT']
                            df_out.loc[oneline_idx, 'next_idx'] = None
                            # DEFINE ARRIVE AND DEPART FLIGHT
                            if int(row['STD_UTC']) < int(row_2['STD_UTC']):
                                arr_row = row
                                dep_row = row_2
                            else:
                                dep_row = row
                                arr_row = row_2
                            # GET CAPACITE
                            cap = re.findall('[A-Z](\d+)', str(arr_row['Aircraft_Configuration']))
                            cap = [int(i) for i in cap]
                            capacite = sum(cap)
                            # GET KEY FLIGHT - KEY_FLT 211204
                            date_arr = str(arr_row['arrival_date'])
                            date_arr = date_arr.replace('-', '')
                            date_arr = date_arr[2:]
                            # x = re.search("20(\d{2})", date_arr.replace('-', ''))
                            # date_arr = date_arr.replace('-', '').replace('2021', '21')
                            date_arr = date_arr[4:] + date_arr[2:4] + date_arr[:2]
                            try:
                                arr_row['Flight_Number'] = str(int(arr_row['Flight_Number']))
                                if len(arr_row['Flight_Number']) < 4:
                                    arr_row['Flight_Number'] = '0' + str(arr_row['Flight_Number'])
                            except ValueError:
                                arr_row['Flight_Number'] = arr_row['Flight_Number'].replace('-', '')
                            key_flt = date_arr + arr_row['Flight_Number'].replace('-', '') + arr_row['Arrival_Station'] + arr_row['Departure_Station']
                            # CONVERT TIME
                            sta = '0' + str(arr_row['STA_UTC']) if len(str(arr_row['STA_UTC'])) < 4 else str(arr_row['STA_UTC'])
                            sta = datetime.datetime.strptime(sta[0:2] + ':' + sta[2:4], '%H:%M').time()
                            std = '0' + str(dep_row['STD_UTC']) if len(str(dep_row['STD_UTC'])) < 4 else str(dep_row['STD_UTC'])
                            std = datetime.datetime.strptime(std[0:2] + ':' + std[2:4], '%H:%M').time()
                            values_to_add = {
                                'KEY_FLT': key_flt,
                                'DATE DEMANDE': date_dem,
                                'ETAT DU VOL' : 'New',
                                'DATE CNL': None,
                                'HEURE CNL': None,
                                'CNL / ETA': None,
                                'OBS': None,
                                'MONNAIE': monnaie,
                                'ESCALE (IATA)': arr_row['Arrival_Station'],
                                'DATE ARRIVEE': arr_row['arrival_date'],
                                'ACT DTE ARR': None,
                                'PROV': arr_row['Departure_Station'],
                                'N° VOL ARRIV': arr_row['Flight_Number'],
                                'STA': sta,
                                'ATA': None,
                                'PAX ARRIV': 0,
                                'CARGO ARRIV': 0,
                                'DATE DEPART': dep_row['fly_date'],
                                'ACT DTE DEP': None,
                                'DEST': dep_row['Arrival_Station'],
                                'N° VOL DEP': dep_row['Flight_Number'],
                                'STD': std,
                                'ATD': None,
                                'PAX DEP': 0,
                                'CARGO DEP': 0,
                                'COMPAGNIE DISPATCHER': comp.company_dispatcher,
                                'N° FICHE TOUCHEE': None,
                                'NATURE TOUCHEE': None,
                                'OPERATEUR': None,
                                'TYPE AVION': arr_row['Aircraft_Type'],
                                'MODE PAIEMENT': 'CONTRAT',
                                'CAPACITE': int(capacite),
                                'slug': key_flt.lower()
                            }
                            row_to_add = pd.Series(values_to_add)
                            new_df = new_df.append(row_to_add, ignore_index = True)
                # print(df_out[['KEY_FLT', 'Flight_Number', 'Departure_Station', 'Arrival_Station', 'STD_UTC', 'STA_UTC', 'fly_date', 'next_idx']])
                new_df.insert(1, 'N°', range(n_max + 1, n_max + len(new_df) + 1))
                engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
                new_df.to_sql('FLIGHT_ASSIST', engine, if_exists='append', index=False)
                # new_df.to_csv('new_prog.csv', index = False)
                # pd.set_option('display.max_rows', len(df))
                messages.success(request, "Le programme a été chargé avec succès !")
                return redirect('core:add-schedule')
            except pd.errors.ParserError:
                messages.error(request, "Le fichier renseigné n'est pas valide / n'est pas au format IATA !")
                return redirect('core:add-schedule')
            # print(df.head())
            # print(myfile.name, myfile.size)

class FactRegular(ListView):
    template_name = 'core/fact_regular.html'

    def get_context_data(self, *args,**kwargs):
        context = super(FactRegular, self).get_context_data(*args, **kwargs)
        context['title'] = 'Facturation des vols réguliers'.upper()
        qs = self.get_queryset()
        context['qs_count'] = qs.count()
        context['companies'] = BLANK_CHOICE_DASH + list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').order_by('company_dispatcher'))
        context['escales'] = BLANK_CHOICE_DASH + list(ESCALES.objects.all().order_by('full_name'))
        if 'from_date' in self.request.GET:
            context['from_date'] = datetime.datetime.strptime(self.request.GET.get('from_date'), '%Y-%m-%d').date()
            context['until_date'] = datetime.datetime.strptime(self.request.GET.get('until_date'), '%Y-%m-%d').date()
            context['company'] = self.request.GET.get('compagnie_dispatcher')
            comp = COMP_DISPATCHER.objects.get(company_dispatcher = context['company'])
            context['esc'] = ESCALES.objects.get(escale = self.request.GET.get('escale')).full_name
            context['title'] = 'Facturation - COMPAGNIE : '.upper() + comp.company_dispatcher
            # GENERATION DU FICHIER EXCEL
            # df = read_frame(qs)
            # df.to_excel(context['esc'] + '_' + context['company'] + '_' + self.request.GET.get('from_date').replace('-', '') + '_' + self.request.GET.get('until_date').replace('-', '') + '.xlsx', index = False)
            # context['file'] = open(context['esc'] + '_' + context['company'] + '_' + self.request.GET.get('from_date').replace('-', '') + '_' + self.request.GET.get('until_date').replace('-', '') + '.xlsx', 'r', encoding='utf-8')
            # print(context['file'].name, context['file'])
            context['monnaie'] = comp.monnaie
        return context
    
    def get_queryset(self):
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher = self.request.GET.get('compagnie_dispatcher'), act_dte_arr__isnull = False, escale = self.request.GET.get('escale')).order_by('act_dte_arr')
        qs_fin = qs
        if self.request.method == 'GET':
            if 'from_date' in self.request.GET:
                from_date = datetime.datetime.strptime(self.request.GET.get('from_date'), '%Y-%m-%d').date()
            else:
                from_date = None
            if 'until_date' in self.request.GET:
                until_date = datetime.datetime.strptime(self.request.GET.get('until_date'), '%Y-%m-%d').date()
            else:
                until_date = None
            if from_date is not None and until_date is not None:
                qs_fin = qs.filter(act_dte_arr__gte = from_date, act_dte_arr__lte = until_date)
        return qs_fin

@login_required
def valid_company_fact(request):
    if request.is_ajax():
        if request.method == 'POST':
            date = False
            get = False
            msg = ''
            date_from = ''
            date_until = ''
            qs = ''
            last_date_from = ''
            last_date_until = ''
            from_bool = False
            until_bool = False
            comp = request.POST.get('compagnie_dispatcher')
            esc = ESCALES.objects.get(escale=request.POST.get('escale'))
            if 'compagnie_dispatcher' in request.POST and request.POST.get('compagnie_dispatcher') != 'all':
                comp_obj = COMP_DISPATCHER.objects.get(company_dispatcher = request.POST.get('compagnie_dispatcher'))
            if request.POST.get('compagnie_dispatcher') != 'all':
                try:
                    last_date_from = HISTORIQUE_REGULAR_FACT.objects.filter(company=request.POST.get('compagnie_dispatcher'), escale=esc).latest('date_last_add').from_date.strftime('%d/%m/%Y')
                    last_date_until = HISTORIQUE_REGULAR_FACT.objects.filter(company=request.POST.get('compagnie_dispatcher'), escale=esc).latest('date_last_add').until_date.strftime('%d/%m/%Y')
                except HISTORIQUE_REGULAR_FACT.DoesNotExist:
                    get = True
                    msg = 'Aucune facturation n\'a déjà été effectué pour ' + request.POST.get('compagnie_dispatcher').upper() + ' pour l\'escale ' + esc.full_name.upper()
                    data = {
                        'exist' : get,
                        'msg': msg,
                        'date_from': last_date_from,
                        'date_until': last_date_until,
                        'comp': comp,
                        'esc': esc.escale,
                        'status': 'warning'
                    }
                    return JsonResponse(data)
                try:
                    qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher = request.POST.get('compagnie_dispatcher'), act_dte_arr__isnull = False)
                except FLIGHT_ASSIST.DoesNotExist:
                    get = True
                    msg = 'Aucun vol n\'a été opéré pour ' + request.POST.get('compagnie_dispatcher').upper()
                    data = {
                        'exist' : get,
                        'msg': msg,
                        'date_from': last_date_from,
                        'date_until': last_date_until,
                        'comp': comp,
                        'esc': esc.escale
                    }
                    return JsonResponse(data)
                if 'from_date' in request.POST and request.POST.get('from_date') != '':
                    from_bool = True
                    from_date = datetime.datetime.strptime(request.POST.get('from_date'), '%Y-%m-%d').date()
                    if from_date >= datetime.datetime.now().date():
                        get = True
                        msg = 'La date doit être une date antérieure !'
                        data = {
                            'exist' : get,
                            'msg': msg,
                            'date_from': last_date_from,
                            'date_until': last_date_until,
                            'comp': comp,
                            'esc': esc.escale
                        }
                        return JsonResponse(data)
                if 'until_date' in request.POST and request.POST.get('until_date') != '':
                    until_bool = True
                    until_date = datetime.datetime.strptime(request.POST.get('until_date'), '%Y-%m-%d').date()
                    if until_date >= datetime.datetime.now().date():
                        get = True
                        msg = 'La date doit être une date antérieure !'
                        data = {
                            'exist' : get,
                            'msg': msg,
                            'date_from': last_date_from,
                            'date_until': last_date_until,
                            'comp': comp,
                            'esc': esc.escale
                        }
                        return JsonResponse(data)
                if until_bool and from_bool:
                    date = True
                    if from_date == until_date or until_date < from_date:
                        get = True
                        msg = 'La date limite doit être supérieur à la date de début !'
                        data = {
                            'exist' : get,
                            'msg': msg,
                            'date_from': last_date_from,
                            'date_until': last_date_until,
                            'comp': comp,
                            'esc': esc.escale
                        }
                        return JsonResponse(data)
                    qs = qs.filter(act_dte_arr__gte = from_date, act_dte_arr__lte = until_date)
                    if qs.count() == 0:
                        get = True
                        msg = 'Aucun vol effectué à cette periode !'
                        data = {
                            'exist' : get,
                            'msg': msg,
                            'date_from': last_date_from,
                            'date_until': last_date_until,
                            'comp': comp,
                            'esc': esc.escale
                        }
                        return JsonResponse(data)
                    hist_qs = HISTORIQUE_REGULAR_FACT.objects.filter(escale=esc, company=comp_obj).filter( (Q(from_date__lte = from_date) & Q(until_date__gte = from_date)) | (Q(from_date__lte = until_date) & Q(until_date__gte = until_date)) )
                    print(hist_qs.count())
                    if hist_qs.count() > 0:
                        get = True
                        msg = 'Une partie des vols concernés (ou tous) ont déjà été facturés pour la compagnie ' + comp + ' à l\'escale ' + esc.escale + ' !'
                        data = {
                            'exist' : get,
                            'msg': msg,
                            'date_from': last_date_from,
                            'date_until': last_date_until,
                            'comp': comp,
                            'esc': esc.escale,
                            'status': 'warning'
                        }
                        return JsonResponse(data)
            else:
                msg = 'XXX'
            data = {
                'exist' : get,
                'msg': msg,
                'date_from': last_date_from,
                'date_until': last_date_until,
                'comp': comp,
                'esc': esc.escale
            }
            return JsonResponse(data)

def number_format(value_int):
    value = ''
    if value_int >= 1000000:
            value = "%.0f%s" % (value_int/1000000.00, ' M')
    else:
        if value_int >= 1000:
            value = "%.0f%s" % (value_int/1000.0, ' K')
        else:
            value = str(value_int)
    return value
         
def dashboard(request):
    years = []
    months = []
    current_year = datetime.date.today().year
    for year in range(2019, current_year+1):
        years.append(year)
    for month in range(1, 13):
        months.append(month)
    context = {
        'title' : "VOLET STATISTIQUE".upper(),
        'companies': BLANK_CHOICE_DASH + ['TOUTES'] + list(COMP_DISPATCHER.objects.filter()),
        'escales': BLANK_CHOICE_DASH + list(ESCALES.objects.all()),
        'years': BLANK_CHOICE_DASH + list(years),
        'months': BLANK_CHOICE_DASH + list(months),
        'acts' : BLANK_CHOICE_DASH + ['OCCASIONNEL', 'Régulier'.upper()],
    }
    return render(request, 'core/dashboard.html', context)           

def refresh_template_cxt(request, year, month):
    qs = FLIGHT_ASSIST.objects.filter(act_dte_arr__isnull = False)
    qs_sum = qs.filter(montant_globale__isnull = False)
    qs_sum = qs_sum.filter(Q(act_dte_arr__year = year) | Q(date_cnl__year = year))
    if month is not None:
        qs_sum = qs_sum.filter(Q(act_dte_arr__month = month) | Q(date_cnl__month = month))
    qs_sum_prec = qs.filter(montant_globale__isnull = False)
    qs_sum_prec = qs_sum_prec.filter(Q(act_dte_arr__year = year - 1) | Q(date_cnl__year = year - 1))
    if month is not None:
        qs_sum_prec = qs_sum_prec.filter(Q(act_dte_arr__month = month) | Q(date_cnl__month = month))
    comp = COMP_DISPATCHER.objects.filter(activite='OCCASIONNEL').values_list('company_dispatcher')
    qs_occas = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = comp, montant_globale__isnull = False)
    if year is not None:
        qs_occas = qs_occas.filter(Q(act_dte_arr__year = year) | Q(date_cnl__year = year))
    if month is not None:
        qs_occas = qs_occas.filter(Q(act_dte_arr__month = month) | Q(date_cnl__month = month))
    qs_est = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = True, montant_prevus__isnull = False, date_arrivee__year = year)
    if month is not None:
        qs_est = qs_est.filter(date_arrivee__month = month)
    if qs_sum.count() == 0:
        sum_mont = 0
    else:
        sum_mont = round(qs_sum.aggregate(Sum('montant_globale')).get('montant_globale__sum'))
    if qs_est.count() == 0:
        sum_est = 0
    else:
        sum_est = round(qs_est.aggregate(Sum('montant_prevus')).get('montant_prevus__sum'))
    if qs_sum_prec.count() == 0:
        sum_prec = 0
    else:
        sum_prec = qs_sum_prec.aggregate(Sum('montant_globale')).get('montant_globale__sum')
    if qs_occas.count() == 0:
        sum_occas = 0
        print(sum_occas)
    else:
        sum_occas = qs_occas.aggregate(Sum('montant_globale')).get('montant_globale__sum')
    # sum_prec = 450000
    if sum_prec is None or sum_prec == 0:
        act = None
        perc = None
    else:
        perc = (100 - (round(sum_mont / sum_prec, 2) * 100)) * (-1)
        if perc:
            act = 'down'
        else:
            act = 'up'
    context = {
        'perc': str(perc).replace('-', ''),
        'act': act,
        'qs_occas': qs_occas.count(),
        'sum_qs_occas': number_format(sum_occas),
        'sum_mont': number_format(sum_mont),
        'sum_est': number_format(sum_est),
        'current_year': year,
    }
    return context

def Dash(request):
    years = []
    months = []
    current_year = datetime.date.today().year
    for year in range(2019, current_year+1):
        years.append(year)
    for month in range(1, 13):
        months.append(month)
    if 'escale' in request.POST:
        escale = request.POST.get('escale')
    else:
        escale = 'ALG'
        activite = 'all'
    context = {
        'title': 'Data Analytics ( Département contrats et assistance au sol )'.upper(),
        'escale': escale,
        'activite': activite,
        'companies': ['TOUTES'] + list(COMP_DISPATCHER.objects.filter()),
        'escales': list(ESCALES.objects.all()),
        'years': list(years),
        'months': BLANK_CHOICE_DASH + list(months),
        'acts' : BLANK_CHOICE_DASH + ['OCCASIONNEL', 'Régulier'.upper()],
    }
    ctxt = refresh_template_cxt(request, int(datetime.datetime.now().year), None)
    context.update(ctxt)
    return render(request, 'core/dashboard-cas.html', context)

def cas_build_pie_chart(request):
    if request.is_ajax():
        if request.method == 'POST':
            # print(request.POST)
            escale = request.POST.get('escale')
            act = request.POST.get('activite') 
            if request.POST.get('escale') == '':
                escale = 'ALG'
            qs = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = False, escale = escale)
            year = int(request.POST.get('year'))
            qs = qs.filter(Q(act_dte_arr__year = year) | Q(date_cnl__year = year))
            if request.POST.get('month') != "('', '---------')":
                month = int(request.POST.get('month'))
                qs = qs.filter(Q(act_dte_arr__month = month) | Q(date_cnl__month = month))
            else:
                month = None
            if act == 'all':
                comps = COMP_DISPATCHER.objects.all().values_list('company_dispatcher', flat=True).distinct()
            elif act == 'occas':
                comps = COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL').values_list('company_dispatcher', flat=True).distinct()
            else:
                comps = COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').values_list('company_dispatcher', flat=True).distinct()
            comps = list(comps)
            qs_montant = []
            for company in comps:
                subqs = qs.filter(compagnie_dispatcher = company).aggregate(Sum('montant_globale')).get('montant_globale__sum')
                if subqs is not None:
                    subqs = round(subqs, 2)
                    qs_montant.append({company:subqs})
            qs_montant = sorted(qs_montant, key=lambda k: list(k.values()), reverse=True) 
            if len(qs_montant) > 10:
                qs_montant = qs_montant[:10]
            ctx = refresh_template_cxt(request, year, month)
            data = {
                'exist': True,
                'title': 'Montant par compagnie - Escale : ' + escale + ' ( Top 10 )',
                'data': qs_montant
            }
            data.update(ctx)
            return JsonResponse(data, safe=False)

def build_chart(request):
    if request.is_ajax():
        if request.method == 'POST':
            # print(request.POST)
            qs = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = False)
            year = int(request.POST.get('year'))
            qs = qs.filter(Q(act_dte_arr__year = year) | Q(date_cnl__year = year))
            if request.POST.get('month') != "('', '---------')":
                month = int(request.POST.get('month'))
                qs = qs.filter(Q(act_dte_arr__month = month) | Q(date_cnl__month = month))
            else:
                month = None
            if request.POST.get('orient') == 'comp':
                orient = 'compagnie'
                if request.POST.get('activite') == 'all':
                    comps = COMP_DISPATCHER.objects.all().values_list('company_dispatcher', flat=True).distinct()
                elif request.POST.get('activite') == 'occas':
                    orient += ' ( Vols occasionnels )'
                    comps = COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL').values_list('company_dispatcher', flat=True).distinct()
                else:
                    orient += ' ( Vols réguliers )'
                    comps = COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').values_list('company_dispatcher', flat=True).distinct()
                comps = list(comps)
                qs = qs.filter(compagnie_dispatcher__in = comps)
                qs_montant = []
                for company in comps:
                    subqs = qs.filter(compagnie_dispatcher = company).aggregate(Sum('montant_globale')).get('montant_globale__sum')
                    if subqs is not None:
                        subqs = round(subqs, 2)
                        qs_montant.append({company:subqs})
            else:
                orient = 'escale'
                escales = FLIGHT_ASSIST.objects.all().values_list('escale', flat=True).distinct()
                qs_montant = []
                for esc in escales:
                    subqs = qs.filter(escale = esc).aggregate(Sum('montant_globale')).get('montant_globale__sum')
                    if subqs is not None:
                        subqs = round(subqs, 2)
                        qs_montant.append({esc:subqs})
            # REFRESH TEMPLATE
            ctx = refresh_template_cxt(request, year, month)
            data = {
                'exist': True,
                'title': 'Montant par ' + orient,
                'data': qs_montant
            }
            data.update(ctx)
            return JsonResponse(data, safe=False)

def month_name(month_number):
    return calendar.month_name[month_number]

def cas_build_time_chart(request):
    months = []
    for month in range(1, 13):
        months.append(month)
    today = datetime.datetime.now().date()
    year_ago_date = today - datetime.timedelta(days=365)
    qs = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = False)
    qs_bas = qs.filter(Q(act_dte_arr__gte = year_ago_date) | Q(date_cnl__gte = year_ago_date))
    print(qs.count())
    res = []
    year_ago_copy = year_ago_date
    while year_ago_copy <= today:
        qs = qs_bas.filter(Q(act_dte_arr__year = year_ago_copy.year) | Q(date_cnl__year = year_ago_copy.year))
        qs = qs.filter(Q(act_dte_arr__month = year_ago_copy.month) | Q(date_cnl__month = year_ago_copy.month))
        if qs.count() == 0:
            sum_mont = 0
        else:
            sum_mont = qs.aggregate(Sum('montant_globale')).get('montant_globale__sum')
        res.append({month_name(year_ago_copy.month)[:3].upper() + ' ' + str(year_ago_copy.year):round(sum_mont, 2)})
        year_ago_copy += pd.DateOffset(months = 1)
    data = {
        'exist': True,
        'res': res
    }
    return JsonResponse(data, safe=False)

# cas_build_time_chart()

class HistRegularFact(ListView):
    template_name = 'core/hist_regular_fact.html'
    model = HISTORIQUE_REGULAR_FACT

    def get_context_data(self, *args,**kwargs):
        context = super(HistRegularFact, self).get_context_data(*args, **kwargs)
        context['title'] = 'HISTORIQUE DES FACTURATIONS DES COMPAGNIES à VOLS RéGULIERS'.upper()
        context['companies'] = list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL'))
        context['escales'] = list(ESCALES.objects.all())
        context['users'] = list(HISTORIQUE_REGULAR_FACT.objects.all().distinct('user_add'))
        users = []
        for item in context['users']:
            users.append(item.user_add.last_name + ' ' + item.user_add.first_name)
        context['users'] = users
        # QUERYSET
        if self.request.GET.get('company') and self.request.GET.get('company') != 'all':
            context['filter_cmp'] = self.request.GET.get('company')
        if self.request.GET.get('escale') and self.request.GET.get('escale') != 'all':
            context['filter_escale'] = self.request.GET.get('escale')
        if self.request.GET.get('users') and self.request.GET.get('users') != 'all':
            context['filter_users'] = self.request.GET.get('users')
        if self.request.GET.get('from_date') and self.request.GET.get('from_date') != '':
            context['filter_from_date'] = datetime.datetime.strptime(self.request.GET.get('from_date'), '%Y-%m-%d')
        if self.request.GET.get('until_date') and self.request.GET.get('until_date') != '':
            context['filter_until_date'] = datetime.datetime.strptime(self.request.GET.get('until_date'), '%Y-%m-%d')
        if self.request.GET.get('date_last_add_1') and self.request.GET.get('date_last_add_1') != '':
            context['filter_date_last_add_1'] = datetime.datetime.strptime(self.request.GET.get('date_last_add_1'), '%Y-%m-%d')
        if self.request.GET.get('date_last_add_2') and self.request.GET.get('date_last_add_2') != '':
            context['filter_date_last_add_2'] = datetime.datetime.strptime(self.request.GET.get('date_last_add_2'), '%Y-%m-%d')
        return context
    
    def get_queryset(self):
        # QUERYSET
        qs = HISTORIQUE_REGULAR_FACT.objects.all()
        if self.request.GET.get('company') and self.request.GET.get('company') != 'all':
            qs = qs.filter(company = self.request.GET.get('company'))
        if self.request.GET.get('escale') and self.request.GET.get('escale') != 'all':
            qs = qs.filter(escale = self.request.GET.get('escale'))
        if self.request.GET.get('users') and self.request.GET.get('users') != 'all':
            usr = User.objects.get(last_name = self.request.GET.get('users').split(' ')[0], first_name = self.request.GET.get('users').split(' ')[1])
            qs = qs.filter(user_add = usr)
        if self.request.GET.get('from_date') and self.request.GET.get('from_date') != '':
            date_1 = datetime.datetime.strptime(self.request.GET.get('from_date'), '%Y-%m-%d')
        else:
            date_1 = None
        if self.request.GET.get('until_date') and self.request.GET.get('until_date') != '':
            date_2 = datetime.datetime.strptime(self.request.GET.get('until_date'), '%Y-%m-%d')
        else:
            date_2 = None
        if date_1 and date_2:
            qs = qs.filter((Q(from_date__lte = date_1) & Q(until_date__gte = date_1)) | (Q(from_date__lte = date_2) & Q(until_date__gte = date_2)))
        elif date_1 and not date_2:
            qs = qs.filter(from_date__lte = date_1, until_date__gte = date_1)
        elif not date_1 and date_2:
            qs = qs.filter(from_date__lte = date_2, until_date__gte = date_2)
        if self.request.GET.get('date_last_add_1') and self.request.GET.get('date_last_add_1') != '':
            date_1 = datetime.datetime.strptime(self.request.GET.get('date_last_add_1'), '%Y-%m-%d')
        else:
            date_1 = None
        if self.request.GET.get('date_last_add_2') and self.request.GET.get('date_last_add_2') != '':
            date_2 = datetime.datetime.strptime(self.request.GET.get('date_last_add_2'), '%Y-%m-%d')
        else:
            date_2 = None
        if date_1 and date_2:
            qs = qs.filter(date_last_add__gte = date_1, date_last_add__lte = date_2)
        elif date_1 and not date_2:
            qs = qs.filter(date_last_add__date = date_1)
        elif not date_1 and date_2:
            qs = qs.filter(date_last_add__date = date_2)
        return qs.order_by('-date_last_add')
            
class validFactRegular(View):
    def post(self, request):
        # print(request.POST)
        hist_bill = HISTORIQUE_REGULAR_FACT.objects.create(
            escale = ESCALES.objects.get(escale=request.POST.get('escale')),
            company = COMP_DISPATCHER.objects.get(company_dispatcher=request.POST.get('compagnie_dispatcher')),
            user_add = request.user,
            from_date = datetime.datetime.strptime(request.POST.get('from_date'), '%Y-%m-%d'),
            until_date = datetime.datetime.strptime(request.POST.get('until_date'), '%Y-%m-%d'),
            _id = HISTORIQUE_REGULAR_FACT.objects.aggregate(Max('_id')).get('_id__max') + 1,
            slug = slugify(str(HISTORIQUE_REGULAR_FACT.objects.aggregate(Max('_id')).get('_id__max') + 1))
        )
        hist_bill.save()
        messages.success(request, 'Facturation enregistrée avec succès !')
        return HttpResponseRedirect(reverse('core:fact-regular-detail', kwargs={
            'slug': hist_bill.slug
        }))

class FactRegularDetail(DetailView):
    model = HISTORIQUE_REGULAR_FACT
    template_name = 'core/fact_regular_detail.html'

    def get_context_data(self, *args,**kwargs):
        context = super(FactRegularDetail, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        obj = HISTORIQUE_REGULAR_FACT.objects.get(_id = int(self.kwargs['slug']))
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher = obj.company, act_dte_arr__isnull = False, escale = obj.escale.escale).order_by('act_dte_arr')
        qs = qs.filter(act_dte_arr__gte = obj.from_date, act_dte_arr__lte = obj.until_date)
        sum = 0
        if obj.montant is None:
            if obj.company.monnaie == 'EUR':
                for row in qs:
                    sum += row.eur
            elif obj.company.monnaie == 'USD':
                for row in qs:
                    sum += row.montant_globale
            else:
                for row in qs:
                    sum += row.dzd
            obj.montant = round(sum, 2)
            obj.save()
        if obj.type_fact is not None:
            context['type_fact'] = obj.type_fact
        else:
            context['type_fact'] = None
        context['fact'] = obj.n_facture
        context['slug'] = obj.slug
        context['qs_count'] = qs.count()
        context['companies'] = BLANK_CHOICE_DASH + list(COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').order_by('company_dispatcher'))
        context['escales'] = BLANK_CHOICE_DASH + list(ESCALES.objects.all().order_by('full_name'))
        context['from_date'] = obj.from_date
        context['until_date'] = obj.until_date
        context['company'] = obj.company
        comp = COMP_DISPATCHER.objects.get(company_dispatcher = context['company'])
        context['esc'] = obj.escale.full_name
        context['title'] = 'Facturation - COMPAGNIE : '.upper() + comp.company_dispatcher
        context['monnaie'] = comp.monnaie   
        context['object_list'] = qs        
        return context

class fact_regular_bill(View):
    def post(self, request, id):
        _id = self.kwargs['id']
        obj = HISTORIQUE_REGULAR_FACT.objects.get(slug = slugify(_id))
        obj.n_facture = request.POST.get('n_facture')
        obj.save()
        qs = FLIGHT_ASSIST.objects.filter(escale = obj.escale.escale, act_dte_arr__isnull = False, compagnie_dispatcher = obj.company.company_dispatcher, act_dte_arr__gte = obj.from_date, act_dte_arr__lte = obj.until_date)
        for flt in qs:
            flt.n_facture = request.POST.get('n_facture')
            flt.save()
        return HttpResponseRedirect(reverse('core:fact-regular-detail', kwargs={
                'slug': obj.slug
            }))

class HistOPCompany(ListView):
    template_name = 'core/hist_op_company.html'
    paginate_by = 20

    def get_context_data(self, *args,**kwargs):
        context = super(HistOPCompany, self).get_context_data(*args, **kwargs)
        context['title'] = 'HISTORIQUE DES OPéRATIONS'.upper()
        obj = COMP_DISPATCHER.objects.get(slug = self.kwargs['slug'])
        context['monnaie'] = obj.monnaie
        context['comp'] = obj.company_dispatcher
        return context
    
    def get_queryset(self):
        return HISTORIQUE_OP_COMPANY.objects.filter(company = COMP_DISPATCHER.objects.get(slug = self.kwargs['slug'])).order_by('-date_last_add')


# BAG


class luggage_view(ListView):
    template_name = 'core/luggage_view.html'
    ordering = ['-date_claim']

    def get_queryset(self):
        if self.kwargs['opt'] == 'ahl':
            return BAG_SUIVI.objects.filter(file_type='AHL').order_by('-date_claim')
        elif self.kwargs['opt'] == 'ohd':
            return BAG_SUIVI.objects.filter(file_type='OHD').order_by('-date_claim')
        else:
            return BAG_SUIVI.objects.filter(file_type='DPR').order_by('-date_claim')

    def get_context_data(self, *args,**kwargs):
        context = super(luggage_view, self).get_context_data(*args, **kwargs)
        if self.kwargs['opt'] == 'ahl':
            context['title'] = 'ANNUAIRE DES AHL'
            context['type'] = 'AHL'
        elif self.kwargs['opt'] == 'ohd':
            context['title'] = 'ANNUAIRE DES OHD'
            context['type'] = 'OHD'
        else:
            context['title'] = 'ANNUAIRE DES DPR'
            context['type'] = 'DPR'
        return context

context = {
    'status': list(status),
    'escales': list(ESCALES.objects.all()),
    'rl': list(BAG_RL.objects.all()),
    'bag_id_colours': list(BAG_ID_CHART.objects.filter(cat='Colour Codes')),
    'bag_id_type_codes_nz': list(BAG_ID_CHART.objects.filter(cat='Type Codes', sub_cat='Non-zippered Bags')),
    'bag_id_type_codes_z': list(BAG_ID_CHART.objects.filter(cat='Type Codes', sub_cat='zippered Bags')),
    'misc_specials': list(BAG_ID_CHART.objects.filter(cat='Miscllaneous Articles', sub_cat='Special containers')),
    'misc_sport': list(BAG_ID_CHART.objects.filter(cat='Miscllaneous Articles', sub_cat='Sporting Goods')),
    'misc_child': list(BAG_ID_CHART.objects.filter(cat='Miscllaneous Articles', sub_cat='Child / Infant')),
    'misc_photo': list(BAG_ID_CHART.objects.filter(cat='Miscllaneous Articles', sub_cat='Photographic/Electronic/Musical/Communications Equipment')),
    'misc_inse': list(BAG_ID_CHART.objects.filter(cat='Miscllaneous Articles', sub_cat='Item Not Shown Elsewhere')),
    'bag_id_other_type_codes_inse': list(BAG_ID_CHART.objects.filter(cat='Type Codes', sub_cat='Item Not Shown Elsewhere')),
    'bag_id_other_type_codes_basic': list(BAG_ID_CHART.objects.filter(cat='Type Codes', sub_cat='Basic Element')),
    'bag_id_other_type_codes_ext': list(BAG_ID_CHART.objects.filter(cat='Type Codes', sub_cat='External Element')),
}

def add_ahl(request, context = context):
    context['title'] = "AJOUT D'UN AHL"
    context['type'] = 'AHL'
    context['tag'] = 'x'
    # try:
    #     maxid = BAG_SUIVI.objects.filter(file_type = 'AHL').filter(date_claim__year=datetime.datetime.now().year).aggregate(Max('_id'))
    #     obj = BAG_SUIVI.objects.get(_id = maxid.get('_id__max'))
    #     maxid = re.search('(\d+)/', obj.n_file).group(1)
    # except BAG_SUIVI.DoesNotExist:
    #     maxid = '0'
    # context['n_file'] = str(int(maxid) + 1) + '/' + str(datetime.datetime.now().year).replace('20', '')
    return render(request, 'core/add-bag-case.html', context)

def add_dpr(request, context = context):
    context['title'] = "AJOUT D'UN DPR"
    context['type'] = 'DPR'
    context['tag'] = 'x'
    # try:
    #     maxid = BAG_SUIVI.objects.filter(file_type = 'DPR').filter(date_claim__year=datetime.datetime.now().year).aggregate(Max('_id'))
    #     obj = BAG_SUIVI.objects.get(_id = maxid.get('_id__max'))
    #     maxid = re.search('(\d+)/', obj.n_file).group(1)
    # except BAG_SUIVI.DoesNotExist:
    #     maxid = '0'
    # context['n_file'] = str(int(maxid) + 1) + '/' + str(datetime.datetime.now().year).replace('20', '')
    return render(request, 'core/add-bag-case.html', context)

def add_ohd(request, context = context):
    context['title'] = "AJOUT D'UN OHD"
    context['type'] = 'OHD'
    context['tag'] = 'x'
    # try:
    #     maxid = BAG_SUIVI.objects.filter(file_type = 'OHD').filter(date_claim__year=datetime.datetime.now().year).aggregate(Max('_id'))
    #     obj = BAG_SUIVI.objects.get(_id = maxid.get('_id__max'))
    #     maxid = re.search('(\d+)/', obj.n_file).group(1)
    # except BAG_SUIVI.DoesNotExist:
    #     maxid = '0'
    # context['n_file'] = str(int(maxid) + 1) + '/' + str(datetime.datetime.now().year).replace('20', '')
    return render(request, 'core/add-bag-case.html', context)

class validBagCase(View):
    def post(self, request):
        # print(request.POST)
        dic = dict(request.POST)
        dic_bag = dict()
        dic_flt = dict()
        del dic['csrfmiddlewaretoken']
        # dic_values = dic.items()
        nb_bag = 0
        if (dic['file_type'][0] == 'AHL' or dic['file_type'][0] == 'DPR') and dic['id'][0] == '0':
            if int(dic['n_bag_received'][0]) + int(dic['n_bag_miss_dmg'][0]) != len(dic['bag_n_tag']):
                messages.error(request, 'Veuillez renseigner tout les bagages (Reçus et manquants / endommagés) (' + str(int(dic['n_bag_received'][0]) + int(dic['n_bag_miss_dmg'][0])) + ')')
                if dic['file_type'][0] == 'AHL':
                    return redirect('core:add-ahl')
                else:
                    return redirect('core:add-dpr')
        for key, value in dic.copy().items():
            if key.startswith('bag'):
                vals = []
                if key == 'bag_weight':
                    nb_bag = len(value)
                for idx in value:
                    if idx == '' or idx == 'null':
                        vals.append(None)
                    else:
                        if key == 'bag_weight':
                            vals.append(float(idx))
                        else:
                            if idx == 'oui':
                                idx = True
                            elif idx == 'non':
                                idx = False
                            vals.append(idx)
                if len(vals) == 1:
                    dic_bag[key] = vals[0]
                else:
                    dic_bag[key] = vals
                del dic[key]
            elif key == 'company' or key == 'flt' or key == 'dte_flt' or key == 'prov' or key == 'dest' or key == 'fs' or key == 'ft' or key == 'flt_obs' or key == 'n_flt':
                # print(key, value)
                vals = []
                if key == 'n_flt':
                    nb_flt = len(value)
                for idx in value:
                    if idx == '':
                        vals.append(None)
                    else:
                        vals.append(idx)
                if len(vals) == 1:
                    dic_flt[key] = vals[0]
                else:
                    dic_flt[key] = vals
                del dic[key]
            else:
                if value[0] == '' or value[0] == 'null':
                    dic[key] = None
                elif value[0] == 'oui':
                    dic[key] = True
                elif value[0] == 'non':
                    dic[key] = False
                else:
                    if key == 'rl':
                        obj = BAG_RL.objects.get(code = value[0])
                        dic[key] = obj
                    else:
                        dic[key] = value[0]
        # print(dic_bag)
        if 'id' in dic:
            del dic['id']
        # save status
        if request.POST.get('id') != '0':
            old_conf = BAG_SUIVI.objects.get(_id = request.POST.get('id')).file_conforme
            old_st = BAG_SUIVI.objects.get(_id = request.POST.get('id')).status
        else:
            old_conf = None
            old_st = None
        # max_suivi = BAG_SUIVI.objects.aggregate(Max('_id'))
        # obj._id = max_suivi.get('_id__max') + 1
        created = False
        try:
            obj = BAG_SUIVI.objects.get(_id = request.POST.get('id'))
        except BAG_SUIVI.DoesNotExist:
            obj, created = BAG_SUIVI.objects.get_or_create(
                date_claim=datetime.datetime.now(),
                defaults = dic
            )
        if created:
            print('CREATED', obj.file_type)
            # obj.date_claim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            if obj.file_type == 'AHL':
                if obj.file_conforme:
                    obj.status = 'RECH. SECONDAIRE'
                else:
                    obj.status = 'RECH. PRIMAIRE'
            elif obj.file_type == 'DPR':
                if obj.file_conforme:
                    obj.status = 'EN COURS D\'INDEMNISATION'
                else:
                    obj.status = None
            else:
                obj.status = None
            obj.user_last_edit = request.user.first_name + ' ' + request.user.last_name
            # print(len(dic_bag['bag_weight']))
            for idx in range(0, nb_bag):
                # print(idx)
                vals = dict()
                for key, val in dic_bag.items():
                    if nb_bag == 1:
                        vals[key] = val
                    else:
                        vals[key] = val[idx]
                bag_obj = BAG_DETAILS(**vals)
                bag_obj.suivi = obj
                bag_obj.save()
            if 'n_flt' in dic_flt:
                del dic_flt['n_flt']
            for idx in range(0, nb_flt):
                # print(idx)
                vals = dict()
                for key, val in dic_flt.items():
                    if nb_flt == 1:
                        vals[key] = val
                    else:
                        vals[key] = val[idx]
                flt_obj = BAG_FLIGHTS(**vals)
                flt_obj.suivi = obj
                flt_obj.save()
            obj.save()
            messages.success(request, 'Nouveau cas crée avec succès !')
            return redirect(reverse('core:luggage-view', kwargs = {
                'opt' : 'ahl'
            }))
        else:
            obj, created = BAG_SUIVI.objects.update_or_create(
                _id = request.POST.get('id'),
                defaults = dic
            )
            if old_conf is not None and obj.file_conforme != old_conf and obj.file_type == 'DPR':
                # print('HERE')
                obj.status = 'EN COURS D\'INDEMNISATION'.upper()
                typ = obj.file_type
                try:
                    maxid = BAG_SUIVI.objects.filter(file_type = typ).filter(date_claim__year=datetime.datetime.now().year).aggregate(Max('_id'))
                    obj_max = BAG_SUIVI.objects.get(_id = maxid.get('_id__max'))
                    maxid = re.search('(\d+)/', obj_max.n_file).group(1)
                except (BAG_SUIVI.DoesNotExist, TypeError):
                    maxid = '0'
                obj.n_file = str(int(maxid) + 1) + '/' + str(datetime.datetime.now().year).replace('20', '')
                indemn_obj = BAG_HIST_INDEMN.objects.create(
                    suivi = obj,
                    dte_prop = None,
                    esc_dest = obj.escale_claim,
                    monnaie = None,
                    montant_dzd = None,
                    montant_eur = None,
                    montant_usd = None,
                    accord = None
                )
                indemn_obj.save()
            obj.save()
            st = obj.status
            subs_obj = obj
            if old_st is not None and old_st != 'EN COURS D\'INDEMNISATION' and obj.status == 'EN COURS D\'INDEMNISATION':
                typ = obj.file_type
                try:
                    maxid = BAG_SUIVI.objects.filter(file_type = typ).filter(date_claim__year=datetime.datetime.now().year).aggregate(Max('_id'))
                    obj = BAG_SUIVI.objects.get(_id = maxid.get('_id__max'))
                    maxid = re.search('(\d+)/', obj.n_file).group(1)
                except (BAG_SUIVI.DoesNotExist, TypeError):
                    maxid = '0'
                obj.n_file = str(int(maxid) + 1) + '/' + str(datetime.datetime.now().year).replace('20', '')
                indemn_obj, created = BAG_HIST_INDEMN.objects.create(
                    suivi = obj,
                    dte_prop = None,
                    esc_dest = obj.escale_claim,
                    monnaie = None,
                    montant_dzd = None,
                    montant_eur = None,
                    montant_usd = None,
                    accord = None
                )
                indemn_obj.save()
            obj.save()
            # print(dic_bag)
            indemn_obj = BAG_HIST_INDEMN.objects.filter(suivi = obj).order_by('-_id').first()
            _id = '0'
            print(subs_obj.dte_sign)
            if 'montant_dzd' in dic and indemn_obj.dte_prop is None:
                indemn_obj.dte_prop = datetime.datetime.now().date()
                indemn_obj.monnaie = dic['monnaie']
                echg = EXCHANGE.objects.get(status='actual')
                if indemn_obj.monnaie == 'USD':
                    indemn_obj.montant_usd = float(dic['montant_dzd'])
                    # MAKE EXCHANGE HERE ( IATA RATES )
                    indemn_obj.montant_dzd = round(indemn_obj.montant_usd * echg.dzd, 2)
                else:
                    indemn_obj.montant_dzd = float(dic['montant_dzd'])
                    indemn_obj.montant_usd = round(indemn_obj.montant_dzd / echg.dzd, 2)
                indemn_obj.save()
                _id = obj._id
            elif 'accord' in dic and indemn_obj.accord is None:
                indemn_obj.accord = dic['accord']
                indemn_obj.save()
                if not indemn_obj.accord:
                    indemn_obj = BAG_HIST_INDEMN.objects.create(
                        suivi = subs_obj,
                        dte_prop = None,
                        esc_dest = subs_obj.escale_claim,
                        monnaie = None,
                        montant_dzd = None,
                        montant_eur = None,
                        montant_usd = None,
                        accord = None
                    )
                    indemn_obj.save()
                else:
                    # BILL OTHER COMPANIES
                    # 1. MILEAGE
                    exch = EXCHANGE.objects.get(status='actual')
                    if indemn_obj.monnaie != 'USD':
                        usd_amount = round(indemn_obj.montant_dzd / exch.dzd, 2)
                    else:
                        usd_amount = indemn_obj.montant_usd
                    qs = BAG_FLIGHTS.objects.filter(suivi = subs_obj)
                    if qs.count() > 1:
                        tot_miles = 0
                        for flt in qs:
                            tot_miles += flt.miles
                        for flt in qs:
                            prc = round((flt.miles * 100) / tot_miles, 2)
                            flt.montant_fct = round((usd_amount * prc) / 100, 2)
                            flt.save()
                _id = subs_obj._id
            elif subs_obj.payment_status:
                subs_obj.status = 'CLOSED'
                subs_obj.save()
                _id = subs_obj._id
            else:
                objs = BAG_DETAILS.objects.filter(suivi=request.POST.get('id'))
                # print(dic_bag)
                idx = 0
                for item in objs:
                    st_dic = dict()
                    for key, value in dic_bag.items():
                        if type(value) == list:
                            st_dic[key] = value[idx]
                        else:
                            st_dic[key] = value
                    obj, created = BAG_DETAILS.objects.update_or_create(
                        _id = item._id,
                        defaults = st_dic
                    )
                    idx += 1
                    obj.save()
                if st != 'CLOSED':
                    qs = BAG_DETAILS.objects.filter(suivi=request.POST.get('id'), bag_status = False)
                    found = True
                    for bag in qs:
                        if not bag.bag_found:
                            found = False
                            break
                    if found:
                        subs_obj.status = 'CLOSED'
                        subs_obj.save()
                flts = BAG_FLIGHTS.objects.filter(suivi=request.POST.get('id'))
                idx = 0
                for item in flts:
                    st_dic = dict()
                    vals = []
                    for key, value in dic_flt.items():
                        if type(value) == list:
                            st_dic[key] = value[idx]
                        else:
                            st_dic[key] = value
                    obj, created = BAG_FLIGHTS.objects.update_or_create(
                        _id = item._id,
                        defaults = st_dic
                    )
                    idx += 1
                    obj.save()
                _id = item.suivi._id
            messages.success(request, 'Modificaton effectué avec succès !')
            return redirect(reverse('core:bag-case-details', kwargs = {
                'pk' : int(_id)
            }))


class BagCaseDetails(DetailView):
    model = BAG_SUIVI
    template_name = 'core/add-bag-case.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BagCaseDetails, self).get_context_data(*args, **kwargs)
        _id = self.kwargs['pk']
        context['obj'] = BAG_SUIVI.objects.get(_id = self.get_object().pk)
        context['type'] = context['obj'].file_type
        context['rl_desc'] = BAG_RL.objects.get(code = context['obj'].rl.code).rl
        context['title'] = 'Détails du : '.upper() + context['type']
        context['id'] = _id
        context['stats'] = list(status)
        bags_obj = BAG_DETAILS.objects.filter(suivi=context['obj'])
        context['bags'] = list(bags_obj)
        flts_obj = BAG_FLIGHTS.objects.filter(suivi=context['obj'])
        context['flts'] = list(flts_obj)
        context['tag'] = 'x'
        context['status'] = context['obj'].status
        if context['type'] == 'OHD':
            context['tag'] = BAG_DETAILS.objects.get(suivi=context['obj']).bag_n_tag
        context['length'] = bags_obj.count()
        context['escales'] = list(ESCALES.objects.all())
        context['rl'] = list(BAG_RL.objects.all())
        context['ind'] = BAG_HIST_INDEMN.objects.filter(suivi = context['obj']).order_by('-_id').first()
        if context['ind'] is not None:
            if context['ind'].monnaie is None:
                context['amount'] = None
            elif context['ind'].monnaie == 'DZD':
                context['amount'] = context['ind'].montant_dzd
            else:
                context['amount'] = context['ind'].montant_usd
        return context 

class HistIndemn(ListView):
    model = BAG_HIST_INDEMN
    template_name = 'core/history-indemnisation.html'
    paginate_by = 15

    def get_queryset(self):
        return BAG_HIST_INDEMN.objects.filter(suivi = self.kwargs['pk']).order_by('-_id')
    
    def get_context_data(self, *args, **kwargs):
        context = super(HistIndemn, self).get_context_data(*args, **kwargs)
        obj = BAG_SUIVI.objects.get(_id = self.kwargs['pk'])
        context['title'] = 'Historique des propositions d\'indemnisation : ' + obj.file_type + ' N° ' + obj.n_file
        return context

class AllPriceList(ListView):
    model = TARIF_OCCAS
    template_name = 'core/all-prices-list.html'

    def get_queryset(self):
        return TARIF_OCCAS.objects.all().order_by('-dte_begin')

    def get_context_data(self, *args, **kwargs):
        context = super(AllPriceList, self).get_context_data(*args, **kwargs)
        context['title'] = 'Liste des prices list enregistrées'.upper()
        return context

class ExchangeRates(ListView):
    model = EXCHANGE
    template_name = 'core/exchange-rates.html'

    def get_queryset(self):
        return EXCHANGE.objects.all().exclude(status='actual').order_by('-date_begin')

    def get_context_data(self, *args, **kwargs):
        context = super(ExchangeRates, self).get_context_data(*args, **kwargs)
        context['actual'] = EXCHANGE.objects.get(status='actual')
        context['title'] = 'Annuaire des taux d\'échanges enregistrés'.upper()
        return context

class validExchRate(View):
    def post(self, request):
        # print(request.POST)
        dic = dict(request.POST)
        del dic['csrfmiddlewaretoken']
        print(dic)
        dic_values = dic.items()
        for key, value in dic_values:
            dic[key] = value[0]
        dic['usd'] = 1
        obj = EXCHANGE.objects.get(status='actual')
        obj.status = None
        obj.date_end = datetime.datetime.now().date()
        obj.save()
        new = EXCHANGE(**dic)
        new.status = 'actual'
        new.user_last_edit = request.user.first_name + ' ' + request.user.last_name
        new.date_begin = datetime.datetime.now().date()
        new.save()
        messages.success(request, 'Nouveau taux d\'échanges enregistré')
        return redirect('core:exchange-rates')



@login_required
def valid_case(request):
    dic = dict(request.POST)
    del dic['csrfmiddlewaretoken']
    print(dic['file_type'][0].lower())
    return redirect(reverse('core:luggage-view', kwargs = {
            'opt' : dic['file_type'][0].lower()
        }))



