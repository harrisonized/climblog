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
from plot import logistic_func, plot_scatter, plot_hist, plot_heatmap, convert_json

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

@app.route("/indoors", methods=["POST", "GET"])
def indoors():

	climbing_log_indoors = pd.read_csv('static/data/climbing-log-indoors.csv') # Read in data

	# Scatter
	scatter_df = get.get_scatter(climbing_log_indoors, color_dict)
	grades_hist_df = get.get_hist(climbing_log_indoors, color_dict)
	grades_hist_filter_df = grades_hist_df[grades_hist_df.grade_-grades_hist_df.grade_.shift().fillna(0) > 0][['grade_', 'date_']]
	grades_hist_df = grades_hist_df.sort_values('grade_').reset_index(drop=True)

	# Curve fit on new grades
	date_linspace = np.linspace(
    	mdates.date2num(dt.datetime.strptime(grades_hist_filter_df.date_.min(), "%Y-%m-%d")), # Date min
    	mdates.date2num(dt.datetime.strptime(grades_hist_filter_df.date_.max(), "%Y-%m-%d")), # Date max
    	num=25)
	popt, pcov = curve_fit(
		logistic_func,
		grades_hist_filter_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
		grades_hist_filter_df.grade_,
		p0=(3.29367465e+00,  1.22369278e+01, -9.00439720e+06, -2.10297837e+01))

	scatter_df.date_ = scatter_df.date_.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Convert to datetime
	scatter_df.date_ = scatter_df.date_.apply(lambda x: x+dt.timedelta(seconds=59*random.random())) # Jitter
	scatter_df.grade_ = scatter_df.grade_.apply(lambda x: x-0.15+0.3*random.random()) # Jitter

	fig = plot_scatter(scatter_df, date_linspace, popt)
	scatter_div = convert_json(fig)

	# Grades Histogram
	fig = plot_hist(grades_hist_df, 'Grades Histogram', 'VGrade', 'Number of Recorded Sends')
	histogram_div = convert_json(fig)

	# Grades by Year
	year_df = get.get_year(climbing_log_indoors)
	year_df.description = year_df.description.apply(lambda x: word_wrap(x, 10))
	year_table_df = year_df.reset_index().pivot(index="grade_", columns="year", values="count_").fillna(0) # Pivot
	year_table_df.index = year_table_df.index.map(lambda x: 'V'+str(x))
	year_fig = plot_heatmap(year_df, year_table_df,
		"Year", "Grade", "Heatmap of Grades by Year")
	year_div = convert_json(year_fig)

	# Grades by Wall-type
	wall_df = get.get_wall(climbing_log_indoors)
	wall_df.description = wall_df.description.apply(lambda x: word_wrap(x, 10))
	wall_table_df = wall_df.reset_index().pivot(index="grade_", columns="wall_type", values="count_").fillna(0) # Pivot
	wall_table_df.index = wall_table_df.index.map(lambda x: 'V'+str(x))
	wall_table_df = wall_table_df[['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']]
	wall_fig = plot_heatmap(wall_df, wall_table_df,
		"Wall-type", "Grade", "Heatmap of Grades by Wall-type")
	wall_div = convert_json(wall_fig)

	# Grades by Hold-type
	hold_df = get.get_hold(climbing_log_indoors)
	hold_df.description = hold_df.description.apply(lambda x: word_wrap(x, 10))
	hold_table_df = hold_df.reset_index().pivot(index="grade_", columns="sep_hold_type", values="count_").fillna(0) # Pivot
	hold_table_df.index = hold_table_df.index.map(lambda x: 'V'+str(x))
	hold_table_df = hold_table_df[['jug', 'crimp', 'sloper', 'pinch']]
	hold_fig = plot_heatmap(hold_df, hold_table_df,
		"Hold-type", "Grade", "Heatmap of Grades by Hold-type")
	hold_div = convert_json(hold_fig)

	# Grades by Style
	style_df = get.get_style(climbing_log_indoors)
	style_df.description = style_df.description.apply(lambda x: word_wrap(x, 10)) 
	style_table_df = style_df.reset_index().pivot(index="grade_", columns="style", values="count_").fillna(0) # Pivot
	style_table_df.index = style_table_df.index.map(lambda x: 'V'+str(x))
	style_table_df = style_table_df[['mantle', 'natural', 'dyno', 'comp']]
	style_fig = plot_heatmap(style_df, style_table_df,
		"Style", "Grade", "Heatmap of Grades by Style")
	style_div = convert_json(style_fig)

	return render_template(
    	"page.html",
    	scatter_div=Markup(scatter_div),
    	histogram_div=Markup(histogram_div),
    	year_div = year_div,
    	wall_div = wall_div,
    	hold_div = hold_div,
    	style_div = style_div
    )

