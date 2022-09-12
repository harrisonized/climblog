import os
import json
import plotly.offline as pyo
import plotly.io as pio
from climblog.utils.handlers.file_handler import get_defaults_from_ini
from climblog.utils.plotting import export_fig_to_json
from climblog.utils.curve_fit import curve_fit_new_grades
from climblog.apps.dashboard.get_data import (get_data_for_sends_by_date_scatter_from_csv,
                                              get_data_for_grades_histogram_from_csv,
                                              get_data_for_grades_by_year_heatmap_from_csv,
                                              get_data_for_grades_by_wall_heatmap_from_csv,
                                              get_data_for_grades_by_hold_heatmap_from_csv,
                                              get_data_for_grades_by_style_heatmap_from_csv)
from climblog.apps.dashboard.plot_fig import (plot_fig_for_sends_by_date_scatter,
                                              plot_fig_for_grades_histogram,
                                              plot_fig_for_grades_by_year_heatmap,
                                              plot_fig_for_grades_by_wall_heatmap,
                                              plot_fig_for_grades_by_hold_heatmap,
                                              plot_fig_for_grades_by_style_heatmap)

# test settings
default_settings = get_defaults_from_ini()
to_export_fig = default_settings.getboolean('to_export_fig')
fig_dir = 'figures/guest_portal'

# Functions included in this file:
# # retrieve_sends_by_date_scatter
# # retrieve_grades_histogram
# # retrieve_grades_by_year_heatmap
# # retrieve_grades_by_wall_heatmap
# # retrieve_grades_by_hold_heatmap
# # retrieve_grades_by_style_heatmap


"""
If figure in tmp folder, read directly from file
Else use postgres database to create figures
If postgres is unavailable, use data from csv to create figures (backup)
"""


def retrieve_sends_by_date_scatter(location_type,
                                   to_export_fig=to_export_fig):
    filename = 'sends-by-date'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        scatter_df = get_data_for_sends_by_date_scatter_from_csv(location_type, is_tmp=True)
        grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type, is_tmp=True)

        try:
            logistic_params = curve_fit_new_grades(grades_histogram_df)
        except:
            logistic_params = None

        fig = plot_fig_for_sends_by_date_scatter(scatter_df, logistic_params)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_histogram(location_type,
                              to_export_fig=to_export_fig):
    filename = 'grades-histogram'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type, is_tmp=True)

        fig = plot_fig_for_grades_histogram(grades_histogram_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_year_heatmap(location_type,
                                    to_export_fig=to_export_fig):
    filename = 'grades-by-year'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        table_df, year_df = get_data_for_grades_by_year_heatmap_from_csv(location_type, is_tmp=True)

        fig = plot_fig_for_grades_by_year_heatmap(table_df, year_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_wall_heatmap(location_type,
                                    to_export_fig=to_export_fig):
    filename = 'grades-by-wall-type'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        table_df, wall_df = get_data_for_grades_by_wall_heatmap_from_csv(location_type, is_tmp=True)

        fig = plot_fig_for_grades_by_wall_heatmap(table_df, wall_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_hold_heatmap(location_type,
                                    to_export_fig=to_export_fig):
    filename = 'grades-by-hold-type'
    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        table_df, hold_df = get_data_for_grades_by_hold_heatmap_from_csv(location_type, is_tmp=True)
        fig = plot_fig_for_grades_by_hold_heatmap(table_df, hold_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_style_heatmap(location_type,
                                     to_export_fig=to_export_fig):
    filename = 'grades-by-style'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        table_df, style_df = get_data_for_grades_by_style_heatmap_from_csv(location_type, is_tmp=True)
        fig = plot_fig_for_grades_by_style_heatmap(table_df, style_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div
