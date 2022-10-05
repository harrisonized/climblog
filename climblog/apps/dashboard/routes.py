"""Displays climbing data for Harrison Wang
"""

from flask import Blueprint, Markup
from flask import render_template
from .generate_fig import generate_fig_switch


dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates',
                      static_folder='static')


# ----------------------------------------------------------------------
# Home pages

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


# ----------------------------------------------------------------------
# Figures

@dashboard.route("/fig/<location_type>/<plot_type>", methods=["GET"])
def plot(location_type, plot_type):

    div = generate_fig_switch[plot_type](location_type)  # see generate_fig.py

    return render_template(
        "fig.html",
        div=Markup(div)
    )
