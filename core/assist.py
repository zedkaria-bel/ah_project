import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine
from chv import df_to_postgres

con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
con.autocommit = True
engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
cursor = con.cursor()

FILE = os.listdir('OCCAS')[0]
df = pd.read_excel('OCCAS/' + FILE, sheet_name = 'ALPHA JET')

dispatcher = [None] * 4
disp_cols = ['COMPANY DISPATCHER', 'SOLDE', 'SOLDE ESTIMEE', 'SOLDE_LAST_EDIT']
dispatcher[0] = df['Unnamed: 2'][11]
dispatcher[1] = df['Unnamed: 17'][2]
dispatcher[2] = df['Unnamed: 17'][6]
dispatcher[3] = df['Unnamed: 18'][2]
if engine.dialect.has_table(engine, 'COMP_DISPATCHER'):
    cmp_disp = pd.read_sql('SELECT * FROM "COMP_DISPATCHER"', con)
    if (cmp_disp['COMPANY DISPATCHER'] == dispatcher[3]).any():
        pass
    else:
        dispatcher = pd.Series(dispatcher, index = disp_cols)
        cmp_disp = cmp_disp.append(dispatcher, ignore_index = True)
        df_to_postgres(cmp_disp, con, cursor, engine, 'COMP_DISPACTHER')
else:
    dispatcher = pd.DataFrame([dispatcher], columns = disp_cols)
    df_to_postgres(dispatcher, con, cursor, engine, 'COMP_DISPACTHER')

df = pd.read_excel('OCCAS/' + FILE, skiprows = 11, sheet_name = 'ALPHA JET')
df = df[df['DATE DEMANDE'].notna()]
date_dep = df['DATE DEPART'].dt.strftime('%d-%m-%Y').tolist()
date_dep = [d.replace('-', '').replace('2021', '21') for d in date_dep]
df['KEY_FLT'] = date_dep + df['N VOL DEP'] + df['PROV']
cols = df.columns.to_list()
df_cols = cols[-1:] + cols[:-1]
df = df[df_cols]
cursor = con.cursor()
df_to_postgres(df, con, cursor, engine, 'FLIGHT_OCCAS')

df_cols = df.columns.to_list()
if engine.dialect.has_table(engine, 'FLIGHT_FI'):
    bd_df = pd.read_sql('SELECT * FROM "FLIGHT_FI"', con)
    print(bd_df.shape)
    cols_bd = bd_df.columns.to_list()
    for idx, row in df.iterrows():
        vol_occas_val = [None] * len(cols_bd)
        vol_occas_val[cols_bd.index('KEY_FLT')] = row['KEY_FLT']
        vol_occas_val[cols_bd.index('STATUS')] = "/"
        vol_occas_val[cols_bd.index('OCCAS')] = 'OCCAS'
        vol_occas_val[cols_bd.index('DATE')] = row['DATE DEPART']
        vol_occas_val[cols_bd.index('AC')] = row['TYPE AVION']
        vol_occas_val[cols_bd.index('REG')] = row['REG']
        vol_occas_val[cols_bd.index('DEP')] = row['PROV']
        vol_occas_val[cols_bd.index('ARR')] = row['DEST']
        vol_occas_val[cols_bd.index('STD')] = row['HEURE DEP']
        vol_occas_val[cols_bd.index('STA')] = row['HEURE ARR']
        vol_occas_val[cols_bd.index('ESCALE (IATA)')] = row['ESCALE (IATA)']
        vol_occas_val = pd.Series(vol_occas_val, index = bd_df.columns)
        bd_df = bd_df.append(vol_occas_val, ignore_index = True)

df_to_postgres(bd_df, con, cursor, engine, 'FLIGHT_FI')