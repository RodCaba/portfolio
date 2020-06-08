import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests
import plotly.graph_objs as go
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username', 'password'],
                           ['JamesBond', '007']]

app = dash.Dash()
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server


app.layout = html.Div([
    html.Div([
        html.H1('Number of Active Flights according to FlightRadar24')
    ]),
    html.Div([
        html.Pre(id='counter-text',
                 children='Active Flights Worldwide'),
        dcc.Graph(id='live-update-graph',
                  style={'width': 1200}),
        dcc.Interval(id='interval-component',
                     interval=6000,
                     n_intervals=0)
    ])
])

counter_list = []

@app.callback(Output('counter-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?faa=1&mlat=1&flarm=1&adsb=1&gnd=&air=1&vehicles=1" \
          "&estimated=1&stats=1"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = res.json()
    counter = 0
    for element in data['stats']['total']:
        counter += data['stats']['total'][element]
    counter_list.append(counter)
    return "Active flights Worldwide: {}".format(counter)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    fig = go.Figure(data=[
        go.Scatter(x=list(range(len(counter_list))),
                   y=counter_list,
                   mode='lines+markers')
    ])
    return fig


if __name__ == '__main__':
    app.run_server()