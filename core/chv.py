import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np
import re, os
import datetime
import time
from datetime import date, timedelta, datetime

days_code=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

start_time = time.time()
# con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
# con.autocommit = True
# engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
# if engine.dialect.has_table(engine, 'FLIGHT'):
#     bd_df = pd.read_sql('SELECT * FROM "FLIGHT"', con)

# ******************** FI **************************************************************************************************
def sort_df(df, att):
    """
    Takes a DataFrame and a column (must contain int), sort on the column and return the new sorted DataFrame. 
    """
    # print(df[att].str.extract(r'(\d+)', expand=False))
    df['sort'] = df[att].str.extract(r'(\d+)', expand=False).astype('float64')
    df.sort_values('sort',inplace=True, ascending=True)
    df = df.drop('sort', axis=1)
    return df

#fonction qui retourne la date a partir nom fichier 
def file_date(a):
    c='-'.join([a[3:][:2], a[3:][2:4], a[3:][4:6]])
    d=':'.join([a[3:][6:8], a[3:][8:10]])
    e=c+" "+d
    date_time_obj = datetime.strptime(e, '%d-%m-%y %H:%M')
    return date_time_obj

def src_to_df(file):
    """
    Take the source file as entry and return a dataframe.
    """
    FILE = 'FIs/' + file
    df = pd.read_csv(FILE, skiprows=4, names=['ssim_data'])
    df['DATE'] = df['ssim_data'].map(lambda x: x[0:8], na_action=None)
    df['ROUTE_AC'] = df['ssim_data'].map(lambda x: x[10:14], na_action=None)
    df['FLT'] = df['ssim_data'].map(lambda x: x[17:25].replace(' ', ''), na_action=None)
    df['TYPE'] = df['ssim_data'].map(lambda x: x[29:30], na_action=None)
    df['REG'] = df['ssim_data'].map(lambda x: x[34:40].replace('-', ''), na_action=None)
    df['FC'] = df['ssim_data'].map(lambda x: x[48:50], na_action=None)
    df['AC'] = df['ssim_data'].map(lambda x: x[52:56], na_action=None)
    df['CHR'] = df['ssim_data'].map(lambda x: x[58:60], na_action=None)
    df['DEP'] = df['ssim_data'].map(lambda x: x[65:68], na_action=None)
    df['ARR'] = df['ssim_data'].map(lambda x: x[71:74], na_action=None)
    df['STD'] = df['ssim_data'].map(lambda x: x[77:82], na_action=None)
    df['STA'] = df['ssim_data'].map(lambda x: x[84:89], na_action=None)
    df['ETD'] = df['ssim_data'].map(lambda x: x[91:96], na_action=None)
    df['ETA'] = df['ssim_data'].map(lambda x: x[98:103], na_action=None)
    df['TKof'] = df['ssim_data'].map(lambda x: x[105:110], na_action=None)
    df['TDwn'] = df['ssim_data'].map(lambda x: x[112:117], na_action=None)
    df['ST'] = df['ssim_data'].map(lambda x: x[119:122].replace(' ', ''), na_action=None)
    df['ATD'] = df['ssim_data'].map(lambda x: x[123:128], na_action=None)
    df['ATA'] = df['ssim_data'].map(lambda x: x[130:135], na_action=None)
    df['BLOCK'] = df['ssim_data'].map(lambda x: x[137:142], na_action=None)
    df['FLThr'] = df['ssim_data'].map(lambda x: x[147:152], na_action=None)
    df['C1'] = df['ssim_data'].map(lambda x: x[157:160].replace(' ', ''), na_action=None)
    df['DLY1'] = df['ssim_data'].map(lambda x: x[163:168], na_action=None)
    df['Sub1'] = df['ssim_data'].map(lambda x: x[171:175], na_action=None)
    df['C2'] = df['ssim_data'].map(lambda x: x[176:179].replace(' ', ''), na_action=None)
    df['DLY2'] = df['ssim_data'].map(lambda x: x[182:187], na_action=None)
    df['Sub2'] = df['ssim_data'].map(lambda x: x[190:194], na_action=None)
    df['C3'] = df['ssim_data'].map(lambda x: x[195:198].replace(' ', ''), na_action=None)
    df['DLY3'] = df['ssim_data'].map(lambda x: x[201:206], na_action=None)
    df['Sub3'] = df['ssim_data'].map(lambda x: x[209:213], na_action=None)
    df['C4'] = df['ssim_data'].map(lambda x: x[214:217].replace(' ', ''), na_action=None)
    df['DLY4'] = df['ssim_data'].map(lambda x: x[220:225], na_action=None)
    df['Sub4'] = df['ssim_data'].map(lambda x: x[228:232], na_action=None)
    df['C5'] = df['ssim_data'].map(lambda x: x[233:236].replace(' ', ''), na_action=None)
    df['DLY5'] = df['ssim_data'].map(lambda x: x[239:244], na_action=None)
    df['Sub5'] = df['ssim_data'].map(lambda x: x[247:251], na_action=None)
    df['C6'] = df['ssim_data'].map(lambda x: x[252:255].replace(' ', ''), na_action=None)
    df['DLY6'] = df['ssim_data'].map(lambda x: x[258:263], na_action=None)
    df['Sub6'] = df['ssim_data'].map(lambda x: x[266:270], na_action=None)
    df['C7'] = df['ssim_data'].map(lambda x: x[271:274].replace(' ', ''), na_action=None)
    df['DLY7'] = df['ssim_data'].map(lambda x: x[277:282], na_action=None)
    df['Sub7'] = df['ssim_data'].map(lambda x: x[285:289], na_action=None)
    df['C8'] = df['ssim_data'].map(lambda x: x[290:293].replace(' ', ''), na_action=None)
    df['DLY8'] = df['ssim_data'].map(lambda x: x[296:301], na_action=None)
    df['Sub8'] = df['ssim_data'].map(lambda x: x[304:308], na_action=None)
    df['C1A'] = df['ssim_data'].map(lambda x: x[309:312].replace(' ', ''), na_action=None)
    df['DLY1A'] = df['ssim_data'].map(lambda x: x[315:320], na_action=None)
    df['Sub9'] = df['ssim_data'].map(lambda x: x[323:327], na_action=None)
    df['C2A'] = df['ssim_data'].map(lambda x: x[328:331].replace(' ', ''), na_action=None)
    df['DLY2A'] = df['ssim_data'].map(lambda x: x[334:339], na_action=None)
    df['Sb10'] = df['ssim_data'].map(lambda x: x[342:346], na_action=None)
    df['Cargo'] = df['ssim_data'].map(lambda x: x[347:353].replace(' ', ''), na_action=None)
    df['Mail'] = df['ssim_data'].map(lambda x: x[357:363].replace(' ', ''), na_action=None)
    df['Payld'] = df['ssim_data'].map(lambda x: x[367:373].replace(' ', ''), na_action=None)
    df['Bags'] = df['ssim_data'].map(lambda x: x[377:383].replace(' ', ''), na_action=None)
    df['EXP PAX F'] = df['ssim_data'].map(lambda x: x[387:407].split('|', 4)[0] if len(x[387:407].split('|', 4)) > 1 else x[387:407].split('|', 4)[0], na_action=None)
    df['EXP PAX C'] = df['ssim_data'].map(lambda x: x[387:407].split('|', 4)[1] if len(x[387:407].split('|', 4)) > 1 else x[387:407].split('|', 4)[0], na_action=None)
    df['EXP PAX Y'] = df['ssim_data'].map(lambda x: x[387:407].split('|', 4)[2] if len(x[387:407].split('|', 4)) > 1 else x[387:407].split('|', 4)[0], na_action=None)
    df['EXP PAX INF'] = df['ssim_data'].map(lambda x: x[387:407].split('|', 4)[3] if len(x[387:407].split('|', 4)) > 1 else x[387:407].split('|', 4)[0], na_action=None)
    df['ACT PAX F'] = df['ssim_data'].map(lambda x: x[408:428].split('|', 4)[0] if len(x[408:428].split('|', 4)) > 1 else x[408:428].split('|', 4)[0], na_action=None)
    df['ACT PAX C'] = df['ssim_data'].map(lambda x: x[408:428].split('|', 4)[1] if len(x[408:428].split('|', 4)) > 1 else x[408:428].split('|', 4)[0], na_action=None)
    df['ACT PAX Y'] = df['ssim_data'].map(lambda x: x[408:428].split('|', 4)[2] if len(x[408:428].split('|', 4)) > 1 else x[408:428].split('|', 4)[0], na_action=None)
    df['ACT PAX INF'] = df['ssim_data'].map(lambda x: x[408:428].split('|', 4)[3] if len(x[408:428].split('|', 4)) > 1 else x[408:428].split('|', 4)[0], na_action=None)
    df['EXP TTL'] = df['ssim_data'].map(lambda x: x[429:433].replace(' ', ''), na_action=None)
    df['PAX TTL'] = df['ssim_data'].map(lambda x: x[440:444].replace(' ', ''), na_action=None)
    df['SEATS TTL'] = df['ssim_data'].map(lambda x: x[451:458].replace(' ', ''), na_action=None)
    df['LF %'] = df['ssim_data'].map(lambda x: x[462:466].replace(' ', ''), na_action=None)
    df['AC CONFIG1'] = df['ssim_data'].map(lambda x: x[467:488].split()[0] if len(x[467:488].split()) > 1 else "", na_action=None)
    df['AC CONFIG2'] = df['ssim_data'].map(lambda x: x[467:488].split()[1] if len(x[467:488].split()) > 1 else "", na_action=None)
    df['AC CONFIG3'] = df['ssim_data'].map(lambda x: x[467:488].split()[2] if len(x[467:488].split()) > 1 else "", na_action=None)
    df['AC CONFIG4'] = df['ssim_data'].map(lambda x: x[467:488].split()[3] if len(x[467:488].split()) > 1 else "", na_action=None)
    df['Log_Page#'] = df['ssim_data'].map(lambda x: x[488:492].replace(' ', ''), na_action=None)
    df['Character Seats F'] = df['ssim_data'].map(lambda x: x[499:517].split()[0] if len(x[499:517].split()) > 1 else "", na_action=None)
    df['Character Seats C'] = df['ssim_data'].map(lambda x: x[499:517].split()[1] if len(x[499:517].split()) > 1 else "", na_action=None)
    df['Character Seats Y'] = df['ssim_data'].map(lambda x: x[499:517].split()[2] if len(x[499:517].split()) > 1 else "", na_action=None)
    df['Character Seats INF'] = df['ssim_data'].map(lambda x: x[499:517].split()[3] if len(x[499:517].split()) > 1 else "", na_action=None)
    df['Code Share and Seats F'] = df['ssim_data'].map(lambda x: x[520:542].split()[0] if len(x[520:542].split()) > 1 else "", na_action=None)
    df['Code Share and Seats C'] = df['ssim_data'].map(lambda x: x[520:542].split()[1] if len(x[520:542].split()) > 1 else "", na_action=None)
    df['Code Share and Seats Y'] = df['ssim_data'].map(lambda x: x[520:542].split()[2] if len(x[520:542].split()) > 2 else "", na_action=None)
    df['Code Share and Seats INF'] = df['ssim_data'].map(lambda x: x[520:542].split()[3] if len(x[520:542].split()) > 2 else "", na_action=None)
    df['Dist'] = df['ssim_data'].map(lambda x: x[546:554].replace(' ', ''), na_action=None)
    df['DStand'] = df['ssim_data'].map(lambda x: x[556:564].replace(' ', ''), na_action=None)
    df['AStand'] = df['ssim_data'].map(lambda x: x[563:571].replace(' ', ''), na_action=None)
    df['Change reason'] = df['ssim_data'].map(lambda x: x[570:594].replace(' ', ''), na_action=None)
    df['Init'] = df['ssim_data'].map(lambda x: x[596:605].replace(' ', ''), na_action=None)
    df['Uplf W'] = df['ssim_data'].map(lambda x: x[606:615].replace(' ', ''), na_action=None)
    df['Ramp'] = df['ssim_data'].map(lambda x: x[616:625].replace(' ', ''), na_action=None)
    df['Stdn'] = df['ssim_data'].map(lambda x: x[626:635].replace(' ', ''), na_action=None)
    df['Burn'] = df['ssim_data'].map(lambda x: x[636:645].replace(' ', ''), na_action=None)
    df['Uplf V'] = df['ssim_data'].map(lambda x: x[646:655].replace(' ', ''), na_action=None)
    df['USG/LTS'] = df['ssim_data'].map(lambda x: x[656:664].replace(' ', ''), na_action=None)
    df['Tank'] = df['ssim_data'].map(lambda x: x[666:675].replace(' ', ''), na_action=None)
    df['ZFW'] = df['ssim_data'].map(lambda x: x[676:685].replace(' ', ''), na_action=None)
    df['FPBurn'] = df['ssim_data'].map(lambda x: x[686:695].replace(' ', ''), na_action=None)
    df['SGrav'] = df['ssim_data'].map(lambda x: x[696:706].replace(' ', ''), na_action=None)
    df['Miles'] = df['ssim_data'].map(lambda x: x[706:715].replace(' ', ''), na_action=None)
    df['Rt base'] = df['ssim_data'].map(lambda x: x[716:724].replace(' ', ''), na_action=None)
    df['DGate'] = df['ssim_data'].map(lambda x: x[725:734].replace(' ', ''), na_action=None)
    df['AGate'] = df['ssim_data'].map(lambda x: x[732:741].replace(' ', ''), na_action=None)
    df['Orig.ARR Station'] = df['ssim_data'].map(lambda x: x[739:747].replace(' ', ''), na_action=None)
    df['D.Closed'] = df['ssim_data'].map(lambda x: x[749:759].replace(' ', ''), na_action=None)
    df['ch_type_app'] = ''
    df['ch_std'] = ''
    df['ch_dest'] = ''
    df['ch_config'] = ''
    # fi = re.search('(.+?).txt', FILE.replace('FIs/', '')).group(1).replace('FI_', '')
    # dt = '20' + fi[4:6] + '-' + fi[2:4] + '-' + fi[0:2] + ' ' + fi[6:8] + ':' + fi[8:]
    # df['FI_FILE'] = re.search('(.+?).txt', FILE.replace('FIs/', '')).group(1)
    # df['FI_FILE'] = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M')
    df['FI_FILE'] = file_date(file)
    df['KEY_FLT'] = df['DATE'].str.replace('/', '') + df['FLT'].replace(' ', '') + df['DEP']
    df['STATUS'] = '/'
    df['OCCAS'] = '/'
    df['ESCALE (IATA)'] = ''
    cols_df = df.columns.to_list()
    cols = cols_df[-4:] + cols_df[:-4]
    df = df[cols]
    # df['Crew'] = df['ssim_data'].map(lambda x: x[760:800], na_action=None)
    df.drop(['ssim_data'], axis=1, inplace=True)
    df.drop(df[df.FLT.str.len() < 3].index, inplace=True)
    #df.to_csv('FI_1004212315.csv', index=False)
    df = sort_df(df, 'KEY_FLT')
    return df

