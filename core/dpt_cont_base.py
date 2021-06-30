import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine
import time
# from chv import df_to_postgres

con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
con.autocommit = True
engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
cursor = con.cursor()

start_time = time.time()

def df_to_base(file):
    df = pd.read_excel('OCCAS/' + file, index_col = None)
    # df = pd.read_csv(file)
    df.dropna(subset = ['ACT DTE ARR'], inplace = True)
    df.insert(0, 'KEY_FLT', range(1, 1 + len(df)))
    cols = df.columns.to_list()
    df_cols = cols[-1:] + cols[:-1]
    df = df[df_cols]
    df = df.iloc[: , 1:]
    return df

if engine.dialect.has_table(engine, 'FLIGHT_OCCAS'):
    bd_df = pd.read_sql('SELECT * FROM "FLIGHT_OCCAS"', con)

print("--- %s sec ---" % (time.time() - start_time))