from django import template
from django.utils.text import slugify
import datetime
from django.utils import timezone
import os
# pylint: disable=E1101
# pylint: disable=import-error
# pylint: disable=no-name-in-module
from core.models import (
    FLIGHT_ASSIST,
    FLIGHT_OCCAS,
    COMP_DISPATCHER,
)


register = template.Library()


@register.filter
def flight_occas_count(user):
    if user.is_authenticated:
        qs = FLIGHT_ASSIST.objects.all()
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_occas_opere_count(user):
    if user.is_authenticated:
        qs = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = False, etat_du_vol='OPERE')
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_occas_cnl_count(user):
    if user.is_authenticated:
        qs = FLIGHT_ASSIST.objects.filter(etat_du_vol='ANNULE')
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_occas_pending_count(user):
    if user.is_authenticated:
        qs = FLIGHT_ASSIST.objects.filter(montant_globale__isnull = True).exclude(etat_du_vol__in = ['ANNULE', 'NO OP'])
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def get_solde_est(company):
    company = COMP_DISPATCHER.objects.get(company_dispatcher=company)
    return company.solde_estimee

@register.filter
def flight_cnl(obj):
    bl = False
    if datetime.datetime.combine(timezone.now().date(), timezone.now().hour()) >= datetime.datetime.combine(obj.date_arrivee, obj.sta) and (obj.etat_du_vol != 'OPERE' and obj.etat_du_vol != 'ANNULE'):
        obj.etat_du_vol = 'ANNULE'
        obj.save()
        bl = True
    return  

@register.filter()
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400: # 60sec * 60min * 24hrs
        days = secs // 86400
        timetot += "{} days".format(int(days))
        secs = secs - days*86400

    if secs > 3600:
        hrs = secs // 3600
        timetot += " {} hours".format(int(hrs))
        secs = secs - hrs*3600

    if secs > 60:
        mins = secs // 60
        timetot += " {} minutes".format(int(mins))
        secs = secs - mins*60

    if secs > 0:
        timetot += " {} seconds".format(int(secs))
    return timetot

@register.filter()
def if_readonly(obj):
    return obj.etat_du_vol == 'ANNULE' or obj.etat_du_vol == 'OPERE' or obj.etat_du_vol == 'NO OP'

@register.filter
def get_type(value):
    return str(type(value))

def slugify_val(value):
    return slugify(value)

@register.filter
def if_late(obj):
    if (datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.now().time()) - datetime.datetime.combine(obj.date_arrivee, obj.sta) > datetime.timedelta(days=6) or datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.now().time()) >= datetime.datetime.combine(obj.date_arrivee, obj.sta)) and obj.etat_du_vol == 'ANNULE':
        # obj.reponse = True
        # obj.save()
        return True
    else:
        return False

@register.filter
def filename(value):
    return os.path.basename(value.name)

@register.filter
def subtract(value, arg):
    return value - arg

