# import pandas as pd
# import numpy as np
# import os
# import psycopg2
# from sqlalchemy import create_engine
# import chv

# con = psycopg2.connect(database="AH_DB", user="postgres", password="zaki1690", host="localhost", port="5432")
# con.autocommit = True
# engine = create_engine('postgresql://postgres:zaki1690@localhost:5432/AH_DB')
# cursor = con.cursor()


dic = {
    'bag_weight': [10, 9, 8],
    'bag_brand' : ['SENSONITE', 'TravelPro', 'AKIROO'],
    'bag_details': ['rouge coté', 'bleu ciel', 'Gris xv']
}
idx = 0
st_dic = dict()
for key, value in dic.items():
    st_dic[key] = value[idx]
print(st_dic)