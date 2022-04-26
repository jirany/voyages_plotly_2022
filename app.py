from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from layouts import *
from vars import *
import requests
from callbacks import *
import json
from app_secrets import *


r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

registered_apps=[
	["xyscatter_layout","Scatter and Timeline Graphs"],
	["bar_layout","Bar Charts"],
	["donut_layout","Donut Charts"],
	["pivot_table_layout","Pivot Table Layout"],
	["leaflet_map","LEAFLET map (experimental)"]
]

app.layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Card([
				dbc.Col(
					html.Div([
						html.Label('Select App'),
							dcc.Dropdown(
								id='app_selector',
								options=[
									{'label':i[1],'value':i[0]} for i in registered_apps],
								value=registered_apps[0][0],
								multi=False
							),
						html.Br()
					])
				)
			])
		]),
		html.Hr(),
		dbc.Row([
			dbc.Col(
				html.Div(id='page-content'),
			)
		])
	]
)

@app.callback(
	Output('page-content', 'children'),
    Input('app_selector', 'value')
)
def display_page(selected_app_layout_name):
	return eval(selected_app_layout_name)

if __name__ == '__main__':
    app.run_server(debug=True)