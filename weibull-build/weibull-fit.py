import pandas as pd
from connect import connect_tcp_socket
from scipy import stats

engine = connect_tcp_socket()

with engine.connect() as con:
    query = 'SELECT * FROM windspeed ORDER BY datetime DESC LIMIT 1440'
    df = pd.read_sql(query, con)

df = df[::-1]

parameters = []
a = 0

# The shape parameter is at least 2 according the exploratory analysis.
for i in range(1, 11, 1):
    parameters.append(stats.weibull_min.fit(df['turbine_{}'.format(i)], 2))

# To prevent the unrealistic fitting, the minimum loc parameter is set to 6.
for i in range(len(parameters)):
    while True:
        if parameters[i][2] < 6:
            a += 0.1
            parameters[i] = stats.weibull_min.fit(df['turbine_{}'.format(i)], 2+a)
        else:
            break

# The median is used due the skewness of the curve
weibull_median = []
for i in parameters:
    weibull_median.append(stats.weibull_min.median(i[0], i[1], i[2]))

time = df['datetime'].iloc[-1]

for i in range(1, 11):
    with engine.connect() as con:
        query = "insert into weibullparameters values ('{}', {}, {}, {}, {}, {})"
        con.execute(query.format(time,
                                 parameters[i-1][0],
                                 parameters[i-1][1],
                                 parameters[i-1][2],
                                 weibull_median[i-1],
                                 i))

print('ok')
