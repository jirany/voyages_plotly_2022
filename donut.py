from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from donut_vars import *
from auth_settings import *
from authenticate import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

r=requests.options(base_url+'voyage/?hierarchical=False',headers=auth_headers)
md=json.loads(r.text)

url=base_url+'voyage/caches'
data={
	'cachename':'voyage_bar_and_donut_charts'
}

r=requests.post(url,data,headers=auth_headers)
j=r.text
df=pd.read_json(j)



controls=controls=dbc.Card(
	[dbc.Row(
		[
			dbc.Col(
					html.Div([
						html.Label('Sectors'),
						dcc.Dropdown(
							id='sector_var',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in donut_name_vars],
							value=donut_name_vars[0],
							multi=False
						),
					]),
					width=12,xs=12,sm=12,md=12,lg=6
				),
				dbc.Col(
					html.Div([
						html.Label('Values'),
						dcc.Dropdown(
							id='value_var',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in donut_value_vars],
							value=donut_value_vars[0],
							multi=False
						),
						html.Br(),
						html.Label('Aggregation'),
						dcc.RadioItems(
							id='agg_mode',
							options=[{'label': i, 'value': i} for i in ['Totals/Sums','Averages']],
							value='Totals/Sums',
							labelStyle={'display': 'inline-block'}
						)
					]),
					width=12,xs=12,sm=12,md=12,lg=6
				)
		]
	)]
)
	

app.layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div(
					[controls]
				)
			),
		]),
		dbc.Row([
			dbc.Col(
				html.Div(
					[dcc.Graph(id='voyages-donut-graph')]
				),
			),
		])
	]
)



@app.callback(
	Output('voyages-donut-graph', 'figure'),
	Input('sector_var', 'value'),
	Input('value_var', 'value'),
	Input('agg_mode','value')
	)

def update_figure(sector_var,value_var,agg_mode):
	
	if agg_mode=='Averages':
		df2=df.groupby(sector_var)[value_var].mean()
		df2=df2.reset_index()
	elif agg_mode=='Totals/Sums':
		df2=df.groupby(sector_var)[value_var].sum()
		df2=df2.reset_index()
	
	sectorvarlabel=md[sector_var]['flatlabel']
	valuevarlabel=md[value_var]['flatlabel']
	
	fig=px.pie(df2,values=value_var,names=sector_var,
		labels={
			sector_var:sectorvarlabel,
			value_var:valuevarlabel
			},
		hole=.4
		)
	fig.update_traces(textposition='inside', textinfo='percent+label')

	return fig
	
if __name__ == '__main__':
	app.run_server(debug=True)