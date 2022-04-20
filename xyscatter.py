from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from scatter_vars import *
from auth_settings import *
from authenticate import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

r=requests.options(base_url+'voyage/?hierarchical=False',headers=auth_headers)
md=json.loads(r.text)

url=base_url+'voyage/caches'
data={
	'cachename':'voyage_xyscatter'
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
							id='x_vars',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_x_vars],
							value=scatter_plot_x_vars[0],
							multi=False
						),
						html.Label('Group By'),
						dcc.Dropdown(
							id='factors',
							options= [{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_factors] + [{"label":"Do Not Group","value":"Do Not Group"}],
							value="Do Not Group",
							multi=False
						)
					]),						
					width=12,xs=12,sm=12,md=12,lg=6
				),
				dbc.Col(
					html.Div([
						html.Label('Y variables'),
						dcc.Dropdown(
							id='y_vars',
							options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_y_vars],
							value=scatter_plot_y_vars[0],
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
					[dcc.Graph(id='voyages-scatter-graph')]
				),
			),
		]),
	],
	style={"height": "100vh"},
)




@app.callback(
	Output('voyages-scatter-graph', 'figure'),
	Input('agg_mode', 'value'),
	Input('x_vars', 'value'),
	Input('y_vars', 'value'),
	Input('factors', 'value')
	)

def update_figure(agg_mode,x_val,y_val,color_val):
	
	
	def agg_functions(x_val,y_val,agg_mode,df3):
		if agg_mode=='Averages':
			df3=df3.groupby(x_val)[y_val].mean()
			df3=df3.reset_index()
		elif agg_mode=='Totals/Sums':
			df3=df3.groupby(x_val)[y_val].sum()
			df3=df3.reset_index()
		return(df3)
	
	figtitle='Stacked %s of:<br>' %agg_mode.lower() + md[y_val]['flatlabel']
	
	fig=go.Figure()	
	
	if color_val!="Do Not Group":
		colors=df[color_val].unique()
		for color in colors:
			df2=df[df[color_val]==color]
			df2=agg_functions(x_val,y_val,agg_mode,df2)
			x_vals=df2[x_val]
			y_vals=df2[y_val]
			trace_name=color
	
			fig.add_trace(go.Scatter(
				x=x_vals,
				y=y_vals,
				name=trace_name,
				stackgroup='one',
				line= {'shape': 'spline'},
				mode='none')
			)
	else:
		df2=agg_functions(x_val,y_val,agg_mode,df)
		x_vals=df2[x_val].values
		y_vals=df2[y_val].values
		fig.add_trace(go.Scatter(
			x=x_vals,
			y=y_vals,
			fill='tozeroy')
		)
	
	fig.update_layout(height=700)
	
	return fig


if __name__ == '__main__':
	app.run_server(debug=True)