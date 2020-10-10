import json
import plotly
import plotly.offline as pyo
from apps.plotting.get_data import get_histogram, get_scatter, get_year, get_wall, get_hold, get_style
from apps.plotting.plotly_tools import color_dict, plot_scatter, plot_histogram, plot_heatmap
from apps.plotting.curve_fit import curve_fit_new_grades, logistic_func


def div_for_fig(fig):
    json_str = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig_dict = json.loads(json_str)
    # fig_go = go.Figure(data = fig_dict['data'], layout = fig_dict['layout'])
    div = pyo.plot(fig_dict, output_type='div')
    return div


def refresh_histogram(df):
    """Grades Histogram
    """
    grades_histogram_df = get_histogram(df, color_dict)
    fig = plot_histogram(grades_histogram_df, 'Grades Histogram', 'Grade', 'Number of Recorded Sends')
    histogram_div = div_for_fig(fig)

    return histogram_div


def refresh_scatter(df):
    """Scatter
    """
    scatter_df = get_scatter(df, color_dict)

    grades_histogram_df = get_histogram(df, color_dict)
    popt = curve_fit_new_grades(grades_histogram_df)

    fig = plot_scatter(scatter_df, popt, "Sends by Date", "Date", "Grade")
    scatter_div = div_for_fig(fig)

    return scatter_div, fig


def refresh_heatmap(df):
    """
    """

    # Grades by Year
    year_df = get_year(df)
    year_fig = plot_heatmap(year_df, "Heatmap of Grades by Year", "Year", "Grade")
    year_div = div_for_fig(year_fig)

    # Grades by Wall-type
    wall_df = get_wall(df)
    wall_fig = plot_heatmap(wall_df, "Heatmap of Grades by Wall-type", "Wall-type", "Grade",
                            ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable'])
    wall_div = div_for_fig(wall_fig)

    # Grades by Hold-type
    hold_df = get_hold(df)
    hold_fig = plot_heatmap(hold_df, "Heatmap of Grades by Hold-type", "Hold-type", "Grade",
                            ['jug', 'crimp', 'sloper', 'pinch'])
    hold_div = div_for_fig(hold_fig)

    # Grades by Style
    style_df = get_style(df)
    style_fig = plot_heatmap(style_df, "Heatmap of Grades by Style", "Style", "Grade",
                             ['mantle', 'natural', 'dyno', 'comp'])
    style_div = div_for_fig(style_fig)

    return year_div, wall_div, hold_div, style_div
