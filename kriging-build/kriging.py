from pykrige.ok import OrdinaryKriging
import pandas as pd
import math
from connect import connect_tcp_socket

engine = connect_tcp_socket()

sdf = pd.read_csv('./Site-location.csv')  # Coordinates of each turbine.
df = pd.read_csv('./WindSpeedTest.csv')  # Test Dataframe of speed of each turbine.

with engine.connect() as con:
    last_row = con.execute('''SELECT COUNT (turbine_1) FROM windspeed''')
    last_row = last_row.first()[0]

sensor_data = df.drop(columns='DateTime').iloc[last_row]  # Row of test Dataframe that will be added to DB
time = df.DateTime.iloc[last_row]

nan_locs = []

x = []
y = []
z = []

xu = []
yu = []

for i in range(len(sensor_data)):
    if math.isnan(sensor_data[i]) is False:
        x.append(sdf.iloc[i][1])
        y.append(sdf.iloc[i][2])
        z.append(sensor_data[i])
    else:
        xu.append(sdf.iloc[i][1])
        yu.append(sdf.iloc[i][2])
        nan_locs.append(i)

OK = OrdinaryKriging(x, y, z, variogram_model='power')

for i in range(len(nan_locs)):
    sensor_data[nan_locs[i]] = OK.execute('points', xu, yu)[0].data[i]

keys = ['turbine_1', 'turbine_2', 'turbine_3', 'turbine_4', 'turbine_5',
        'turbine_6', 'turbine_7', 'turbine_8', 'turbine_9', 'turbine_10']

sensor_data = dict(zip(keys, sensor_data.T))
columns = ', '.join(list(sensor_data.keys()))
values = list(sensor_data.values())
values = ', '.join([str(i) for i in values])

query = "INSERT INTO windspeed ({}, datetime) VALUES ({}, '{}')".format(columns, values, time)

engine = connect_tcp_socket()
with engine.connect() as con:
    con.execute(query)
