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

df = pd.read_excel('ah.xlsx', sheet_name = 'FICHE TOUCHEE')
chv.df_to_postgres(df, con, cursor, engine, 'FICHE_TOUCHEE')
with engine.connect() as conn:
    conn.execute('ALTER TABLE public."FICHE_TOUCHEE" ADD PRIMARY KEY "N° FICHE";')