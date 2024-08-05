from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from utils import build_servers_footprint

energy_perf = pd.read_csv('energy_perf.csv', sep=";", index_col="Year")
carbon_intensity = pd.read_csv('carbon_intensity.csv', sep=";", index_col="Country")

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='Server renewable simulator'),
    html.Div([
        html.H2('Country'),
        dcc.Dropdown(carbon_intensity.index, 'France', id='country_dropdown'),
        html.Div(id='carbon_intensity_div')
        ]),
    html.Div([
        html.H2('Hardware'),
        html.Div([
            html.H4('Manufacturing cost (kgCO2e)', style={'display':'inline-block','margin-right':20}),
            dcc.Input(id='manufacturing_cost', type='number', value=1950)]),
        html.Div([
            html.H4('Power consumption (W)', style={'display':'inline-block','margin-right':20}),
            dcc.Input(id='base_power_consumption', type='number', value=917)]),
        ]),
    html.H4(id='result_text'),
    html.H4(children='For all other impacts, the less you renew, the better !!!'),
    html.Div([
        dcc.Graph(id='year_graph', style={'display': 'inline-block'}),
        dcc.Graph(id='cumul_graph', style={'display': 'inline-block'})
    ]) 
])


@callback(
    Output('carbon_intensity_div', 'children'),
    Input('country_dropdown', 'value'))
def update_carbon_intensity(value):
    return f'carbon intensity: {carbon_intensity.loc[value]["Carbon Intensity (kgCO2e/kWh)"]}'

@callback(
    Output('year_graph', 'figure'),
    Output('cumul_graph', 'figure'),
    Output('result_text', 'children'),
    Input('manufacturing_cost', 'value'),
    Input('base_power_consumption', 'value'),
    Input('country_dropdown', 'value'))
def update_graph(manuf_cost, power,intensity):
    footprint_year = pd.DataFrame()
    footprint_cumul = pd.DataFrame()
    for life in range(1,15,2):
        servers = build_servers_footprint(experience_years=20, 
                                          manufacturing_cost=manuf_cost, 
                                          power_consumption=power,
                                          power_factor=energy_perf,
                                          lifetime=life,
                                          carbon_intensity=carbon_intensity.loc[intensity]["Carbon Intensity (kgCO2e/kWh)"])
        footprint_year[f'Replacing every {life} years'] = servers["emissions (kgCO2e)"]
        footprint_cumul[f'Replacing every {life} years'] = servers["cumulated emissions (kgCO2e)"]

    fig1 = px.line(footprint_year, labels={'index': 'year', 'value': 'emissions (kgCO2e)'})
    fig2 = px.line(footprint_cumul, markers=True, title="Cumulated Footprint", labels={'index': 'year', 'value': 'emissions (kgCO2e)'})

    best_choice = footprint_cumul.tail(1).iloc[-1].idxmin()

    text = f'Regarding only Global Warming potential, {best_choice} is the best policy.'
    return fig1, fig2, text

if __name__ == "__main__":
    
    app.run(debug=True)