def df_to_postgres(df, con, cursor, engine, tab_name):
    if tab_name.startswith('FLIGHT'):
        pk = '("KEY_FLT")'
    elif tab_name.startswith('CHG'):
        pk = '("ID", "KEY_FLT")'
    else:
        pk = '("' + df.columns.to_list()[0] + '")'
    if engine.dialect.has_table(engine, tab_name):
        df_new = df
        if tab_name.startswith('CHG'):
            df_old = pd.read_sql('SELECT * FROM public."' + tab_name + '";', con)
            # print('requete -> OK')
            df_old = df_old.drop(['ID'], axis=1)
            # print('drop -> OK')
            df_new = df_old.append(df)
            # print('append -> OK')
            df_new.insert(0, 'ID', range(1, 1 + len(df_new)))
            # print('insert -> OK')
            # cur = con.cursor()
            # cur.execute('''TRUNCATE TABLE public''')
        with engine.connect() as conn:
            conn.execute('TRUNCATE TABLE public."' + tab_name + '"')
        # print('truncate -> OK')
        df_new.to_sql(tab_name, engine, if_exists='replace', index=False)
        # print('table ' + tab_name + ' modifier')
    else:
        if tab_name.startswith('CHG'):
            df.insert(0, 'ID', range(1, 1 + len(df)))
        df.to_sql(tab_name, engine, if_exists='replace', index=False)
        # print('table ' + tab_name + ' cree')
    with engine.connect() as conn:
        conn.execute('ALTER TABLE public."' + tab_name + '" ADD PRIMARY KEY ' + pk + ';')

