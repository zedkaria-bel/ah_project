import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine
import chv

con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
con.autocommit = True
engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
cursor = con.cursor()


df = pd.read_excel('TEST SUIVI AHL DPR.xlsx', sheet_name = 'Feuil1', skiprows=2)
df = df[df['DATES'].notna()]
df.DATES = pd.to_datetime(df.DATES,dayfirst=True)
df.insert(0, 'id', range(1, 1 + len(df)))
pd.set_option('display.max_rows', None)
print(df.columns)
# df.to_sql('BAG_MRD_TYPE_DMG', engine, if_exists='append', index=False)