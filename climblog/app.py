import os
from flask import (Flask, request, Response,
	               send_file, render_template,
	               Markup)
# from flask_bootstrap import Bootstrap
from apps.dashboard.retrieve_fig import (retrieve_sends_by_date_scatter,
                                         retrieve_grades_histogram,
                                         retrieve_grades_by_year_heatmap,
                                         retrieve_grades_by_wall_heatmap,
                                         retrieve_grades_by_hold_heatmap,
                                         retrieve_grades_by_style_heatmap)

real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)


app = Flask(__name__)  # Initialize the app
# bootstrap = Bootstrap(app)


"""
Main Pages
"""

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/indoor", methods=["POST", "GET"])
def indoor():
    return render_template(
        "dashboard.html",
        location_type="Indoor",
    )


@app.route("/outdoor", methods=["POST", "GET"])
def outdoor():

    return render_template(
        "dashboard.html",
        location_type="Outdoor",
    )


"""
Figures
"""

@app.route("/fig/indoor/scatter", methods=["POST", "GET"])
def indoor_scatter():

    scatter_div = retrieve_sends_by_date_scatter('indoor')

    return render_template(
        "fig.html",
        div=Markup(scatter_div)
    )


@app.route("/fig/Indoor/histogram", methods=["POST", "GET"])
def indoor_histogram():

    histogram_div = retrieve_grades_histogram('indoor')

    return render_template(
        "fig.html",
        div=Markup(histogram_div)
    )


@app.route("/fig/Indoor/year", methods=["POST", "GET"])
def indoor_year():

    year_div = retrieve_grades_by_year_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(year_div)
    )


@app.route("/fig/Indoor/wall", methods=["POST", "GET"])
def indoor_wall():

    wall_div = retrieve_grades_by_wall_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(wall_div)
    )


@app.route("/fig/Indoor/hold", methods=["POST", "GET"])
def indoor_hold():

    hold_div = retrieve_grades_by_hold_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(hold_div)
    )


@app.route("/fig/Indoor/style", methods=["POST", "GET"])
def indoor_style():

    style_div = retrieve_grades_by_style_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(style_div)
    )


@app.route("/fig/Outdoor/scatter", methods=["POST", "GET"])
def outdoor_scatter():

    scatter_div = retrieve_sends_by_date_scatter('outdoor')

    return render_template(
        "fig.html",
        div=Markup(scatter_div)
    )


@app.route("/fig/Outdoor/histogram", methods=["POST", "GET"])
def outdoor_histogram():

    histogram_div = retrieve_grades_histogram('outdoor')

    return render_template(
        "fig.html",
        div=Markup(histogram_div)
    )


@app.route("/fig/Outdoor/year", methods=["POST", "GET"])
def outdoor_year():

    year_div = retrieve_grades_by_year_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(year_div)
    )


@app.route("/fig/Outdoor/wall", methods=["POST", "GET"])
def outdoor_wall():

    wall_div = retrieve_grades_by_wall_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(wall_div)
    )


@app.route("/fig/Outdoor/hold", methods=["POST", "GET"])
def outdoor_hold():

    hold_div = retrieve_grades_by_hold_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(hold_div)
    )


@app.route("/fig/Outdoor/style", methods=["POST", "GET"])
def outdoor_style():

    style_div = retrieve_grades_by_style_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(style_div)
    )
