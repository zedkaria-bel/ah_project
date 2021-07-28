from django.urls import path
from .views import (
    home_view,
    get_back,
    RequestSummary,
    FlightOccas,
    add_vol_occas_view,
    valid_company,
    AddVolOccas,
    valid_date,
    agent_flight_summary,
    post_vol,
    valid_services,
    validReleveTouchee,
    facturation_occas,
    CompaniesSummary,
    add_company,
    ValidNewCompany,
    valid_new_company_name,
    CompanyDetail,
    valid_fiche,
    price_list,
    price_list_actual,
    ValidPriceList,
    FichesTouchee,
    gestion_affect_fiches,
    AddQuota,
    valid_affect_quota,
    HistQuota,
    AffectQuota,
    valid_escale,
    HistAffect,
    valid_cnl_fiche,
    CNLFiches,
    HistCNL,
    valid_uniq_flt,
    add_schedule,
    NewSchedule,
    FactRegular,
    valid_company_fact,
    dashboard,
    build_chart,
    HistRegularFact,
    validFactRegular,
    FactRegularDetail,
    HistOPCompany,
    luggage_view,
    add_ahl, add_dpr, add_ohd,
    validBagCase,
    BagCaseDetails,
    valid_case,
    HistIndemn,
    AllPriceList,
    ExchangeRates,
    validExchRate,
    fact_regular_bill,
    Dash,
    cas_build_pie_chart,
    cas_build_time_chart,
)

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home-view'),
    path('get-back', get_back, name = 'get-back'),
    path('request-summary/<str:activite>/', RequestSummary.as_view(), name = 'request-summary'),
    path('request-summary/<str:activite>/<str:qs>/', RequestSummary.as_view(), name = 'request-summary-specials'),
    path('flight-detail/<slug>/', FlightOccas.as_view(), name = 'flight-detail'),
    path('add-occas-flight/', add_vol_occas_view, name = 'add-occas-flight'),
    path('valid-company/', valid_company, name = 'valid-company'),
    path('valid-date/', valid_date, name = 'valid-date'),
    path('valid-vol-occas/', AddVolOccas.as_view(), name = 'valid-vol-occas'),
    path('agent-summary/<str:activite>/', agent_flight_summary.as_view(), name='agent-summary'),
    path('post-vol/<slug>/', post_vol.as_view(), name = 'post-vol'),
    path('valid-services/', valid_services, name = 'valid-services'),
    path('valid-releve-touchee/', validReleveTouchee.as_view(), name = 'valid-releve-touchee'),
    path('facturation-occas/<int:n_field>/', facturation_occas, name = 'facturation-occas'),
    path('companies-summary/', CompaniesSummary.as_view(), name = 'companies-summary'),
    path('add-company/', add_company, name = 'add-company'),
    path('valid-new-company/', ValidNewCompany.as_view(), name = 'valid-new-company'),
    path('valid-new-company-name/', valid_new_company_name, name = 'valid-new-company-name'),
    path('compagnie-detail/<slug>/', CompanyDetail.as_view(), name = 'compagnie-detail'),
    path('valid-fiche/', valid_fiche, name = 'valid-fiche'),
    path('price-list/<pk>/', price_list.as_view(), name = 'price-list'),
    path('price-list/', price_list_actual, name = 'price-list-actual'),
    path('annuaire-prices-list/', AllPriceList.as_view(), name = 'annuaire-prices-list'),
    path('valid-price-list/', ValidPriceList.as_view(), name = 'valid-price-list'),
    path('fiche-touchee/', FichesTouchee.as_view(), name = 'fiche-touchee'),
    path('fiche-touchee/gestion-fiches/', gestion_affect_fiches, name = 'gestion-fiches'),
    path('fiche-touchee/gestion-fiches/add-quota/', AddQuota.as_view(), name = 'add-quota'),
    path('valid-affect-quota/', valid_affect_quota, name = 'valid-affect-quota'),
    path('fiche-touchee/gestion-fiches/hist-quota/', HistQuota.as_view(), name = 'hist-quota'),
    path('affect-quota/', AffectQuota.as_view(), name = 'affect-quota'),
    path('valid-escale/', valid_escale, name = 'valid-escale'),
    path('fiche-touchee/gestion-fiches/hist-affect/', HistAffect.as_view(), name = 'hist-affect'),
    path('valid-cnl-fiche/', valid_cnl_fiche, name = 'valid-cnl-fiche'),
    path('fiche-touchee/gestion-fiches/cnl-fiches/', CNLFiches.as_view(), name = 'cnl-fiches'),
    path('fiche-touchee/gestion-fiches/hist-cnl/', HistCNL.as_view(), name = 'hist-cnl'),
    path('valid-uniq-flt/', valid_uniq_flt, name = 'valid-uniq-flt'),
    path('add-schedule/', add_schedule, name = 'add-schedule'),
    path('new-schedule/', NewSchedule.as_view(), name = 'new-schedule'),
    path('fact-regular/', FactRegular.as_view(), name = 'fact-regular'),
    path('valid-company-fact/', valid_company_fact, name = 'valid-company-fact'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('dashboard-cas/', Dash, name = 'dashboard-cas'),
    path('dashboard/build-chart/', build_chart, name = 'build-chart'),
    path('fact-regular/hist-regular-fact/', HistRegularFact.as_view(), name = 'hist-regular-fact'),
    path('valid-fact-regular/', validFactRegular.as_view(), name = 'valid-fact-regular'),
    path('fact-regular-detail/<slug>/', FactRegularDetail.as_view(), name = 'fact-regular-detail'),
    path('compagnie-detail/<slug>/historic-operations-company/', HistOPCompany.as_view(), name = 'historic-operations-company'),
    path('luggage-summary/<str:opt>/', luggage_view.as_view(), name = 'luggage-view'),
    path('luggage-view/add-ahl/', add_ahl, name = 'add-ahl'),
    path('luggage-view/add-dpr/', add_dpr, name = 'add-dpr'),
    path('luggage-view/add-ohd/', add_ohd, name = 'add-ohd'),
    path('bag-case/<pk>/', BagCaseDetails.as_view(), name = 'bag-case-details'),
    path('valid-bag-case/', validBagCase.as_view(), name = 'valid-bag-case'),
    path('valid-case/', valid_case, name = 'valid-case'),
    path('bag-case/<pk>/historique-des-propositions/', HistIndemn.as_view(), name = 'historique-des-propositions'),
    path('exchange-rates/', ExchangeRates.as_view(), name = 'exchange-rates'),
    path('valid-exchange-rate/', validExchRate.as_view(), name = 'valid-exchange-rate'),
    path('fact-regular-bill/<int:id>/', fact_regular_bill.as_view(), name = 'fact-regular-bill'),
    path('cas-build-pie-chart/', cas_build_pie_chart, name = 'cas-build-pie-chart'),
    path('cas-build-time-chart/', cas_build_time_chart, name = 'cas-build-time-chart'),
]