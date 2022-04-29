## PLOTLY CAN'T CURRENTLY HANDLE COMMAS IN ITS MULTISELECT DROPDOWN FIELDS.

## https://github.com/plotly/dash/commit/f6b51a841e7deddebfbada374e7de4c297bb2ce8

##when that's fixed, this should be good to go as a component
##though I should make it flexible and use it from tools.py





		dbc.Row([
			dbc.Card([
				html.H5("Search/Filters"),
				dbc.Row([
					dbc.Col(
						html.Div([
							"Multi dynamic Dropdown",
							dcc.Dropdown(
								id="my-multi-dynamic-dropdown",
								multi=True,
								options=[],
								value=None
							),
						]),
					)
				])
			])
		]),
	

#from https://dash.plotly.com/dash-core-components/dropdown
@app.callback(
    Output("my-multi-dynamic-dropdown", "options"),
	[Input("my-multi-dynamic-dropdown", "search_value"),
	State("my-multi-dynamic-dropdown", "value")]
)
def update_multi_options(search_value, state_value):
	
	if search_value:
		varname="voyage_captainconnection__captain__name"
		data={varname: [search_value]}
		r=requests.post(url=base_url+'voyage/autocomplete',headers=headers,data=data)
		j=json.loads(r.text)
		autocomplete_results=[
			{"label":i,"value":i} for i in j[varname]
		]
	else:
		autocomplete_results=[]
	
	if type(state_value)==list:
		autocomplete_results+=[{"label":i,"value":i} for i in state_value]
	elif type(state_value)==str:
		autocomplete_results+=[{"label":i,"value":i} for i in [state_value]]
	
	return autocomplete_results