@app.route("/outdoors", methods=["POST", "GET"])
def outdoors():

	climbing_log_outdoors = pd.read_csv('static/data/climbing-log-outdoors.csv') # Read in data

	# Scatter
	scatter_df = get.get_scatter(climbing_log_outdoors, color_dict)
	grades_hist_df = get.get_hist(climbing_log_outdoors, color_dict)
	grades_hist_filter_df = grades_hist_df[grades_hist_df.grade_-grades_hist_df.grade_.shift().fillna(0) > 0][['grade_', 'date_']]
	grades_hist_df = grades_hist_df.sort_values('grade_').reset_index(drop=True)

	# Curve fit on new grades
	date_linspace = np.linspace(
    	mdates.date2num(dt.datetime.strptime(grades_hist_filter_df.date_.min(), "%Y-%m-%d")), # Date min
    	mdates.date2num(dt.datetime.strptime(grades_hist_filter_df.date_.max(), "%Y-%m-%d")), # Date max
    	num=25)
	popt, pcov = curve_fit(
		logistic_func,
		grades_hist_filter_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
		grades_hist_filter_df.grade_,
		p0=(1.69557320e+00,  1.23573774e+01, -9.09837912e+06, -7.49917188e+00))

	scatter_df.date_ = scatter_df.date_.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Convert to datetime
	scatter_df.date_ = scatter_df.date_.apply(lambda x: x+dt.timedelta(seconds=59*random.random())) # Jitter
	scatter_df.grade_ = scatter_df.grade_.apply(lambda x: x-0.15+0.3*random.random()) # Jitter

	fig = plot_scatter(scatter_df, date_linspace, popt)
	scatter_div = convert_json(fig)

	# Grades Histogram
	fig = plot_hist(grades_hist_df, 'Grades Histogram', 'VGrade', 'Number of Recorded Sends')
	histogram_div = convert_json(fig)

	# Grades by Year
	year_df = get.get_year(climbing_log_outdoors)
	year_df.description = year_df.description.apply(lambda x: word_wrap(x, 10))
	year_table_df = year_df.reset_index().pivot(index="grade_", columns="year", values="count_").fillna(0) # Pivot
	year_table_df.index = year_table_df.index.map(lambda x: 'V'+str(x))
	year_fig = plot_heatmap(year_df, year_table_df,
		"Year", "Grade", "Heatmap of Grades by Year")
	year_div = convert_json(year_fig)

	# Grades by Wall-type
	wall_df = get.get_wall(climbing_log_outdoors)
	wall_df.description = wall_df.description.apply(lambda x: word_wrap(x, 10))
	wall_table_df = wall_df.reset_index().pivot(index="grade_", columns="wall_type", values="count_").fillna(0) # Pivot
	wall_table_df.index = wall_table_df.index.map(lambda x: 'V'+str(x))
	wall_table_df = wall_table_df[['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'crack', 'variable']]
	wall_fig = plot_heatmap(wall_df, wall_table_df,
		"Wall-type", "Grade", "Heatmap of Grades by Wall-type")
	wall_div = convert_json(wall_fig)

	# Grades by Hold-type
	hold_df = get.get_hold(climbing_log_outdoors)
	hold_df.description = hold_df.description.apply(lambda x: word_wrap(x, 10))
	hold_table_df = hold_df.reset_index().pivot(index="grade_", columns="sep_hold_type", values="count_").fillna(0) # Pivot
	hold_table_df.index = hold_table_df.index.map(lambda x: 'V'+str(x))
	hold_table_df = hold_table_df[['jug', 'crimp', 'sloper', 'pinch']]
	hold_fig = plot_heatmap(hold_df, hold_table_df,
		"Hold-type", "Grade", "Heatmap of Grades by Hold-type")
	hold_div = convert_json(hold_fig)

	# Grades by Style
	style_df = get.get_style(climbing_log_outdoors)
	style_df.description = style_df.description.apply(lambda x: word_wrap(x, 10)) 
	style_table_df = style_df.reset_index().pivot(index="grade_", columns="style", values="count_").fillna(0) # Pivot
	style_table_df.index = style_table_df.index.map(lambda x: 'V'+str(x))
	style_table_df = style_table_df[['mantle', 'natural', 'dyno', 'comp']]
	style_fig = plot_heatmap(style_df, style_table_df,
		"Style", "Grade", "Heatmap of Grades by Style")
	style_div = convert_json(style_fig)

	return render_template(
    	"page.html",
    	scatter_div=Markup(scatter_div),
    	histogram_div=Markup(histogram_div),
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