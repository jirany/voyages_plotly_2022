import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dash_table,State
import pandas as pd
import requests
import json
from app_secrets import *
import dash
import dash_core_components as dcc
import dash_html_components as html

scatter_plot_x_vars=[
	'voyage_dates__imp_arrival_at_port_of_dis_yyyy',
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_dates__length_middle_passage_days',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked'
	]

scatter_plot_y_vars=[
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
	'voyage_slaves_numbers__percentage_female',
	'voyage_slaves_numbers__percentage_male',
	'voyage_slaves_numbers__percentage_child',
	'voyage_slaves_numbers__percentage_men_among_embarked_slaves',
	'voyage_slaves_numbers__percentage_women_among_embarked_slaves',
	'voyage_slaves_numbers__imp_mortality_ratio',
	'voyage_slaves_numbers__imp_jamaican_cash_price',
	'voyage_slaves_numbers__percentage_boys_among_embarked_slaves',
	'voyage_slaves_numbers__percentage_girls_among_embarked_slaves',
	'voyage_ship__tonnage_mod',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing'
]

scatter_plot_factors=[
	'voyage_ship__imputed_nationality__name',
	'voyage_itinerary__imp_principal_region_of_slave_purchase__region',
	'voyage_itinerary__imp_broad_region_of_slave_purchase__broad_region',
	'voyage_itinerary__imp_broad_region_slave_dis__broad_region'
]

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(id='fizz'),
    dcc.Dropdown(
		id='scatter_x_vars',
		options=[i for i in scatter_plot_x_vars],
		value=scatter_plot_x_vars[0],
		multi=False
	),
	dcc.Dropdown(
		id='scatter_y_vars',
		options=[i for i in scatter_plot_y_vars],
		value=scatter_plot_y_vars[0],
		multi=False
	),
	dcc.Dropdown(
		id='scatter_factors',
		options=[i for i in scatter_plot_factors]+ ["Do Not Group"],
		value="Do Not Group",
		multi=False
	)
])

@app.callback(
	Output('fizz', 'figure'),
	Input('scatter_x_vars', 'value'),
	Input('scatter_y_vars', 'value'),
	Input('scatter_factors', 'value'),
	)
def update_scatter_graph(scatter_x_vars,scatter_y_vars,scatter_factors):
	global headers
	selected_fields=[i for i in [scatter_x_vars,scatter_y_vars,scatter_factors] if i!="Do Not Group"]

	data={
		'selected_fields':selected_fields,
		'cachename':['voyage_xyscatter']
	}

	url="https://voyages3-api.crc.rice.edu/voyage/caches"

	r=requests.post(url,data=data,headers=headers)
	j=r.text

	df=pd.read_json(j)
	fig=go.Figure()
	if scatter_factors!="Do Not Group":
		colors=df[scatter_factors].unique()
		for color in colors:
			df=df[df[scatter_factors]==color]
			scatter_x_vars=df[scatter_x_vars]
			scatter_y_vars=df[scatter_y_vars]
			trace_name=color

			fig.add_trace(go.Scatter(
				x=scatter_x_vars,
				y=scatter_y_vars,
				name=trace_name,
				stackgroup='one',
				line= {'shape': 'spline'},
				mode='none')
			)
	else:
		scatter_x_vars=df[scatter_x_vars]
		scatter_y_vars=df[scatter_y_vars]
		fig.add_trace(go.Scatter(
				x=scatter_x_vars,
				y=scatter_y_vars,
				fill='tozeroy')
			)
	return fig



app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
