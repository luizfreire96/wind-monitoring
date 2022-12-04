import numpy as np
from pykrige.ok import OrdinaryKriging
import pandas as pd
import math
from connect import connect_tcp_socket

engine = connect_tcp_socket()
sdf = pd.read_csv('./Site-location.csv')
df = pd.read_csv('./WindSpeedTest.csv')

with engine.connect() as con:
    nlinha = con.execute('''SELECT COUNT (turbine_1) FROM windspeed''')
    nlinha = nlinha.first()[0]

input = df.drop(columns='DateTime').iloc[nlinha] 
time = df.DateTime.iloc[nlinha]

nanlocs = []
x = []
xu = []
y = []
yu = []
z = []
for i in range(len(input)):
    if math.isnan(input[i]) == False:
        x.append(sdf.iloc[i][1])
        y.append(sdf.iloc[i][2])
        z.append(input[i])
    else:
        xu.append(sdf.iloc[i][1])
        yu.append(sdf.iloc[i][2])
        nanlocs.append(i)
OK = OrdinaryKriging(x,y,z,variogram_model='power')
for i in range(len(nanlocs)):
    input[nanlocs[i]] = OK.execute('points', xu, yu)[0].data[i]

keys = ['turbine_1', 'turbine_2', 'turbine_3', 'turbine_4', 'turbine_5', 'turbine_6', 'turbine_7', 'turbine_8', 'turbine_9', 'turbine_10']
input = dict(zip(keys, input.T))
columns = ', '.join(list(input.keys()))
values = list(input.values())
values = ', '.join([str(i) for i in values])

query = "INSERT INTO windSpeed ({}, datetime) VALUES ({}, '{}')".format(columns, values, time)

engine = connect_tcp_socket()
with engine.connect() as con:
    con.execute(query)