

MONNAIE = ['DZD', 'USD', 'EUR']

FLIGHT_STATUS = ['OPERE', 'ANNULE', 'RE-SCHED', 'IRGHO', 'NO OP']

PAYMENT = ['CONTRAT', 'VIREMENT', 'PRE-PAY', 'TPE/CARD', 'CASH', 'AUTRE']

NATURE = ['PAX', 'CARGO', 'VIP', 'MILITAIRE', 'PIST', 'TECH', 'SERVICES', 'FULL HANDLING', 'AUTRE']

monnaie = (
    (1, 'DZD'),
    (2, 'USD'),
    (3, 'EUR')
)

poste = (
    (1, 'SOUS DIRECTEUR GESTION DES ESCALES'),
    (2, 'CHEF DEPARTEMENT'),
    (3, 'CHEF DE SERVICE'),
    (4, 'AGENT'),
    (5, 'CHEF D\'ESCALE')
)

dpt = (
    (1, 'DPT CONTRATS ET ASSISTANCE AU SOL'),
    (2, 'CONTRôLE DU FONCTIONNEMENT DES ESCALES'.upper()),
    (3, 'DPT LOGISTIQUE DES ESCALES'),
    (4, 'DPT RECHERCHES ET INDEMNISATION DES BAGAGES')
)

service_ramp_piste = (
    (1, 'TAPIS BAGAGE'),
    (2, 'TRACTEUR CHARIOT'),
    (3, 'PASSERELLE AUTO TRAC'),
    (4, 'PASSERELLE TRACTEE'),
    (5, 'NAVETTE PISTE'),
    (6, 'NET CABINE'),
    (7, 'AGENT DE SERVITUDE'),
    (8, 'AGENT D\'OPERATIONS QUALIFIE'),
    (9, 'CHARIOT BAGAGE'),
    (10, 'DOSSIER DE VOL'),
    (11, 'HEADSET'),
    (12, 'CALES'),
    (13, 'ARRANGEMENT CABINE'),
    (14, 'BRS'),
    (15, 'BAGAGE D\'IDENTIFICATION'),
    (16, 'TOWING'),
    (17, 'HUM'),
    (18, 'CHARGEMENT'),
    (19, 'DECHARGEMENT')
)

service_passager = (
    (1, 'AMBULIFT'),
    (2, 'NBR GUICHET'),
    (3, 'VIP'),
    (4, 'SALON'),
    (5, 'CIVIERE'),
    (6, 'DOCUMENT METEO'),
    (7, 'VHF COMMUNICATION'),
    (8, 'MESSAGE OPS'),
)

causes = ['ERREUR', 'DISPARITION', 'ETAT DÉTÉRIORÉ', 'AUTRE']


# MTOW / TOUCHEE

MTOW_10_COM = 500
MTOW_10_TECH = 300
MTOW_10_30_COM = 900
MTOW_10_30_TECH = 500
MTOW_30_50_COM = 1400
MTOW_30_50_TECH = 700
MTOW_50_80_COM = 2300
MTOW_50_80_TECH = 1200
MTOW_80_150_COM = 3400
MTOW_80_150_TECH = 1400
MTOW_150_250_COM = 4500
MTOW_150_250_TECH = 1700
MTOW_250_COM = 6200
MTOW_250_TECH = 2200


# SERVICES ADD

ASSIST_WCH = 35
ASSIST_UM = 30
ASSIST_TRANSIT = 30
ACC_SALON = 35
ASSIST_VIP = 100
USE_DCS = 2
DEPORTEE = 100
AGENT_SERV_PASSAGE = 100
CIVIERE = 300
HUM = 150
OUV_DOSS_BAG = 15
DOSS_VOL_IMP = 100
AGENT_COORD = 150
COMM_SOL_COCKPIT = 80
AGENT_OP_QUALIF = 200
GPU = 200
ASU_MOY_PORT = 200
ASU_BIG_PORT = 300
ACU = 400
VIDE_TOILET_MOY_PORT = 120
VIDE_TOILET_BIG_PORT = 230
PLEIN_WATER_MOY_PORT = 100
PLEIN_WATER_BIG_PORT = 170
NET_CABINE_100 = 150
NET_CABINE_200 = 250
NET_CABINE_300 = 350
ARRANGEMENT_CAB_100 = 100
ARRANGEMENT_CAB_200 = 250
ARRANGEMENT_CAB_300 = 300
RECONC_BAG_BRS = 100
ID_BAG_100 = 100
ID_BAG_200 = 200
PASSERELLE_PSG = 200
CAMION_ELEV = 200
VIP_BUS = 100
VEHICULE_TRANSP_PISTE = 150
PUSH_BACK = 180
TOWING = 300
CHARIOT_BAG = 80
TRACT_CHARIOT = 120
TAPIS_BAG = 250
PLATEFORME = 400
PORTE_CONTAINER_PALETTE = 20
CONTAINER_PALETTE = 50
ELEV_FOURCHE = 200
AGENT_SERV_PISTE = 100
DB_MANIP_ULD = 500

# MAJORATIONS

# HOLIDAYS
WEEKEND = ['VENDREDI', 'SAMEDI']

EID_EL_ADHA = ['31-07-2020', '20-07-2021', '10-07-2022', '29-06-2023', '17-06-2024', '07-06-2025']

EID_EL_FITR = ['24-05-2020', '13-05-2021', '03-05-2022', '22-04-2023', '10-04-2024', '31-03-2025']

MAWLID_NABAWI = ['29-10-2020', '19-10-2021', '08-10-2022', '27-09-2023', '16-09-2024', '05-09-2025']

MUHARRAM = ['20-08-2020', '10-08-2021', '30-07-2022', '19-07-2023', '08-07-2024', '27-06-2025']

NIGHT = ['21:00', '06:00']
