"""
If figure in tmp folder, read directly from file
Else use postgres database to create figures
If postgres is unavailable, use data from csv to create figures (backup)
"""

import os
import json
import plotly.offline as pyo
import plotly.io as pio
from climblog.utils.handlers.file_handler import get_defaults_from_ini
from climblog.utils.plotting import export_fig_to_json
from .get_data import (get_data_for_sends_by_date_scatter,
                       get_data_for_grades_histogram,
                       get_data_for_grades_by_heatmap)
from .plot_fig import (curve_fit_new_grades,
                       plot_fig_for_sends_by_date_scatter,
                       plot_fig_for_grades_histogram,
                       plot_fig_for_grades_by_heatmap)

from climblog.etc.params import heatmap_params
from climblog.factories import queries

# test settings
default_settings = get_defaults_from_ini()
to_export_fig = default_settings.getboolean('to_export_fig')
use_csv_backup = default_settings.getboolean('use_csv_backup')

fig_dir = 'figures'


# Functions
# # retrieve_fig_from_tmp_json
# # retrieve_sends_by_date_scatter
# # retrieve_grades_histogram
# # retrieve_grades_by_heatmap
# # retrieve_grades_by_year_heatmap
# # retrieve_grades_by_wall_heatmap
# # retrieve_grades_by_hold_heatmap
# # retrieve_grades_by_style_heatmap


def retrieve_fig_from_tmp_json(filename,
                               subdir,
                               fig_dir='figures'):
    """Retrieves figure from hardcoded path
    """
    filepath = f'tmp/{fig_dir}/{subdir}/{filename}.json'
    if os.path.exists(filepath):
        with open(filepath) as f:
            fig = json.load(f)
        print(f'{filename} retrieved from tmp')
        return fig


def retrieve_sends_by_date_scatter(location_type,
                                   filename = 'sends-by-date',
                                   fig_dir = 'figures',
                                   to_export_fig=to_export_fig,
                                   use_csv_backup=use_csv_backup,
                                   is_tmp=False,
                                   ):
    
    # fig = retrieve_fig_from_tmp_json(filename, location_type)
    fig = None
    if not fig:
        scatter_df = get_data_for_sends_by_date_scatter(location_type)

        try:
            grades_histogram_df = get_data_for_grades_histogram(location_type)
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
                              filename = 'grades-histogram',
                              fig_dir = 'figures',
                              to_export_fig=to_export_fig,
                              use_csv_backup=use_csv_backup,
                              is_tmp=False,
                              ):
    
    fig = retrieve_fig_from_tmp_json(filename, location_type)

    if not fig:
        grades_histogram_df = get_data_for_grades_histogram(location_type)
        fig = plot_fig_for_grades_histogram(grades_histogram_df)

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_heatmap(location_type,
                               filename,  # from params
                               xlabel,  # from params
                               query_pg,  # from params
                               query_df,  # from params
                               columns=None,  # from params
                               query_dir='heatmap', # params
                               fig_dir = 'figures',
                               to_export_fig=to_export_fig,
                               use_csv_backup=use_csv_backup,
                               is_tmp=False,
                               ):
    """General function to plot all heatmaps
    """

    # get figure from json
    fig = retrieve_fig_from_tmp_json(filename, location_type)

    # if figure not found, generate from raw data
    if not fig:
        heatmap_input_df, hovertext_input_df = get_data_for_grades_by_heatmap(
            location_type=location_type,
            query_pg=query_pg,
            query_df=query_df,
            columns=columns,
            query_dir=query_dir,
        )
        fig = plot_fig_for_grades_by_heatmap(
            heatmap_input_df,
            hovertext_input_df,
            xlabel=xlabel,
            columns=columns,
        )

        if to_export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'tmp/{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


def retrieve_grades_by_year_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    fig_dir = 'figures',
                                    use_csv_backup=use_csv_backup,
                                    is_tmp=False,
                                    ):
    
    div = retrieve_grades_by_heatmap(
        location_type=location_type,
        to_export_fig=to_export_fig,
        use_csv_backup=use_csv_backup,
        fig_dir = 'figures',
        **heatmap_params['grades_by_year']
    )
    return div


def retrieve_grades_by_wall_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    fig_dir = 'figures',
                                    use_csv_backup=use_csv_backup,
                                    is_tmp=False,
                                    ):

    div = retrieve_grades_by_heatmap(
        location_type=location_type,
        to_export_fig=to_export_fig,
        use_csv_backup=use_csv_backup,
        fig_dir = 'figures',
        **heatmap_params['grades_by_wall']
    )
    return div


def retrieve_grades_by_hold_heatmap(location_type,
                                    to_export_fig=to_export_fig,
                                    fig_dir = 'figures',
                                    use_csv_backup=use_csv_backup,
                                    is_tmp=False,
                                    ):
    

    div = retrieve_grades_by_heatmap(
        location_type=location_type,
        to_export_fig=to_export_fig,
        use_csv_backup=use_csv_backup,
        fig_dir = 'figures',
        **heatmap_params['grades_by_hold']
    )
    return div


def retrieve_grades_by_style_heatmap(location_type,
                                     to_export_fig=to_export_fig,
                                     fig_dir = 'figures',
                                     use_csv_backup=use_csv_backup,
                                     is_tmp=False,
                                     ):
    div = retrieve_grades_by_heatmap(
        location_type=location_type,
        to_export_fig=to_export_fig,
        use_csv_backup=use_csv_backup,
        fig_dir = 'figures',
        **heatmap_params['grades_by_style']
    )
    return div
