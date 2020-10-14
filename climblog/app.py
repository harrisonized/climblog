from flask import request, Response, send_file, render_template, Markup, Flask
# from flask_bootstrap import Bootstrap
from apps.dashboard.retrieve_fig import (retrieve_sends_by_date_scatter,
                                         retrieve_grades_histogram,
                                         retrieve_grades_by_year_heatmap,
                                         retrieve_grades_by_wall_heatmap,
                                         retrieve_grades_by_hold_heatmap,
                                         retrieve_grades_by_style_heatmap)

app = Flask(__name__)  # Initialize the app


# bootstrap = Bootstrap(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/indoor", methods=["POST", "GET"])
def indoor():
    scatter_div = retrieve_sends_by_date_scatter('indoor')
    histogram_div = retrieve_grades_histogram('indoor')
    year_div = retrieve_grades_by_year_heatmap('indoor')
    wall_div = retrieve_grades_by_wall_heatmap('indoor')
    hold_div = retrieve_grades_by_hold_heatmap('indoor')
    style_div = retrieve_grades_by_style_heatmap('indoor')

    return render_template(
        "figures.html",
        scatter_div=Markup(scatter_div),
        histogram_div=Markup(histogram_div),
        year_div=Markup(year_div),
        wall_div=Markup(wall_div),
        hold_div=Markup(hold_div),
        style_div=Markup(style_div)
    )


@app.route("/outdoor", methods=["POST", "GET"])
def outdoor():
    scatter_div = retrieve_sends_by_date_scatter('outdoor')
    histogram_div = retrieve_grades_histogram('outdoor')
    year_div = retrieve_grades_by_year_heatmap('outdoor')
    wall_div = retrieve_grades_by_wall_heatmap('outdoor')
    hold_div = retrieve_grades_by_hold_heatmap('outdoor')
    style_div = retrieve_grades_by_style_heatmap('outdoor')

    return render_template(
        "figures.html",
        scatter_div=Markup(scatter_div),
        histogram_div=Markup(histogram_div),
        year_div=Markup(year_div),
        wall_div=Markup(wall_div),
        hold_div=Markup(hold_div),
        style_div=Markup(style_div)
    )


@app.route("/test", methods=["POST", "GET"])
def test():
    return render_template(
        "figures.html",
    )
