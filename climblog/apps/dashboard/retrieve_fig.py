import os
import json
import plotly.offline as pyo
import plotly.io as pio
from climblog.utils.file_handler import get_defaults_from_ini
from climblog.utils.plotting import export_fig_to_json
from climblog.utils.math.curve_fit import curve_fit_new_grades
from .get_data import (get_data_for_sends_by_date_scatter_from_csv,
                       get_data_for_sends_by_date_scatter_from_postgres,
                       get_data_for_grades_histogram_from_csv,
                       get_data_for_grades_histogram_from_postgres,
                       get_data_for_grades_by_year_heatmap_from_csv,
                       get_data_for_grades_by_year_heatmap_from_postgres,
                       get_data_for_grades_by_wall_heatmap_from_csv,
                       get_data_for_grades_by_wall_heatmap_from_postgres,
                       get_data_for_grades_by_hold_heatmap_from_csv,
                       get_data_for_grades_by_hold_heatmap_from_postgres,
                       get_data_for_grades_by_style_heatmap_from_csv,
                       get_data_for_grades_by_style_heatmap_from_postgres)
from .plot_fig import (fig_for_sends_by_date_scatter,
                       fig_for_grades_histogram,
                       fig_for_grades_by_year_heatmap,
                       fig_for_grades_by_wall_heatmap,
                       fig_for_grades_by_hold_heatmap,
                       fig_for_grades_by_style_heatmap)

# test settings
default_settings = get_defaults_from_ini()
to_export_fig = default_settings.getboolean('to_export_fig')
use_csv_backup = default_settings.getboolean('use_csv_backup')
fig_dir = 'figures'

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
                                   to_export_fig=to_export_fig,
                                   use_csv_backup=use_csv_backup):
    filename = 'sends-by-date'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            scatter_df = get_data_for_sends_by_date_scatter_from_postgres(location_type)
        except:
            if use_csv_backup:
                scatter_df = get_data_for_sends_by_date_scatter_from_csv(location_type)

        try:
            grades_histogram_df = get_data_for_grades_histogram_from_postgres(location_type)
        except:
            if use_csv_backup:
                grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type)

        try:
            logistic_params = curve_fit_new_grades(grades_histogram_df)
        except:
            logistic_params = None

        fig = fig_for_sends_by_date_scatter(scatter_df, logistic_params)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_histogram(location_type,
                              to_export_fig=to_export_fig,
                              use_csv_backup=use_csv_backup):
    filename = 'grades-histogram'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            grades_histogram_df = get_data_for_grades_histogram_from_postgres(location_type)
        except:
            if use_csv_backup:
                grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type)

        fig = fig_for_grades_histogram(grades_histogram_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_year_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    use_csv_backup=use_csv_backup):
    filename = 'grades-by-year'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            table_df, year_df = get_data_for_grades_by_year_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, year_df = get_data_for_grades_by_year_heatmap_from_csv(location_type)

        fig = fig_for_grades_by_year_heatmap(table_df, year_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_wall_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    use_csv_backup=use_csv_backup):
    filename = 'grades-by-wall-type'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            table_df, wall_df = get_data_for_grades_by_wall_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, wall_df = get_data_for_grades_by_wall_heatmap_from_csv(location_type)

        fig = fig_for_grades_by_wall_heatmap(table_df, wall_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_hold_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    use_csv_backup=use_csv_backup):
    filename = 'grades-by-hold-type'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            table_df, hold_df = get_data_for_grades_by_hold_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, hold_df = get_data_for_grades_by_hold_heatmap_from_csv(location_type)

        fig = fig_for_grades_by_hold_heatmap(table_df, hold_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_style_heatmap(location_type,
                                     to_export_fig=to_export_fig,
                                     use_csv_backup=use_csv_backup):
    filename = 'grades-by-style'

    if os.path.exists(f'tmp/{fig_dir}/{location_type}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{location_type}/{filename}.json') as file:
            fig = json.load(file)
        print(f'{filename} retrieved from tmp')

    else:

        try:
            table_df, style_df = get_data_for_grades_by_style_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, style_df = get_data_for_grades_by_style_heatmap_from_csv(location_type)

        fig = fig_for_grades_by_style_heatmap(table_df, style_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div
