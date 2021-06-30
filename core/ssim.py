import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np
import re, os
import datetime
import time
from datetime import date, timedelta, datetime
from .chv import gestion_chev

days_code=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

start_time = time.time()
# con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
# con.autocommit = True
# engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')

def sort_df(df, att):
    """
    Takes a DataFrame and a column (must contain int), sort on the column and return the new sorted DataFrame. 
    """
    # print(df[att].str.extract(r'(\d+)', expand=False))
    df['sort'] = df[att].str.extract(r'(\d+)', expand=False).astype('float64')
    df.sort_values('sort',inplace=True, ascending=True)
    df = df.drop('sort', axis=1)
    return df

def period_to_date(Start_period,End_period,day_num):
    weekDay = days_code[day_num-1]
    firstDay=datetime.strptime(Start_period,"%d%b%y").date()
    lastDay=datetime.strptime(End_period,"%d%b%y").date() 
    dates = [firstDay + timedelta(days=x) for x in range((lastDay-firstDay).days + 1) if (firstDay + timedelta(days=x)).weekday() == time.strptime(weekDay, '%A').tm_wday]
    return dates

#cle=0804211208ALG date +numero+Dep
def ssim_df(file):
    #change txt to dataframe
    # file = 'SSIMs/' + txt
    df=pd.read_csv(file ,skiprows=[0,1,2,3,6,7,8])
    df.columns = ['ssim_data']
    ssim_period=df.loc[0,"ssim_data"][14:28]
    df = df.drop(df.index[0:2])
    index_skip=[]
    for index, row in df.iterrows():   
        if ("00000000" in df.loc[index,"ssim_data"]):
            index_skip.append(index)
    df = df.drop(df.index[index_skip[0]:index+1])
    df['STATUS'] = '/'
    df["ssim_period"]=ssim_period
    df['index_commercial'] = df['ssim_data'].map(lambda x: x[0:1])
    df['ST_SSIM'] = df['ssim_data'].map(lambda x: x[1:2])
    df['Airline'] = df['ssim_data'].map(lambda x: x[2:4])
    df['Flight_Number']= df['ssim_data'].map(lambda x: x[5:9])
    df['Itinirary_Variation_Indicator']= df['ssim_data'].map(lambda x: x[9:11])
    df['Leg_Sequence_Number']= df['ssim_data'].map(lambda x: x[11:13])
    df['Service_Type']= df['ssim_data'].map(lambda x: x[13:14])
    df['Start_period']= df['ssim_data'].map(lambda x: x[14:21])
    #df['Month_start_period']= df['ssim_data'].map(lambda x: x[16:19])
    #df['Year_start_period']= df['ssim_data'].map(lambda x: x[19:21])
    df['End_period']= df['ssim_data'].map(lambda x: x[21:28])
    #df['Month_end_period']= df['ssim_data'].map(lambda x: x[23:26])
    #df['Year_end_period']= df['ssim_data'].map(lambda x: x[26:28])
    df['Monday']= df['ssim_data'].map(lambda x: x[28:29])
    df['Tuesday']= df['ssim_data'].map(lambda x: x[29:30])
    df['Wednesday']= df['ssim_data'].map(lambda x: x[30:31])
    df['Thursday']= df['ssim_data'].map(lambda x: x[31:32])
    df['Friday']= df['ssim_data'].map(lambda x: x[32:33])
    df['Saturday']= df['ssim_data'].map(lambda x: x[33:34])
    df['Sunday']= df['ssim_data'].map(lambda x: x[34:35])
    df['Departure_Station']= df['ssim_data'].map(lambda x: x[36:39])
    df['PAX_STD_UTC']= df['ssim_data'].map(lambda x: x[39:43])
    #essayer de eliminer cette line si ca se repete 
    df['STD_UTC']= df['ssim_data'].map(lambda x: x[43:47])
    df['STD_Variation_Sign']= df['ssim_data'].map(lambda x: x[47:48])
    df['STD_Variation_UTC']= df['ssim_data'].map(lambda x: x[48:52])
    df['Arrival_Station']= df['ssim_data'].map(lambda x: x[54:57])
    df['STA_UTC']= df['ssim_data'].map(lambda x: x[57:61])
    df['PAX_STA_UTC']= df['ssim_data'].map(lambda x: x[61:65])
    df['STA_Variation_Sign']= df['ssim_data'].map(lambda x: x[65:66])
    df['STA_Variation_UTC']= df['ssim_data'].map(lambda x: x[66:70])
    df['Aircraft_Type']= df['ssim_data'].map(lambda x: x[72:75])
    #we have to define this what is this
    df['fly_next_number']= df['ssim_data'].map(lambda x: x[137:144])
    #its too large no?
    df['Aircraft_Configuration']= df['ssim_data'].map(lambda x: x[172:192])
    df["fly_date"] = ""
    df["arrival_date"]=""
    df["vol_commercial_number"]=""
    df["vol_commercial_airline"]=""
    df["code_ssim"]=""
    df["STATUS"]=""

    del df['ssim_data']
    

    #  vol commercial
    vol= df.loc[df['index_commercial']=="4"]
    vol= vol.reset_index()
    vol=vol.rename(columns = {'index': 'ancien_ind'})

    list_index=[]
    # reformer les 3 champs des vol commercial
    for index, row in vol.iterrows():
        list_index.append(index)
        vol.loc[index,"code_ssim"]=row['Monday']+row['Tuesday']+row['Wednesday']+row['Thursday']+row['Friday']
        air_num=row["PAX_STD_UTC"]+row["STD_UTC"]
        vol.loc[index,"vol_commercial_number"]=air_num[3:7]
        vol.loc[index,"vol_commercial_airline"]=air_num[0:2]

    #ajout des vols commercial dans le df principal
    for index,row in vol.iterrows():
        index_nv=int(row["ancien_ind"])-1
        df.loc[index_nv,"vol_commercial_airline"]= vol.loc[index,"vol_commercial_airline"]
        df.loc[index_nv,"vol_commercial_number"]=  vol.loc[index,"vol_commercial_number"]
        df.loc[index_nv,"code_ssim"] =  vol.loc[index,"code_ssim"]


    #maintenat que on extrait info on elimine les ligne commercial
    df_1=df.loc[df['index_commercial'] == '3']

    #transformer les ligne periode en plusieur ligne dates
    for index, row in df_1.iterrows():
        code_dispo=[]
        #get the days code for a row in  a list
        for day in days_code:
            if(row[day]!=' '):
                code_dispo.append(int(row[day])) 
            #generate each code day betewenn start and end period
        for i in code_dispo:
            dates=period_to_date(row['Start_period'],row['End_period'],i)
            for date in dates:
                row_df = pd.DataFrame([row])
                row_df["fly_date"]=date
                row_df["day_op"]=i
                df_1 = pd.concat([row_df, df_1], ignore_index=True ,sort=False)

    # se debrasser des ligne periode maintenant que on a les ligne date     
    df_1=df_1.loc[(df_1['fly_date'] != '')]
    for index, row in df_1.iterrows():
        if(df_1.loc[index,"STD_UTC"] < df_1.loc[index,"STA_UTC"]):
            df_1.loc[index,"arrival_date"]=df_1.loc[index,"fly_date"]
        else:
            df_1.loc[index,"arrival_date"]=df_1.loc[index,"fly_date"] + timedelta(days=1)
            
        
        
        
        date=df_1.loc[index,"fly_date"]
        flight_num=df_1.loc[index,"Flight_Number"]
        if(flight_num[0]==' '):
            flight_num=flight_num[1:4]

        dep_stat=df_1.loc[index,"Departure_Station"]
        key = str(date.day).zfill(2)+str(date.month).zfill(2)+str(date.year)[2:4]+flight_num+dep_stat
        # found = 
        # df_1['SSIM_DATE'] = 
        df_1.loc[index,"KEY_FLT"]=key
        # cols_df = df_1.columns.to_list()
        # cols = cols_df[-1:] + cols_df[:-1]
        # df_1 = df_1[cols]
        df_1 = sort_df(df_1, 'KEY_FLT')
    return df_1

