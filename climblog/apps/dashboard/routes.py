from flask import Blueprint, Markup
from flask import render_template
from climblog.apps.dashboard.retrieve_fig import (retrieve_sends_by_date_scatter,
                                                  retrieve_grades_histogram,
                                                  retrieve_grades_by_year_heatmap,
                                                  retrieve_grades_by_wall_heatmap,
                                                  retrieve_grades_by_hold_heatmap,
                                                  retrieve_grades_by_style_heatmap)


retrieve_plot = {'timeseries': retrieve_sends_by_date_scatter,
                 'histogram': retrieve_grades_histogram,
                 'year': retrieve_grades_by_year_heatmap,
                 'wall': retrieve_grades_by_wall_heatmap,
                 'hold': retrieve_grades_by_hold_heatmap,
                 'style': retrieve_grades_by_style_heatmap,
                 }


dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates',
                      static_folder='static')


@dashboard.route("/indoor", methods=["GET"])
def indoor():
    location_type = {'title': 'Indoor', 'lower': 'indoor', }
    return render_template(
        "dashboard.html",
        location_type=location_type,
    )


@dashboard.route("/outdoor", methods=["GET"])
def outdoor():
    location_type = {'title': 'Outdoor', 'lower': 'outdoor', }
    return render_template(
        "dashboard.html",
        location_type=location_type,
    )


@dashboard.route("/fig/<location_type>/<plot_type>", methods=["GET"])
def plot(location_type, plot_type):

    div = retrieve_plot[plot_type](location_type)

    return render_template(
        "fig.html",
        div=Markup(div)
    )