#fonction qui retourne le dataframe des vols modifié avec les columns associé
def fi_modifie(df_new,df_old):
    s1 = pd.merge(df_old, df_new, how='inner', on=['KEY_FLT'])
    s1["ch_type_app"]=None#AC
    s1["ch_std"]=None#STD
    s1["ch_dest"]=None#ARR
    s1["ch_config"]=None
    #AC CONFIG1
    #AC CONFIG2
    #AC CONFIG3
    #AC CONFIG4
    for index, row in s1.iterrows():
        if (row["AC_x"]!=row["AC_y"]):
            s1.loc[index,"STATUS_x"]="MODIFIED"
            s1.loc[index,"ch_type_app"]=row["FI_FILE_y"]
        if (row["STD_x"]!=row["STD_y"]):
            s1.loc[index,"STATUS_x"]="MODIFIED"
            s1.loc[index,"ch_std"]=row["FI_FILE_y"]
        if (row["ARR_x"]!=row["ARR_y"]):
            s1.loc[index,"STATUS_x"]="MODIFIED"
            s1.loc[index,"ch_dest"]=row["FI_FILE_y"]
        if (row["AC CONFIG1_x"]!=row["AC CONFIG1_y"] or row["AC CONFIG2_x"]!=row["AC CONFIG2_y"] or row["AC CONFIG3_x"]!=row["AC CONFIG3_y"] or row["AC CONFIG4_x"]!=row["AC CONFIG4_y"]):
            s1.loc[index,"STATUS_x"]="MODIFIED"
            s1.loc[index,"ch_config"]=row["FI_FILE_y"]
    fi_chg = s1.loc[s1['STATUS_x'] == 'MODIFIED'][["KEY_FLT", "STATUS_x","ch_type_app","ch_std","ch_dest","ch_config","STD_x","STD_y","AC_x","AC_y","ARR_x","ARR_y","AC CONFIG1_x","AC CONFIG1_y","AC CONFIG2_x","AC CONFIG2_y","AC CONFIG3_x","AC CONFIG3_y","AC CONFIG4_x","AC CONFIG4_y"]]
    vol_fi_modifie = s1.loc[s1['STATUS_x'] == 'MODIFIED'][["KEY_FLT", "STATUS_x","ch_type_app","ch_std","ch_dest","ch_config"]]
    fi_chg.dropna(subset = ['ch_type_app', 'ch_std', 'ch_dest', 'ch_config'], how = 'all', inplace = True)
    vol_fi_modifie.dropna(subset = ['ch_type_app', 'ch_std', 'ch_dest', 'ch_config'], how = 'all', inplace = True)
    return fi_chg,vol_fi_modifie

