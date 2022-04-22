from dash import Input, Output, callback, dash_table
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import gc
from app_secrets import *

r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)

def update_df(url,data):
	global headers
	r=requests.post(url,data=data,headers=headers)
	j=r.text
	df=pd.read_json(j)
	return df

@callback(
	Output('voyages-bar-graph', 'figure'),
	Input('bar_x_var', 'value'),
	Input('bar_y_var', 'value'),
	Input('bar_agg_mode','value')
	)
def update_bar_graph(x_var,y_var,agg_mode):
	global md

	data={
		'selected_fields':[x_var,y_var],
		'cachename':['voyage_bar_and_donut_charts']
	}
	
	df=update_df(
		base_url+'voyage/caches',
		data=data
	)
	
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
	del df2, df
	gc.collect()
	return fig

@callback(
	Output('voyages-scatter-graph', 'figure'),
	Input('scatter_agg_mode', 'value'),
	Input('scatter_x_vars', 'value'),
	Input('scatter_y_vars', 'value'),
	Input('scatter_factors', 'value')
	)

def update_scatter_graph(agg_mode,x_val,y_val,color_val):
	global md
	def agg_functions(x_val,y_val,agg_mode,df3):
		if agg_mode=='Averages':
			df3=df3.groupby(x_val)[y_val].mean()
			df3=df3.reset_index()
		elif agg_mode=='Totals/Sums':
			df3=df3.groupby(x_val)[y_val].sum()
			df3=df3.reset_index()
		return(df3)
	
	selected_fields=[i for i in [x_val,y_val,color_val] if i!="Do Not Group"]
	
	data={
		'selected_fields':selected_fields,
		'cachename':['voyage_xyscatter']
	}
	
	df=update_df(
		base_url+'voyage/caches',
		data=data
	)
	
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
	df2=None
	del df,df2,df3
	gc.collect()
	fig.update_layout(height=700)
	
	return fig

@callback(
	Output('voyages-donut-graph', 'figure'),
	Input('donut_sector_var', 'value'),
	Input('donut_value_var', 'value'),
	Input('donut_agg_mode','value')
	)
def donut_update_figure(sector_var,value_var,agg_mode):
	global md
	
	data={
		'selected_fields':[sector_var,value_var],
		'cachename':['voyage_bar_and_donut_charts']
	}
	
	df=update_df(
		base_url+'voyage/caches',
		data=data
	)
	
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
	del df,df2
	gc.collect()
	return fig

@callback(
	Output('voyages-pivot-table', 'data'),
	Input('rows', 'value'),
	Input('columns', 'value'),
	Input('cells','value'),
	Input('rmna','value'),
	Input('valuefunction','value')
	)
def pivot_table_update_figure(rows,columns,cells,rmna,valuefunction):
	global md
	
	normalize=False
	if valuefunction=="normalize_columns":
		normalize="columns"
		valuefunction="sum"
	elif valuefunction=="normalize_rows":
		normalize="index"
		valuefunction="sum"
	
	data={
		'rmna':[rmna],
		'normalize':[normalize],
		'groupby_fields':[rows,columns],
		'value_field_tuple':[cells,valuefunction],
		'cachename':['voyage_pivot_tables']
	}
	
	df=update_df(
		base_url+'voyage/groupby',
		data=data
	)
	
	
	
	if normalize != False:
		df=df*100
		df=df.round(1)
	elif valuefunction=="mean":
		df=df.round(0)
	
	df=df.rename_axis('').reset_index()
	
	df=df.fillna(0)
	
	output=df.to_dict('records')
	
	return output


