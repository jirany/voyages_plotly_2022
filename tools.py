from vars import *
import requests
import json
from app_secrets import *
from dash import dcc


r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)



def get_rangeslider(fq_varname,component_id):
	data={
		"aggregate_fields" : [fq_varname]
	}
	r=requests.post(url=base_url+"voyage/aggregations",headers=headers,data=data)
	j=json.loads(r.text)
	minval=j[fq_varname]['min']
	maxval=j[fq_varname]['max']
	component=dcc.RangeSlider(min=minval, max=maxval, marks=None, step=1, id=component_id, tooltip={"placement": "bottom", "always_visible": True})
	return component