#fonction qui retourne le dataframe des vols modifié avec les columns associé
def ssim_modifie(df_new,df_old):
    df_2 = pd.merge(df_old, df_new, how='inner', on=['KEY_FLT'])
    df_2["ch_type_app"]=""#Aircraft_Type
    df_2["ch_std"]=""#STD_UTC
    df_2["ch_dest"]=""#Arrival_Station
    df_2["ch_config"]=""
    #Aircraft_Configuration
    for index, row in df_2.iterrows():
        if (row["Aircraft_Type_x"]!=row["Aircraft_Type_y"]):
            df_2.loc[index,"STATUS_x"]="MODIFIE"
            df_2.loc[index,"ch_type_app"]=df_2.loc[index,"ssim_period_y"]
        if (row["STD_UTC_x"]!=row["STD_UTC_y"]):
            df_2.loc[index,"STATUS_x"]="MODIFIE"
            df_2.loc[index,"ch_std"]=df_2.loc[index,"ssim_period_y"]
        if (row["Arrival_Station_x"]!=row["Arrival_Station_y"]):
            df_2.loc[index,"STATUS_x"]="MODIFIE"
            df_2.loc[index,"ch_dest"]=df_2.loc[index,"ssim_period_y"]
        if (row["Aircraft_Configuration_x"]!=row["Aircraft_Configuration_y"]):
            df_2.loc[index,"STATUS_x"]="MODIFIE"
            df_2.loc[index,"ch_config"]=df_2.loc[index,"ssim_period_y"]
    
    
    df_2 = df_2.loc[df_2['STATUS_x'] == 'MODIFIE'][["KEY_FLT", "STATUS_x","ch_type_app","ch_std","ch_dest","ch_config","Aircraft_Type_x","Aircraft_Type_y","STD_UTC_x","STD_UTC_y","Arrival_Station_x","Arrival_Station_y","Aircraft_Configuration_x","Aircraft_Configuration_y"]]
    ssim_modif = df_2.loc[df_2['STATUS_x'] == 'MODIFIE'][["KEY_FLT", "STATUS_x","ch_type_app","ch_std","ch_dest","ch_config"]]
    # df_2.dropna(subset = ['ch_type_app', 'ch_std', 'ch_dest', 'ch_config'], how = 'all', inplace = True)
    # ssim_modif.dropna(subset = ['ch_type_app', 'ch_std', 'ch_dest', 'ch_config'], how = 'all', inplace = True)
    df_2 = df_2.drop(df_2[(df_2['ch_type_app'] == '') & (df_2['ch_std'] == '') & (df_2['ch_dest'] == '') & (df_2['ch_config'] == '')].index)
    ssim_modif = ssim_modif.drop(ssim_modif[(ssim_modif['ch_type_app'] == '') & (ssim_modif['ch_std'] == '') & (ssim_modif['ch_dest'] == '') & (ssim_modif['ch_config'] == '')].index)
    return df_2,ssim_modif

