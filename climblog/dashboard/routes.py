from flask import Blueprint, Markup
from flask import render_template
from apps.dashboard.retrieve_fig import (retrieve_sends_by_date_scatter,
                                         retrieve_grades_histogram,
                                         retrieve_grades_by_year_heatmap,
                                         retrieve_grades_by_wall_heatmap,
                                         retrieve_grades_by_hold_heatmap,
                                         retrieve_grades_by_style_heatmap)


fig_bp = Blueprint('fig_bp', __name__,
                   template_folder='templates',
                   static_folder='static')


@fig_bp.route("/fig/indoor/timeseries", methods=["GET"])
def indoor_timeseries():

    div = retrieve_sends_by_date_scatter('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/indoor/histogram", methods=["GET"])
def indoor_histogram():

    div = retrieve_grades_histogram('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/indoor/year", methods=["GET"])
def indoor_year():

    div = retrieve_grades_by_year_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/indoor/wall", methods=["GET"])
def indoor_wall():

    div = retrieve_grades_by_wall_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/indoor/hold", methods=["GET"])
def indoor_hold():

    div = retrieve_grades_by_hold_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/indoor/style", methods=["GET"])
def indoor_style():

    div = retrieve_grades_by_style_heatmap('indoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/timeseries", methods=["GET"])
def outdoor_timeseries():

    div = retrieve_sends_by_date_scatter('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/histogram", methods=["GET"])
def outdoor_histogram():

    div = retrieve_grades_histogram('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/year", methods=["GET"])
def outdoor_year():

    div = retrieve_grades_by_year_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/wall", methods=["GET"])
def outdoor_wall():

    div = retrieve_grades_by_wall_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/hold", methods=["GET"])
def outdoor_hold():

    div = retrieve_grades_by_hold_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )


@fig_bp.route("/fig/outdoor/style", methods=["GET"])
def outdoor_style():

    div = retrieve_grades_by_style_heatmap('outdoor')

    return render_template(
        "fig.html",
        div=Markup(div)
    )
