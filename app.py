from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from layouts import *
import plotly.express as px
import plotly.graph_objects as go
from vars import *
import pandas as pd
import requests
import json
import gc
from app_secrets import *

r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

registered_apps=[
	["xyscatter_layout","Scatter and Timeline Graphs"],
	["bar_layout","Bar Charts"],
	["donut_layout","Donut Charts"]
]


def update_df(url,data,headers):
	global df
	r=requests.post(url,data,headers=headers)
	j=r.text
	df=pd.read_json(j)

df=update_df(base_url+'voyage/caches',data={'cachename':'voyage_xyscatter'},headers=headers)

app.layout =  dbc.Container(
	[
		dcc.Store(id="selected_app_layout_name"),
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

@callback(
	Output('selected_app_layout_name','data'),
    Input('app_selector', 'value')
)
def display_page(selected_app_layout_name):
	if selected_app_layout_name in ['donut_layout','bar_layout']:
		cachename='voyage_bar_and_donut_charts'
	elif selected_app_layout_name=='xyscatter_layout':
		cachename='voyage_xyscatter'
	url=base_url+'voyage/caches'
	data={
		'cachename':cachename
	}
	
	update_df(url,data,headers)
	
	return(selected_app_layout_name)

@callback(
	Output('page-content', 'children'),
    Input('selected_app_layout_name', 'data')
)
    
def display_page(selected_app_layout_name):
	return eval(selected_app_layout_name)

@callback(
	Output('voyages-bar-graph', 'figure'),
	Input('bar_x_var', 'value'),
	Input('bar_y_var', 'value'),
	Input('bar_agg_mode','value')
	)
def update_bar_graph(x_var,y_var,agg_mode):
	global df
	global md
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
	del df2
	gc.collect()
	return fig

@app.callback(
	Output('voyages-scatter-graph', 'figure'),
	Input('scatter_agg_mode', 'value'),
	Input('scatter_x_vars', 'value'),
	Input('scatter_y_vars', 'value'),
	Input('scatter_factors', 'value')
	)

def update_scatter_graph(agg_mode,x_val,y_val,color_val):
	global df
	global md
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
	df3=None
	del df3
	del df2
	gc.collect()
	fig.update_layout(height=700)
	
	return fig

@app.callback(
	Output('voyages-donut-graph', 'figure'),
	Input('donut_sector_var', 'value'),
	Input('donut_value_var', 'value'),
	Input('donut_agg_mode','value')
	)
def donut_update_figure(sector_var,value_var,agg_mode):
	global df
	global md
	
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
	fig.update_layout(height=700)
	fig.update_traces(textposition='inside', textinfo='percent+label')
	del df2
	gc.collect()
	return fig

if __name__ == '__main__':
    app.run_server(debug=False)