# Fct gestion chevauchement FI & DB
def gestion_chev(con, engine, bd_df, df, tab_flt, tab_chg):
    cols_bd = bd_df.columns.to_list()
    cols_df = df.columns.to_list()
    for col1, col2 in zip(cols_bd, cols_df):
        if str(bd_df[col1].dtype) != str(df[col2].dtype):
            df[col2] = df[col2].astype(object)
    # gestion vols canceled
    common = bd_df.merge(df, on=['KEY_FLT'])
    pd.set_option('display.max_rows', None)
    if tab_flt.endswith('FI'):    
        min = common['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype(int)[0]
        max = common['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype(int)[-1:].tolist()[0]
    else:
        min = common['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64')[0]
        max = common['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64')[-1:].tolist()[0]
    
    inter_bd = bd_df[(bd_df['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64') <= max) & (bd_df['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64') >= min)]
    cnl_df = inter_bd[~inter_bd['KEY_FLT'].isin(common['KEY_FLT'])]
    for idx, row in cnl_df.iterrows():
        bd_df.at[idx, 'STATUS'] = 'CANCELED'
    # ajout des new vols
    max_bd = bd_df['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64')[-1:].tolist()[0]
    new_df = df[df['KEY_FLT'].str.extract(r'(\d+)', expand=False).astype('float64') > max_bd]
    bd_df = pd.concat([bd_df, new_df])
    bd_df = sort_df(bd_df, 'KEY_FLT')
    # gestion des modif
    if tab_flt.endswith('FI'):    
        chg_df, edit_df = fi_modifie(df, bd_df)
    else:
        chg_df, edit_df = ssim_modifie(df, bd_df)
    for idx, row in edit_df.iterrows():
        bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'STATUS'] = 'MODIFIED'
        bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'ch_type_app'] = edit_df.at[idx, 'ch_type_app']
        bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'ch_std'] = edit_df.at[idx, 'ch_std']
        bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'ch_dest'] = edit_df.at[idx, 'ch_dest']
        bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'ch_config'] = edit_df.at[idx, 'ch_config']
        if tab_flt.endswith('FI'):    
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'STD'] = chg_df.at[idx, 'STD_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'AC'] = chg_df.at[idx, 'AC_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'ARR'] = chg_df.at[idx, 'ARR_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'AC CONFIG1'] = chg_df.at[idx, 'AC CONFIG1_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'AC CONFIG2'] = chg_df.at[idx, 'AC CONFIG2_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'AC CONFIG3'] = chg_df.at[idx, 'AC CONFIG3_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'AC CONFIG4'] = chg_df.at[idx, 'AC CONFIG4_y']
        else:
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'Aircraft_Type'] = chg_df.at[idx, 'Aircraft_Type_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'STD_UTC'] = chg_df.at[idx, 'STD_UTC_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'Arrival_Station'] = chg_df.at[idx, 'Arrival_Station_y']
            bd_df.at[int(bd_df.loc[bd_df.KEY_FLT == row.KEY_FLT].index.values), 'Aircraft_Configuration'] = chg_df.at[idx, 'Aircraft_Configuration_y']
    # MAJ de la BD
    cursor = con.cursor()
    df_to_postgres(bd_df, con, cursor, engine, tab_flt)
    df_to_postgres(chg_df, con, cursor, engine, tab_chg)
    return bd_df

## TEST FI ##

# df1 = src_to_df(os.listdir('FIs')[1])    # role de la BD
# df2 = src_to_df(os.listdir('FIs')[2])
# df1, df2 = fi_modifie(df2, df1)
# pd.set_option('display.max_rows', None)
# print(df1)
# for file in os.listdir('FIs')[1:]:
#     print('BD file shape: ' + str(tuple(df1.shape)))
#     df2 = src_to_df(file)    # role du nv FI entrant
#     print('New FI FILE file "' + file + '" shape: ' + str(tuple(df2.shape)))
#     df1 = gestion_chev(con, engine, df1, df2, 'FLIGHT_FI', 'CHG_FI')
# con.close()


print("--- %s sec ---" % (time.time() - start_time))