from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from connect import connect_tcp_socket
from statsmodels.tsa.arima.model import ARIMA
from scipy.stats import weibull_min
from datetime import datetime, timedelta
import json

engine = connect_tcp_socket()

with engine.connect() as con:
    df = pd.read_sql('SELECT * FROM windspeed ORDER BY datetime DESC LIMIT 10', con).iloc[::-1]
    dfts = pd.read_sql('SELECT * FROM armaparameters ORDER BY datetime DESC LIMIT 10', con).iloc[::-1]
    dfw = pd.read_sql('select * from weibullparameters ORDER BY datetime DESC LIMIT 10', con).iloc[::-1]

def power(my_list):
    return [ x**3 for x in my_list ]

def plot_prediction(a):

    model = ARIMA(df['turbine_{}'.format(a)], order=json.loads(dfts['model_order'].iloc[a-1]))
    model = model.fit()

    prediction = model.forecast(steps=6)
    time_index = [df['datetime'].iloc[-1]  + timedelta(hours=i) for i in range (1, 7)]

    fig = make_subplots(rows=4, cols=2,
                        horizontal_spacing=0.1,
                        vertical_spacing=0.1,
                        column_widths=[0.85, 0.15],
                        specs=[ [{'type':'xy'}, {'type':'domain'}],
                                [{'type':'xy'}, {'type':'domain'}],
                                [{'type':'xy'}, {'type':'domain'}],
                                [{'colspan':2}, None] ],
                        subplot_titles=("Speed", "", "Power Density", "", "Distribution", "", "Residuals"))

    fig.add_trace(go.Scatter(x=time_index, y=prediction,
                    mode='lines'), 
                    row=1, col=1)

    fig.add_trace(go.Indicator(
        value = np.max(prediction),
        gauge = {
            'shape': "bullet",
            'axis' : {'visible': False}},
            title = {'text': "Max Speed m/s<br>(6h forecast)"}),
        row=1, col=2)

    fig.add_trace(go.Scatter(x=time_index, y=power(prediction),
                    mode='lines'),
                    row=2, col=1)

    fig.add_trace(go.Indicator(
        value = np.max(power(prediction)),
        gauge = {
            'shape': "bullet",
            'axis' : {'visible': False}},
            title = {'text': "Max Power density W/m²<br>(6h forecast)"}),
        row=2, col=2)

    fig.add_trace(go.Scatter(x=np.linspace(0, 20, 200), y=weibull_min.pdf(np.linspace(0, 20, 200), dfw['shape'].iloc[a], dfw['loc'].iloc[a], dfw['scale'].iloc[a]),
                        mode='lines'),
                        row=3, col=1)

    fig.add_trace(go.Indicator(
        value = dfw['median'].iloc[a],
        gauge = {
            'shape': "bullet",
            'axis' : {'visible': False}},
            title = {'text': "Median (m/s)"}),
        row=3, col=2)

    fig.add_trace(go.Scatter(x=df['datetime'].iloc[-6:,], y=model.resid[-6:,],
                    mode='lines'),
                    row=4, col=1)
    
    fig.update_layout(showlegend=False)
    

    fig.update_layout(height=1000, width=1200, title_text='Turbine {}'.format(a))

    return fig

fig = plot_prediction(1)

def create_dash_application(flask_app):
    dash_app = Dash(external_stylesheets=[dbc.themes.MINTY], server=flask_app, name="Operational Metrics", url_base_pathname="/")
    dash_app.layout = html.Div([
            html.H1(children="Operational Metrics", style={'textAlign': 'center'}),
            dcc.Graph(id="pred_graph", figure=fig),
            html.Div(children='Select a turbine'),
            dcc.Dropdown(np.arange(1, 11, 1), 1, id='turbine'),
        ]
    )
    @dash_app.callback(
        Output('pred_graph', 'figure'),
        Input('turbine', 'value')
)
    def update_output(value):
        fig = plot_prediction(value)
        return fig

    return dash_app



