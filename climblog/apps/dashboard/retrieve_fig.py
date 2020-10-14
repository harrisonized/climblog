import os
import json
import plotly.offline as pyo
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
from .create_fig import (create_sends_by_date_scatter,
                         create_grades_histogram,
                         create_grades_by_year_heatmap,
                         create_grades_by_wall_heatmap,
                         create_grades_by_hold_heatmap,
                         create_grades_by_style_heatmap)
from .plotting.plotly import export_fig_to_json
from .math.curve_fit import curve_fit_new_grades

# test settings
to_save=False
use_csv_backup=False


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


def retrieve_sends_by_date_scatter(location_type, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'sends-by-date'

    if os.path.exists(f'{fig_dir}/{filename}.json'):
        with open(f'{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            scatter_df = get_data_for_sends_by_date_scatter_from_postgres(location_type)
            grades_histogram_df = get_data_for_grades_histogram_from_postgres(location_type)
        except:
            if use_csv_backup:
                scatter_df = get_data_for_sends_by_date_scatter_from_csv(location_type)
                grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type)

        logistic_params = curve_fit_new_grades(grades_histogram_df)
        fig = create_sends_by_date_scatter(scatter_df, logistic_params)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_histogram(location_type, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'grades-histogram'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            grades_histogram_df = get_data_for_grades_histogram_from_postgres(location_type)
        except:
            if use_csv_backup:
                grades_histogram_df = get_data_for_grades_histogram_from_csv(location_type)

        fig = create_grades_histogram(grades_histogram_df)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_year_heatmap(location_type, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'grades-by-year'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            table_df, year_df = get_data_for_grades_by_year_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, year_df = get_data_for_grades_by_year_heatmap_from_csv(location_type)

        fig = create_grades_by_year_heatmap(table_df, year_df)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_wall_heatmap(location_type, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'grades-by-wall-type'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            table_df, wall_df = get_data_for_grades_by_wall_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, wall_df = get_data_for_grades_by_wall_heatmap_from_csv(location_type)

        fig = create_grades_by_wall_heatmap(table_df, wall_df)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_hold_heatmap(location_type=None, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'grades-by-hold-type'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            table_df, hold_df = get_data_for_grades_by_hold_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, hold_df = get_data_for_grades_by_hold_heatmap_from_csv(location_type)

        fig = create_grades_by_hold_heatmap(table_df, hold_df)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_style_heatmap(location_type=None, to_save=to_save):

    fig_dir = f'tmp/figures/{location_type}'
    filename = 'grades-by-style'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):
        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

    else:

        try:
            table_df, style_df = get_data_for_grades_by_style_heatmap_from_postgres(location_type)
        except:
            if use_csv_backup:
                table_df, style_df = get_data_for_grades_by_style_heatmap_from_csv(location_type)

        fig = create_grades_by_style_heatmap(table_df, style_df)

        if to_save:
            export_fig_to_json(fig, fig_dir=fig_dir, filename=filename)

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div
