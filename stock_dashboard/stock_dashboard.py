# Imports
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc

# Get symbols
symb = requests.get(
    "https://sandbox.iexapis.com/stable/ref-data/symbols?token=Tpk_804fb4beb488475387c5a97a24b78a72").json()
exchange = ['NSY']
# Filter by US exchange

symb_by_exchange = [d for d in symb if d['exchange'] in exchange]

sybs_options = []
for d in symb_by_exchange:
    d1 = {'label': d.get('symbol') + '/' + d.get('name'), 'value': d.get('symbol')}
    sybs_options.append(d1)

# External stylesheet
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = dbc.Container([html.Div([
    html.H1('Stock Ticker Dashboard'),
    dbc.Row([
        dbc.Col(html.Div([
            html.P('Select Stock Symbols:'),
            dcc.Dropdown(id='name-select',
                         options=sybs_options,
                         value=['AEL-A', 'AEO'],
                         multi=True)
        ])),
        dbc.Col(html.Div([
            html.P('Select start and end dates:'),
            dcc.DatePickerRange(id='date-range',
                                start_date=dt(2020, 1, 1),
                                min_date_allowed=dt(2005, 1, 1),
                                end_date=dt.today().date())
        ])),
        dbc.Col(html.Div([
            dbc.Button(id='submit-button',
                       n_clicks=0,
                       children='Submit',
                       className='mr-1',
                       color='primary',
                       size='lg')
        ]))
    ]),
    html.Div([
        dcc.Graph(id='stock-graph')
    ])

])])


# LEFT TO DO: GIVE STYLE TO THE DROPDOWNS AND INSTRUCTIONS, TUNE THE DATE RANGE PICKER

@app.callback(Output('stock-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('name-select', 'value'),
               State('date-range', 'start_date'),
               State('date-range', 'end_date')])
def update_graph(n_clicks, name, f0, f1):
    data = []
    for n in name:
        resp = requests.get(
            "https://sandbox.iexapis.com/stable/stock/{}/chart/max?chartCloseOnly=true&token=Tpk_804fb4beb488475387c5a97a24b78a72".format(
                n)).json()
        df = pd.DataFrame(resp, columns=['date', 'close'])
        df = df[(df['date'] >= f0) & (df['date'] <= f1)]
        trace = go.Scatter(x=df['date'],
                           y=df['close'],
                           name=n,
                           mode='lines')
        data.append(trace)
    layout = go.Layout(title='{} Closing Prices'.format(name))
    return go.Figure(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server()
