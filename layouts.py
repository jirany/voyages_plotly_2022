from dash import dcc, html,dash_table
from vars import *
import dash_bootstrap_components as dbc
import requests
import json
import time
import dash_leaflet as dl
from app_secrets import *

r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)

#token validation
detail=md.get('detail')
if detail == "Invalid token.":
	print("**************\n%s\n%s\nSERVER REJECTED AUTH TOKEN -- CHECK YOUR SETTINGS\n**************" %(base_url,headers))
	time.sleep(15)
	exit()

bar_layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div(
					[					
						dbc.Card(
							[dbc.Row(
								[
									dbc.Col(
											html.Div([
												html.Label('X variables'),
												dcc.Dropdown(
													id='bar_x_var',
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
													id='bar_y_var',
													options=[{'label':md[i]['flatlabel'],'value':i} for i in bar_y_abs_vars],
													value=bar_y_abs_vars[0],
													multi=False
												),
												html.Br(),
												html.Label('Totals/Sums or Averages'),
												dcc.RadioItems(
													id='bar_agg_mode',
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
					]
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

xyscatter_layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div([
					dbc.Card(
						[dbc.Row([
							dbc.Col(
									html.Div([
										html.Label('X variables'),
										dcc.Dropdown(
											id='scatter_x_vars',
											options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_x_vars],
											value=scatter_plot_x_vars[0],
											multi=False
										),
									]),						
									width=9,xs=12,sm=12,md=9,lg=9
							),
							dbc.Col(
								html.Div([
									html.Label('Totals/Sums or Averages'),
									dcc.RadioItems(
												id='scatter_agg_mode',
												options=[{'label': i, 'value': i} for i in ['Totals/Sums','Averages']],
												value='Totals/Sums',
												labelStyle={'display': 'inline-block'}
									)
								]),width=3,xs=12,sm=12,md=3,lg=3)
						]),
						dbc.Row([
							dbc.Col([
								html.Div([
									html.Label('Y variables'),
									dcc.Dropdown(
										id='scatter_y_vars',
										options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_y_vars],
										value=scatter_plot_y_vars[0],
										multi=False
									)
								])
							],width=12),
						]),
						dbc.Row([
							dbc.Col([
								html.Label('Group By'),
								dcc.Dropdown(
									id='scatter_factors',
									options= [{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_factors] + [{"label":"Do Not Group","value":"Do Not Group"}],
									value="Do Not Group",
									multi=False
								)
							],width=12)
						]),
						dbc.Row([
							dbc.Col(
								html.Div(
									[dcc.Graph(id='voyages-scatter-graph')]
								),
							),
						])
					]
				)
			])
		)
	])
	]
)


donut_layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div([
					dbc.Card(
						[dbc.Row(
							[
								dbc.Col(
										html.Div([
											html.Label('Sectors'),
											dcc.Dropdown(
												id='donut_sector_var',
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
												id='donut_value_var',
												options=[{'label':md[i]['flatlabel'],'value':i} for i in donut_value_vars],
												value=donut_value_vars[0],
												multi=False
											),
											html.Br(),
											html.Label('Aggregation'),
											dcc.RadioItems(
												id='donut_agg_mode',
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
				])
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




pivot_table_layout =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div([
					dbc.Card(
						[dbc.Row(
							[
								dbc.Col(
										html.Div([
											html.Label('Rows'),
											dcc.Dropdown(
												id='rows',
												options=[{'label':md[i]['flatlabel'],'value':i} for i in pivot_table_categorical_vars],
												value=pivot_table_categorical_vars[0],
												multi=False
											),
											html.Label('Columns'),
											dcc.Dropdown(
												id='columns',
												options=[{'label':md[i]['flatlabel'],'value':i} for i in pivot_table_categorical_vars],
												value=pivot_table_categorical_vars[1],
												multi=False
											),
											html.Label('Cells'),
											dcc.Dropdown(
												id='cells',
												options=[{'label':md[i]['flatlabel'],'value':i} for i in pivot_table_numerical_vars],
												value=pivot_table_numerical_vars[0],
												multi=False
											),
											html.Label('Remove NA?'),
											dcc.RadioItems(
												id='rmna',
												options=[{'label': i, 'value': i} for i in ['True','False']],
												value='sum',
												labelStyle={'display': 'inline-block'}
											),
											html.Label('Value Function'),
											dcc.RadioItems(
												id='valuefunction',
												options=[{'label': i, 'value': i} for i in ['sum','mean','normalize_columns','normalize_rows']],
												value='sum',
												labelStyle={'display': 'inline-block'}
											)
										]),
									)
							]
						)]
					)
				])
			),
		]),
		dbc.Row([
			dbc.Col(
				html.Div(
					[dash_table.DataTable(id='voyages-pivot-table')]
				),
			),
		])
	]
)

leaflet_map =  dbc.Container(
	[
		dbc.Row([
			dbc.Col(
				html.Div([
					html.Label('Geographic granularity level'),
					dcc.Dropdown(
						id='leaflet_map_levelselect',
						options=[{'label':i,'value':i} for i in ['ports','regions','broad_regions']],
						value='regions',
						multi=False
					)
				])
			)
		]),
		dbc.Row([
			dbc.Col(
				html.Div([
					dl.Map(
						[
							dl.TileLayer(id="tile-layer"),
							dl.LayerGroup(id='feature-layer')
						],
						id="map",
						style={
							'width': '100%',
							'height': '800px',
							'margin': "auto",
							"display": "block"
						}
					)
				])
			)
		])
	]
)
