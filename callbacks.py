from dash import Input, Output, callback

@callback(
    Output('page-1-display-value', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'

@callback(
    Output('page-2-display-value', 'children'),
    Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'


@callback(
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