from vars import *
import requests
import json
from app_secrets import *
from dash import dcc

r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)

def loadjson(fname):
	d=open(fname,"r")
	t=d.read()
	j=json.loads(t)
	d.close()
	return j
def dumpjson(fname,data):
	d=open(fname,"w")
	d.write(json.dumps(data))
	d.close()
	return True

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
