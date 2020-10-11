import os
import json
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.offline as pyo
from flask import request, Response, send_file, render_template, Markup, Flask
# from flask_bootstrap import Bootstrap
from apps.plotting.retrieve_fig import (retrieve_sends_by_date_scatter,
                                        retrieve_grades_histogram,
                                        retrieve_grades_by_year_heatmap,
                                        retrieve_grades_by_wall_heatmap,
                                        retrieve_grades_by_hold_heatmap,
                                        retrieve_grades_by_style_heatmap)


# Initialize the app
app = Flask(__name__)
# bootstrap = Bootstrap(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/indoors", methods=["POST", "GET"])
def indoors():

    fig_dir = 'figures/indoors'
    data_path = 'data/climbing-log-indoors.csv'

    scatter_div = retrieve_sends_by_date_scatter(fig_dir, data_path)
    histogram_div = retrieve_grades_histogram(fig_dir, data_path)
    year_div = retrieve_grades_by_year_heatmap(fig_dir, data_path)
    wall_div = retrieve_grades_by_wall_heatmap(fig_dir, data_path)
    hold_div = retrieve_grades_by_hold_heatmap(fig_dir, data_path)
    style_div = retrieve_grades_by_style_heatmap(fig_dir, data_path)

    return render_template(
        "figures.html",
        scatter_div=Markup(scatter_div),
        histogram_div=Markup(histogram_div),
        year_div=Markup(year_div),
        wall_div=Markup(wall_div),
        hold_div=Markup(hold_div),
        style_div=Markup(style_div)
    )


@app.route("/outdoors", methods=["POST", "GET"])
def outdoors():

    fig_dir = 'figures/outdoors'
    data_path = 'data/climbing-log-outdoors.csv'

    scatter_div = retrieve_sends_by_date_scatter(fig_dir, data_path)
    histogram_div = retrieve_grades_histogram(fig_dir, data_path)
    year_div = retrieve_grades_by_year_heatmap(fig_dir, data_path)
    wall_div = retrieve_grades_by_wall_heatmap(fig_dir, data_path)
    hold_div = retrieve_grades_by_hold_heatmap(fig_dir, data_path)
    style_div = retrieve_grades_by_style_heatmap(fig_dir, data_path)

    return render_template(
        "figures.html",
        scatter_div=Markup(scatter_div),
        histogram_div=Markup(histogram_div),
        year_div=Markup(year_div),
        wall_div=Markup(wall_div),
        hold_div=Markup(hold_div),
        style_div=Markup(style_div)
    )
