from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from bar_vars import *
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
						html.Label('X variables'),
						dcc.Dropdown(
							id='x_var',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in bar_x_vars],
							value=bar_x_vars[0],
							multi=False
						)
					]),						
					width=12,xs=12,sm=12,md=12,lg=6
				),
				dbc.Col(
					html.Div([
						html.Label('Y variables'),
						dcc.Dropdown(
							id='y_var',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in bar_y_abs_vars],
							value=bar_y_abs_vars[0],
							multi=False
						),
						html.Br(),
						html.Label('Totals/Sums or Averages'),
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
					[dcc.Graph(id='voyages-bar-graph')]
				),
			),
		]),
	],
	style={"height": "100vh"},
)

@app.callback(
	Output('voyages-bar-graph', 'figure'),
	Input('x_var', 'value'),
	Input('y_var', 'value'),
	Input('agg_mode','value')
	)

def update_figure(x_var,y_var,agg_mode):
	
	if agg_mode=='Averages':
		df2=df.groupby(x_var)[y_var].mean()
		df2=df2.reset_index()
	elif agg_mode=='Totals/Sums':
		df2=df.groupby(x_var)[y_var].sum()
		df2=df2.reset_index()
	
	yvarlabel=md[y_var]['flatlabel']
	xvarlabel=md[x_var]['flatlabel']
	
	fig=px.bar(df2,x=x_var,y=y_var,
		labels={
			y_var:yvarlabel,
			x_var:xvarlabel
			}
		)
	
	fig.update_layout(
		xaxis_title='',
		yaxis_title='',
		height=700
	)

	return fig
	
if __name__ == '__main__':
	app.run_server(debug=True)