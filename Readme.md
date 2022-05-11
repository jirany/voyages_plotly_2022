# Demo Voyages Dashboard

This is a demonstration of how the experimental Voyages API (https://github.com/JohnMulligan/voyages-api) data can be consumed by lightweight, front-end applications to make interactive dashboards.

## Framework

It is written in Python, using Plotly's Dash framework to render the interactives. Plotly puts a Flask wrapper on React components that render its data visualizations, which allows one to easily create update functions and share data between components in Python without coding any javascript.

* Callbacks: https://dash.plotly.com/advanced-callbacks
* Components: https://dash.plotly.com/urls

## Suggested installation procedures

### Prereqs
	
1. Remote server base url
1. Valid API key (email jcm)
1. Mapbox token
1. Python3

### Setup

Fork this repo then clone to your computer `https://github.com/JohnMulligan/voyages_plotly_2022`

Instantiate a virtual environment in the cloned project directory `python3 -m venv venv`

BEFORE YOU ACTIVATE THE VIRTUAL ENVIRONMENT:

Insert your settings into the venv/bin/activate file like so, and then save

	#REMOTE
	export voyages_auth_token=ABCDEFG...
	export base_url="https://voyages3-api.crc.rice.edu/"
	export mapbox_access_token=HIJKLMNOP...

Now you can activate your virtual environment with `source venv/bin/activate`

Then install the required python packages in your virtual environment `pip3 install -r requirements.txt`

And finally, you can run the app with `python app.py`

## Project Structure

Following Dash documentation with a couple of twists:

* _layouts.py_ contains the layouts of the different micro-apps, organizing the on-page display of the following interfaces (like a visualization) and their related components (like dropdown menus or radio options)
	* bar charts
	* scatter graphs
	* donut charts
	* pivot tables
	* leaflet maps
	* data tables
	* search pane
* _callbacks.py_ enables these laid-out components to be interactive. When a page element's id is specified as the input to a callback, Dash creates event bindings such that updates to that component trigger the Python function.
	* every visualization above has an "update" callback that is triggered
		* by its layout components (e.g., selecting a new X or Y var for the scatter graph to render)
		* by an update to the search pane in all cases (SEE MENTIONS OF DCC.STORE BELOW)
	* the leaflet map has some extra functionality to handle the weirdness of Voyages' legacy mapping code
	* there is a special "update search params" callback tied to the search pane defined in layouts.py. When the page elements in the search pane are updated, these are encoded as a json object which can be read by the voyage api as search parameters; that json object is then saved to a dcc.store object. That dcc.store object is an input / trigger for updating all of the graphs. By breaking this element out, we allow the filter to persist across the visualizations.
* _tools.py_ gestures towards how we might dynamically build some components. See especially the way in which the rangeslider is constructed (for reference, it's used by the search pane).
* _vars.py_
	* names the different variables that each app will request from the API.
	* loads the variable labels from the API options endpoint.
	* overwrites some of those labels with cleaner, shorter text where I found that necessary.
* _app.py_
	* handles the selection of the visualization
	* defines the search pane so that it appears above all visualizations
	* stores the search objects in the DCC.STORE object for use by the visualizations: https://dash.plotly.com/dash-core-components/store
* app_secrets.py loads environment variables
	* the api key
	* the api endpoint
	* the mapbox key (for loading map tiles)