# fonction qui modifie la strucure du Dataframe pour le SSIM
def chg_struct(df1):
    df1.STATUS.replace(np.nan, '/', regex = True, inplace = True)
    cols_df = df1.columns.to_list()
    cols = cols_df[-1:] + cols_df[:-1]
    df1 = df1[cols]
    return df1

## TEST SSIM ## ----------------------------------------------------------------------------------------------------

# Getting all SSIM paths
# ssim_path = []
# for dirpath, dnames, fnames in os.walk("SSIMs/"):
#     ssim_path.append(dirpath)
# ssim_path.pop(0)

# df1 = ssim_df(ssim_path[0] + '/' + os.listdir(ssim_path[0])[0])
# df1 = chg_struct(df1)

# for file in ssim_path[1:]:
#     print('BD file shape: ' + str(tuple(df1.shape)))
#     df2 = ssim_df(file + '/' + os.listdir(file)[0])
#     df2 = chg_struct(df2)
#     print('New SSIM file "' + file + '" shape: ' + str(tuple(df2.shape)))
#     df1 = gestion_chev(con, engine, df1, df2, 'FLIGHT_SSIM', 'CHG_SSIM')

# con.close()
# print("--- %s sec ---" % (time.time() - start_time))

# flt_fi = pd.read_sql('SELECT * FROM "FLIGHT_FI"', con)
# flt_ssim = pd.read_sql('SELECT * FROM "FLIGHT_SSIM"', con)
# chg_fi = pd.read_sql('SELECT * FROM "CHG_FI"', con)
# chg_ssim = pd.read_sql('SELECT * FROM "CHG_SSIM"', con)
# flt_fi.to_csv('FLIGHT_FI.csv', index = False)
# chg_fi.to_csv('CHG_FI.csv', index = False)
# flt_ssim = pd.read_csv('FLIGHT_SSIM.csv')
# chg_ssim = pd.read_csv('CHG_SSIM.csv')
