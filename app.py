import json
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.offline as pyo
from flask import request, Response, send_file, render_template, Markup, Flask
# from flask_bootstrap import Bootstrap
from apps.plotting.refresh_figures import refresh_scatter, refresh_histogram, refresh_heatmap


# Initialize the app
app = Flask(__name__)
# bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/indoors", methods=["POST", "GET"])
def indoors():

    climbing_log_indoors = pd.read_csv('data/climbing-log-indoors.csv')  # Read in data
    scatter_indoors_div, fig = refresh_scatter(climbing_log_indoors)
    histogram_indoors_div = refresh_histogram(climbing_log_indoors)
    year_indoors_div, wall_indoors_div, hold_indoors_div, style_indoors_div = refresh_heatmap(climbing_log_indoors)

    return render_template(
        "page.html",
        scatter_div=Markup(scatter_indoors_div),
        histogram_div=Markup(histogram_indoors_div),
        year_div=Markup(year_indoors_div),
        wall_div=Markup(wall_indoors_div),
        hold_div=Markup(hold_indoors_div),
        style_div=Markup(style_indoors_div)
    )


@app.route("/outdoors", methods=["POST", "GET"])
def outdoors():

    climbing_log_outdoors = pd.read_csv('data/climbing-log-outdoors.csv')  # Read in data
    scatter_outdoors_div, fig = refresh_scatter(climbing_log_outdoors)
    histogram_outdoors_div = refresh_histogram(climbing_log_outdoors)
    year_outdoors_div, wall_outdoors_div, hold_outdoors_div, style_outdoors_div = refresh_heatmap(climbing_log_outdoors)

    return render_template(
        "page.html",
        scatter_div=Markup(scatter_outdoors_div),
        histogram_div=Markup(histogram_outdoors_div),
        year_div=Markup(year_outdoors_div),
        wall_div=Markup(wall_outdoors_div),
        hold_div=Markup(hold_outdoors_div),
        style_div=Markup(style_outdoors_div)
    )

@app.route("/test", methods=["POST", "GET"])
def test():

    climbing_log_outdoors = pd.read_csv('data/climbing-log-outdoors.csv')  # Read in data
    div, fig = refresh_scatter(climbing_log_outdoors)

    # Save
    with open(f'figures/outdoors/sends-by-date.json', 'w') as outfile:
        json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

    # Read in saved data
    with open('figures/outdoors/sends-by-date.json') as json_file:
        fig_json = json.load(json_file)
    fig = go.Figure(data = fig_json['data'], layout = fig_json['layout'])
    scatter_outdoors_div = pyo.plot(fig, output_type='div')

    return render_template(
        "page.html",
        scatter_div=Markup(scatter_outdoors_div),
        # histogram_div=Markup(histogram_outdoors_div),
        # year_div=Markup(year_outdoors_div),
        # wall_div=Markup(wall_outdoors_div),
        # hold_div=Markup(hold_outdoors_div),
        # style_div=Markup(style_outdoors_div)
    )
