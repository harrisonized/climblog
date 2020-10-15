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


@app.route("/indoor", methods=["GET"])
def indoor():

    location_type = {'title': 'Indoor',
                     'lower': 'indoor',}

    return render_template(
        "dashboard.html",
        location_type=location_type,
    )


@app.route("/outdoor", methods=["GET"])
def outdoor():

    location_type = {'title': 'Outdoor',
                     'lower': 'outdoor',}

    return render_template(
        "dashboard.html",
        location_type=location_type,
    )


# @app.route("/test", methods=["GET"])
# def test():

#     scatter_div = retrieve_sends_by_date_scatter('indoor')

#     return render_template(
#         "test.html",
#         location_type='indoor',
#         div=Markup(scatter_div)
#     )


"""
Figures
"""

@app.route("/fig/indoor/timeseries", methods=["GET"])
def indoor_timeseries():

    div = retrieve_sends_by_date_scatter('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/indoor/histogram", methods=["GET"])
def indoor_histogram():

    div = retrieve_grades_histogram('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/indoor/year", methods=["GET"])
def indoor_year():

    div = retrieve_grades_by_year_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/indoor/wall", methods=["GET"])
def indoor_wall():

    div = retrieve_grades_by_wall_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/indoor/hold", methods=["GET"])
def indoor_hold():

    div = retrieve_grades_by_hold_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/indoor/style", methods=["GET"])
def indoor_style():

    div = retrieve_grades_by_style_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/timeseries", methods=["GET"])
def outdoor_timeseries():

    div = retrieve_sends_by_date_scatter('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/histogram", methods=["GET"])
def outdoor_histogram():

    div = retrieve_grades_histogram('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/year", methods=["GET"])
def outdoor_year():

    div = retrieve_grades_by_year_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/wall", methods=["GET"])
def outdoor_wall():

    div = retrieve_grades_by_wall_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/hold", methods=["GET"])
def outdoor_hold():

    div = retrieve_grades_by_hold_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@app.route("/fig/outdoor/style", methods=["GET"])
def outdoor_style():

    div = retrieve_grades_by_style_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )
