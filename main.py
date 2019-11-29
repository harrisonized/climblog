from flask import request, Response, send_file, render_template, Markup, Flask
import random
import json
import datetime as dt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.dates as mdates
from _plotly_future_ import v4_subplots
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly

import get
from plot import logistic_func, plot_scatter, plot_heatmap, convert_json



climbing_log_indoors = pd.read_csv('static/data/climbing-log-indoors.csv') # Read in data
climbing_log_outdoors = pd.read_csv('static/data/climbing-log-outdoors.csv') # Read in data

color_dict = {'black': '#000000',
              'blue': '#1f77b4',
              'brown': '#8c564b',
              'colorless': '#7f7f7f',
              'green': '#2ca02c',
              'orange': '#ff7f0e',
              'pink': '#e377c2',
              'purple': '#9467bd',
              'red': '#d62728',
              'white': '#7f7f7f',
              'yellow': '#FFFF00'}

def word_wrap(string, n):
    string_list = string.split()
    parsed_list = [string_list[n*i:n*(i+1)] for i in range((len(string_list)+n-1)//n)]
    joined_string_list = [' '.join(parsed_list[i]) for i in range(len(parsed_list))]
    final_list = ['<br>'.join(joined_string_list)]
    return final_list[0]


# Initialize the app
app = Flask(__name__)

@app.route("/")
def index():
    return send_file("static/html/index.html")

@app.route("/send-tracker-indoors", methods=["POST", "GET"])
def send_tracker_indoors():

	# Import
	scatter_df = get.get_scatter(climbing_log_indoors, color_dict)
	new_grades_df = get.get_new_grades(climbing_log_indoors, color_dict)

	# Curve fit on new grades
	date_linspace = np.linspace(
		mdates.date2num(dt.datetime.strptime(new_grades_df.date_.min(), "%Y-%m-%d")),
		mdates.date2num(dt.datetime.strptime(new_grades_df.date_.max(), "%Y-%m-%d")),
		num=25)

	popt, pcov = curve_fit(
		logistic_func,
		new_grades_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
		new_grades_df.grade_,
		p0=(3.30729837e+00,  1.23648382e+01, -9.09848737e+06, -2.12035703e+01))

	# Plot
	fig = plot_scatter(date_linspace, scatter_df, popt)
	send_tracker_div = convert_json(fig)

	return render_template(
		'send-tracker.html',
		send_tracker_div=Markup(send_tracker_div)
	)

@app.route("/heatmaps-indoors", methods=["POST", "GET"])
def heatmaps_indoors():

	# Grades by Year
	year_df = get.get_year(climbing_log_indoors)
	year_df.description = year_df.description.apply(lambda x: word_wrap(x, 10))
	year_table_df = year_df.reset_index().pivot(index="grade_", columns="year", values="count_").fillna(0) # Pivot
	year_table_df = year_table_df.reindex(['V6', 'V7', 'V8', 'V9', 'V10', 'V11'])
	year_fig = plot_heatmap(year_df, year_table_df,
		['V6', 'V7', 'V8', 'V9', 'V10', 'V11'],
		['2016', '2017', '2018', '2019'],
		"Year", "Grade", "Heatmap of Grades by Year")
	year_div = convert_json(year_fig)

	# Grades by Wall-type
	wall_df = get.get_wall(climbing_log_indoors)
	wall_df.description = wall_df.description.apply(lambda x: word_wrap(x, 10))
	wall_table_df = wall_df.reset_index().pivot(index="grade_", columns="wall_type", values="count_").fillna(0) # Pivot
	wall_table_df = wall_table_df.reindex(['V6', 'V7', 'V8', 'V9', 'V10', 'V11'])
	wall_table_df = wall_table_df[['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']]
	wall_fig = plot_heatmap(wall_df, wall_table_df,
		['V6', 'V7', 'V8', 'V9', 'V10', 'V11'],
		['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable'],
		"Wall-type", "Grade", "Heatmap of Grades by Wall-type")
	wall_div = convert_json(wall_fig)

	# Grades by Hold-type
	hold_df = get.get_hold(climbing_log_indoors)
	hold_df.description = hold_df.description.apply(lambda x: word_wrap(x, 10))
	hold_table_df = hold_df.reset_index().pivot(index="grade_", columns="hold_type", values="count_").fillna(0) # Pivot
	hold_table_df = hold_table_df.reindex(['V6', 'V7', 'V8', 'V9', 'V10', 'V11'])
	hold_table_df = hold_table_df[['jug', 'crimp', 'sloper', 'pinch']]
	hold_fig = plot_heatmap(hold_df, hold_table_df,
		['V6', 'V7', 'V8', 'V9', 'V10', 'V11'],
		['jug', 'crimp', 'sloper', 'pinch'],
		"Hold-type", "Grade", "Heatmap of Grades by Hold-type")
	hold_div = convert_json(hold_fig)

	# Grades by Style
	style_df = get.get_style(climbing_log_indoors)
	style_df.description = style_df.description.apply(lambda x: word_wrap(x, 10)) 
	style_table_df = style_df.reset_index().pivot(index="grade_", columns="style", values="count_").fillna(0) # Pivot
	style_table_df = style_table_df.reindex(['V6', 'V7', 'V8', 'V9', 'V10', 'V11'])
	style_table_df = style_table_df[['natural', 'dyno', 'comp', 'mantle']]
	style_fig = plot_heatmap(style_df, style_table_df,
		['V6', 'V7', 'V8', 'V9', 'V10', 'V11'],
		['natural', 'dyno', 'comp', 'mantle'],
		"Style", "Grade", "Heatmap of Grades by Style")
	style_div = convert_json(style_fig)

	return render_template(
    	"heatmaps.html",
    	year_div = year_div,
    	wall_div = wall_div,
    	hold_div = hold_div,
    	style_div = style_div
    )

@app.route("/send-tracker-outdoors", methods=["POST", "GET"])
def send_tracker_outdoors():

	# Import
	scatter_df = get.get_scatter(climbing_log_outdoors, color_dict)
	new_grades_df = get.get_new_grades(climbing_log_outdoors, color_dict)

	# Curve fit on new grades
	date_linspace = np.linspace(
		mdates.date2num(dt.datetime.strptime(new_grades_df.date_.min(), "%Y-%m-%d")),
		mdates.date2num(dt.datetime.strptime(new_grades_df.date_.max(), "%Y-%m-%d")),
		num=25)

	popt, pcov = curve_fit(
		logistic_func,
		new_grades_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
		new_grades_df.grade_,
		p0=(3.30729837e+00,  1.23648382e+01, -9.09848737e+06, -2.12035703e+01))

	scatter_df.grade_ = scatter_df.grade_.apply(lambda x: x-0.15+0.3*random.random()) # Jitter

	# Plot
	fig = plot_scatter(date_linspace, scatter_df, popt)
	send_tracker_div = convert_json(fig)

	return render_template(
		'send-tracker.html',
		send_tracker_div=Markup(send_tracker_div)
	)

@app.route("/heatmaps-outdoors", methods=["POST", "GET"])
def heatmaps_outdoors():

	# Grades by Year
	year_df = get.get_year(climbing_log_outdoors)
	year_df.description = year_df.description.apply(lambda x: word_wrap(x, 10))
	year_table_df = year_df.reset_index().pivot(index="grade_", columns="year", values="count_").fillna(0) # Pivot
	year_table_df = year_table_df.reindex(['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'])
	year_fig = plot_heatmap(year_df, year_table_df,
		['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'],
		['2016', '2017', '2018', '2019'],
		"Year", "Grade", "Heatmap of Grades by Year")
	year_div = convert_json(year_fig)

	# Grades by Wall-type
	wall_df = get.get_wall(climbing_log_outdoors)
	wall_df.description = wall_df.description.apply(lambda x: word_wrap(x, 10))
	wall_table_df = wall_df.reset_index().pivot(index="grade_", columns="wall_type", values="count_").fillna(0) # Pivot
	wall_table_df = wall_table_df.reindex(['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'])
	wall_table_df = wall_table_df[['cave', 'overhang', 'face', 'arete', 'slab']]
	wall_fig = plot_heatmap(wall_df, wall_table_df,
		['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'],
		['cave', 'overhang', 'face', 'arete', 'slab'],
		"Wall-type", "Grade", "Heatmap of Grades by Wall-type")
	wall_div = convert_json(wall_fig)

	# Grades by Hold-type
	hold_df = get.get_hold(climbing_log_outdoors)
	hold_df.description = hold_df.description.apply(lambda x: word_wrap(x, 10))
	hold_table_df = hold_df.reset_index().pivot(index="grade_", columns="hold_type", values="count_").fillna(0) # Pivot
	hold_table_df = hold_table_df.reindex(['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'])
	hold_table_df = hold_table_df[['jug', 'crimp', 'sloper', 'pinch']]
	hold_fig = plot_heatmap(hold_df, hold_table_df,
		['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'],
		['jug', 'crimp', 'sloper', 'pinch'],
		"Hold-type", "Grade", "Heatmap of Grades by Hold-type")
	hold_div = convert_json(hold_fig)

	# Grades by Style
	style_df = get.get_style(climbing_log_outdoors)
	style_df.description = style_df.description.apply(lambda x: word_wrap(x, 10)) 
	style_table_df = style_df.reset_index().pivot(index="grade_", columns="style", values="count_").fillna(0) # Pivot
	style_table_df = style_table_df.reindex(['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'])
	style_table_df = style_table_df[['natural', 'dyno', 'comp']]
	style_fig = plot_heatmap(style_df, style_table_df,
		['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'],
		['natural', 'dyno', 'comp'],
		"Style", "Grade", "Heatmap of Grades by Style")
	style_div = convert_json(style_fig)

	return render_template(
    	"heatmaps.html",
    	year_div = year_div,
    	wall_div = wall_div,
    	hold_div = hold_div,
    	style_div = style_div
    )



# Start the server, continuously listen to requests.
# We'll have a running web app!

if __name__=="__main__":
    # For local development:
    #app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()