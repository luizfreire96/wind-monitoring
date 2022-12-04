import numpy as np
import pandas as pd
from connect import connect_tcp_socket
from scipy import stats

engine = connect_tcp_socket()

with engine.connect() as con:
    df = pd.read_sql('''SELECT * FROM windspeed ORDER BY datetime DESC LIMIT 1440 ''', con)

df = df.iloc[::-1]

parameters = []
a = 0
for i in range (1, 11, 1):
  parameters.append(stats.weibull_min.fit(df['turbine_{}'.format(i)], 2))
for i in range(len(parameters)):
  while True:
    if parameters[i][2] < 6:
      a = a + 0.1
      parameters[i] = stats.weibull_min.fit(df['turbine_{}'.format(i)], 2+a)
    else:
      break
weibull_median = []
for i in parameters:
    weibull_median.append(stats.weibull_min.median(i[0], i[1], i[2]))

time = df['datetime'].iloc[-1]

for i in range(1,11):
  with engine.connect() as con:
    con.execute("insert into weibullparameters values ('{}', {}, {}, {}, {}, {})".format(time, parameters[i-1][0], parameters[i-1][1], parameters[i-1][2], weibull_median[i-1], i))

print('ok')