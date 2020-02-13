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
from plot import word_wrap, convert_json, logistic_func, plot_scatter, plot_histogram, plot_heatmap


"""
Shared Items
"""

def curve_fit_new_grades(df, p0):
    new_grades_df = df[df.grade_-df.grade_.shift().fillna(0) > 0]
    popt, pcov = curve_fit(
        logistic_func, 
        new_grades_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
        new_grades_df.grade_, 
        p0=p0)
    return popt

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

"""
Indoors
"""

climbing_log_indoors = pd.read_csv('static/data/climbing-log-indoors.csv') # Read in data

# Scatter
scatter_df = get.get_scatter(climbing_log_indoors, color_dict)
grades_histogram_df = get.get_histogram(climbing_log_indoors, color_dict)
popt =  curve_fit_new_grades(grades_histogram_df,
	p0=(3.29367465e+00,  1.22369278e+01, -9.00439720e+06, -2.10297837e+01))
fig = plot_scatter(scatter_df, popt, "Sends by Date", "Date", "Grade")
scatter_indoors_div = convert_json(fig)

# Grades Histogram
fig = plot_histogram(grades_histogram_df, 'Grades Histogram', 'Grade', 'Number of Recorded Sends')
histogram_indoors_div = convert_json(fig)

# Grades by Year
year_df = get.get_year(climbing_log_indoors)
year_fig = plot_heatmap(year_df, "Heatmap of Grades by Year", "Year", "Grade")
year_indoors_div = convert_json(year_fig)

# Grades by Wall-type
wall_df = get.get_wall(climbing_log_indoors)
wall_fig = plot_heatmap(wall_df, "Heatmap of Grades by Wall-type", "Wall-type", "Grade",
	['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable'])
wall_indoors_div = convert_json(wall_fig)

# Grades by Hold-type
hold_df = get.get_hold(climbing_log_indoors)
hold_fig = plot_heatmap(hold_df, "Heatmap of Grades by Hold-type", "Hold-type", "Grade",
	['jug', 'crimp', 'sloper', 'pinch'])
hold_indoors_div = convert_json(hold_fig)

# Grades by Style
style_df = get.get_style(climbing_log_indoors)
style_fig = plot_heatmap(style_df, "Heatmap of Grades by Style", "Style", "Grade",
	['mantle', 'natural', 'dyno', 'comp'])
style_indoors_div = convert_json(style_fig)



"""
Outdoors
"""

climbing_log_outdoors = pd.read_csv('static/data/climbing-log-outdoors.csv') # Read in data

# Scatter
scatter_df = get.get_scatter(climbing_log_outdoors, color_dict)
grades_histogram_df = get.get_histogram(climbing_log_outdoors, color_dict)
popt =  curve_fit_new_grades(grades_histogram_df,
	p0=(1.69557320e+00,  1.23573774e+01, -9.09837912e+06, -7.49917188e+00))
fig = plot_scatter(scatter_df, popt, "Sends by Date", "Date", "Grade")
scatter_outdoors_div = convert_json(fig)

# Grades Histogram
fig = plot_histogram(grades_histogram_df, 'Grades Histogram', 'Grade', 'Number of Recorded Sends')
histogram_outdoors_div = convert_json(fig)

# Grades by Year
year_df = get.get_year(climbing_log_outdoors)
year_fig = plot_heatmap(year_df, "Heatmap of Grades by Year", "Year", "Grade")
year_outdoors_div = convert_json(year_fig)

# Grades by Wall-type
wall_df = get.get_wall(climbing_log_outdoors)
wall_fig = plot_heatmap(wall_df, "Heatmap of Grades by Wall-type", "Wall-type", "Grade",
	['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'crack', 'variable'])
wall_outdoors_div = convert_json(wall_fig)

# Grades by Hold-type
hold_df = get.get_hold(climbing_log_outdoors)
hold_fig = plot_heatmap(hold_df, "Heatmap of Grades by Hold-type", "Hold-type", "Grade",
	['jug', 'crimp', 'sloper', 'pinch'])
hold_outdoors_div = convert_json(hold_fig)

# Grades by Style
style_df = get.get_style(climbing_log_outdoors)
style_fig = plot_heatmap(style_df, "Heatmap of Grades by Style", "Style", "Grade",
	['mantle', 'natural', 'dyno', 'comp'])
style_outdoors_div = convert_json(style_fig)



# Initialize the app
app = Flask(__name__)

@app.route("/")
def index():
    return send_file("static/html/index.html")

@app.route("/indoors", methods=["POST", "GET"])
def indoors():
	return render_template(
    	"page.html",
    	scatter_div = Markup(scatter_indoors_div),
    	histogram_div = Markup(histogram_indoors_div),
    	year_div = Markup(year_indoors_div),
    	wall_div = Markup(wall_indoors_div),
    	hold_div = Markup(hold_indoors_div),
    	style_div = Markup(style_indoors_div)
    )

@app.route("/outdoors", methods=["POST", "GET"])
def outdoors():
	return render_template(
    	"page.html",
    	scatter_div = Markup(scatter_outdoors_div),
    	histogram_div = Markup(histogram_outdoors_div),
    	year_div = Markup(year_outdoors_div),
    	wall_div = Markup(wall_outdoors_div),
    	hold_div = Markup(hold_outdoors_div),
    	style_div = Markup(style_outdoors_div)
    )



# Start the server, continuously listen to requests.
# We'll have a running web app!

if __name__=="__main__":
    # For local development:
    #app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()