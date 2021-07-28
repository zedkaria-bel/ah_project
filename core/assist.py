import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine
# from chv import df_to_postgres

con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
con.autocommit = True
engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
cursor = con.cursor()

def tf_base(df):
    print(df.shape)
    # print(df.columns)
    pd.set_option('display.max_rows', len(df))
    df = df.loc[df['PROV'] != 'SERVICE'].copy()
    df.dropna(subset = ['ACT DTE ARR', 'ACT DTE DEP', 'PROV', 'DEST', 'PAX     DEP', 'PAX ARRIV', 'CARGO ARRIV', 'CARGO DEP', 'Cie A FACTURER', 'NATURE TOUCHEE', 'TYPE AVION','MTOW (Tn)'], inplace = True)
    df['STATUS'] = 'OPERE'
    df['ACT DTE DEP'] = pd.to_datetime(df['ACT DTE DEP']).dt.date
    df['PAX ARRIV'].fillna(0, inplace = True)
    df['Cie A FACTURER'] = np.where((df['Cie A FACTURER'] == 'TAL') | (df['Cie A FACTURER'] == 'TASSILI AIRLINES') | (df['Cie A FACTURER'] == 'TASSILI ') | (df['Cie A FACTURER'] == 'TASSILI') | (df['Cie A FACTURER'] == 'TASSILI AIRAINES'), 'DTH', df['Cie A FACTURER'])
    df['MTOW (Tn)'] = np.where(df['MTOW (Tn)'].str.replace('.', '', regex = False).astype(int) > 1000, df['MTOW (Tn)'].str.replace('.', '', regex = False).astype(int) / 100, df['MTOW (Tn)'])
    df['DZD'] = np.where(df['MONNAIE'] == 'USD', df['MONTANT GLOBALE'].astype(float) * 133.43, df['DZD'])
    df['MONTANT GLOBALE'] = np.where(df['MONNAIE'] == 'DZD', round(df['MONTANT GLOBALE'].astype(float) / 133.43, 2), df['MONTANT GLOBALE'])
    df['MAJORATION'] = round(df['MAJORATION'] / df['TARIF DE BASE'], 2) * 100
    df['REDUCTION'] = round(df['REDUCTION'] / df['TARIF DE BASE'], 2) * 100
    df['TARIF DE BASE'] = np.where(df['MONNAIE'] == 'DZD', round(df['TARIF DE BASE'].astype(float) / 133.43, 2), df['TARIF DE BASE'])
    df['EUR'] = round(df['MONTANT GLOBALE'] * 0.82, 2)
    df['STA'] = np.where(df['STA'].str.contains('h') | df['STA'].str.contains('H'), df['STA'].str[:2] + ':' + df['STA'].str[3:] + ':00', df['STA'])
    df['STD'] = np.where(df['STD'].str.contains('h') | df['STD'].str.contains('H'), df['STD'].str[:2] + ':' + df['STD'].str[3:] + ':00', df['STD'])
    df['ATA'] = np.where(df['ATA'].str.contains('h') | df['ATA'].str.contains('H'), df['ATA'].str[:2] + ':' + df['ATA'].str[3:] + ':00', df['ATA'])
    df['ATD'] = np.where(df['ATD'].str.contains('h') | df['ATD'].str.contains('H'), df['ATD'].str[:2] + ':' + df['ATD'].str[3:] + ':00', df['ATD'])
    df.rename(columns = {
        'STATUS': 'ETAT DU VOL',
        'ESCALE': 'ESCALE (IATA)',
        'PAX     DEP': 'PAX DEP',
        'Cie A FACTURER': 'COMPAGNIE DISPATCHER',
        'MTOW (Tn)': 'MTOW (Tonnes)',
        'MATRICULE  AVION ': 'REG',
        'UM': 'ASSIST_UM',
        'WCH': 'ASSIST_WCH',
        'MEDICAL LIFT': 'CIVIERE',
        'GPU (MN)': 'GPU',
        'TOILET SERVICE': 'VIDE_TOILET',
        'WATER SERVICE': 'PLEIN_WATER',
        'PUSH BACK ': 'PUSH_BACK',
        'CHARIOT BAG': 'CHARIOT_BAG',
        'TRACTEUR': 'TRACT_CHARIOT',
        'NET CAB': 'NET_CABINE',
        'HEADSET': 'COMM_SOL_COCKPIT',
        'DCS': 'USE_DCS'
    }, inplace = True)
    df = df.drop(columns = ['Unnamed: 0', 'Unnamed: 54', 'STEP AUTO', 'STEP TRACT', 'NAVETTE PISTE', 'MANUT/TNAO', 'TAPIS BAG', 'HUM', 'F/C', 'DEPORTEES'])
    arr = df['ACT DTE ARR'].dt.strftime('%Y-%m-%d').str.replace('-', '')
    arr = arr.str.replace('2021', '21')
    df['KEY_FLT'] = arr.str[4:] + arr.str[2:4] + arr.str[:2] + df['N° VOL ARRIV'] + df['ESCALE (IATA)'] + df['PROV']
    df_cols = df.columns.to_list()
    cols = df_cols[-1:] + df_cols[:-1]
    df = df[cols]
    df['slug'] = df['KEY_FLT'].str.lower()
    df['USER LAST EDIT'] = 'Tarek Hassen'
    df['DATE LAST EDIT'] = '2021-02-08 14:02'
    df['DATE LAST EDIT'] = pd.to_datetime(df['DATE LAST EDIT'])
    df['STA'] = pd.to_datetime(df['STA'], format= '%H:%M:%S').dt.time
    df['STD'] = pd.to_datetime(df['STD'], format= '%H:%M:%S').dt.time
    df['ATD'] = pd.to_datetime(df['ATD'], format= '%H:%M:%S').dt.time
    df['ATA'] = pd.to_datetime(df['ATA'], format= '%H:%M:%S').dt.time
    df.drop_duplicates(subset = ['KEY_FLT'], keep = 'first', inplace = True)
    df.dropna(subset = ['KEY_FLT'], inplace = True)
    df.insert(1, 'N°', range(1, 1 + len(df)))
    df.drop([2, 3, 10, 233, 234], inplace = True)
    print(df.head(), df.shape)
    return df

FILE = os.listdir('CONTRAT & ASSIST')[2]
# print(FILE)
# df = pd.read_excel('CONTRAT & ASSIST/' + FILE, sheet_name = 'Feuil1', skipfooter = 1048332)
# csv = df.to_csv('BASE.csv')
bd_df = pd.DataFrame()
df = pd.read_csv('BASE.csv', low_memory = False, parse_dates = ['ACT DTE ARR', 'ACT DTE DEP', 'STA', 'ATA', 'STD', 'ATD'])
bd_df = tf_base(df)
# df=pd.read_sql_query('select "KEY_FLT" from public."FLIGHT_ASSIST"',con=engine)
bd_df.to_sql('FLIGHT_ASSIST', engine, if_exists='append', index=False)




# df_to_postgres(bd_df, con, cursor, engine, 'FLIGHT_FI')