import pandas as pd
from pmdarima.arima import auto_arima
from connect import connect_tcp_socket
import json

engine = connect_tcp_socket()

with engine.connect() as con:
    query = 'SELECT * FROM windspeed ORDER BY datetime DESC LIMIT 1440'
    df = pd.read_sql(query, con)

df = df[::-1]

models = []
for i in range(1, 11):
    models.append(auto_arima(df['turbine_{}'.format(i)], start_p=1, d=0, start_q=1, max_p=3, max_q=3))

time = df['datetime'].iloc[-1]

orders = []
params = []

for i in models:
    a = i.order
    orders.append(json.dumps(a))


for i in range(1, 11):
    with engine.connect() as con:
        query = "insert into armaparameters values ('{}', '{}', '{}')"
        con.execute(query.format(time, orders[i-1], i))

print('ok')
