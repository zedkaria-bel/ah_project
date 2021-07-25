from django import template
from django.utils.text import slugify
import datetime
from django.utils import timezone
import os
from django.utils.translation import gettext as _
# pylint: disable=E1101
# pylint: disable=import-error
# pylint: disable=no-name-in-module
from core.models import (
    FLIGHT_ASSIST,
    FLIGHT_OCCAS,
    COMP_DISPATCHER,
    BAG_DETAILS,
    BAG_HIST_INDEMN,
)


register = template.Library()


@register.filter
def flight_occas_count(user, act):
    if user.is_authenticated:
        if act == 'occas':
            cmps = COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL').values_list('company_dispatcher', flat=True)
        else:
            cmps = COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').values_list('company_dispatcher', flat=True)
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = cmps)
        qs = qs.filter(montant_globale__isnull = False, n_facture__isnull = True)
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_occas_opere_count(user, act):
    if user.is_authenticated:
        cmps = COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL').values_list('company_dispatcher', flat=True)
        exc = ['OPERE', 'NO OP', 'ANNULE']
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = cmps).exclude(etat_du_vol__in = exc)
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_for_today(user):
    if user.is_authenticated:
        cmps = COMP_DISPATCHER.objects.filter(activite = 'CONTRACTUEL').values_list('company_dispatcher', flat=True)
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = cmps, date_arrivee = datetime.datetime.now().date())
        if qs.exists():
            return qs.count()
    return 0

@register.filter
def flight_occas_cnl_count(user):
    if user.is_authenticated:
        cmps = COMP_DISPATCHER.objects.filter(activite = 'OCCASIONNEL').values_list('company_dispatcher', flat=True)
        exc = ['OPERE', 'NO OP', 'ANNULE']
        qs = FLIGHT_ASSIST.objects.filter(compagnie_dispatcher__in = cmps).exclude(etat_du_vol__in = exc)
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
    return obj.etat_du_vol == 'ANNULE' or obj.etat_du_vol == 'OPERE'

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

@register.filter(expects_localtime=True)
def days_since(value, arg=None):
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = datetime.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.datetime.now(tzinfo).date()
    delta = value - today
    if abs(delta.days) == 1:
        day_str = _("jour")
    else:
        day_str = _("jours")

    if delta.days < 1:
        fa_str = _("ago")
    else:
        fa_str = _("from now")
    return "J+%s" % abs(delta.days)

@register.filter
def bag_id(id):
    return BAG_DETAILS.objects.get(suivi=id).bag_n_tag

@register.filter
def get_proposition(obj, attr):
    try:
        ind_obj = BAG_HIST_INDEMN.objects.filter(suivi = obj).order_by('-_id').first()
    except BAG_HIST_INDEMN.DoesNotExist:
        return None
    if ind_obj is None or ind_obj.dte_prop is None:
        return None
    return getattr(ind_obj, attr)

@register.filter(expects_localtime=True)
def days_until(dte_end):
    delta = dte_end - datetime.datetime.now().date()
    return delta.days

@register.filter
def get_str_id(obj):
    return str(obj.auto_id)
