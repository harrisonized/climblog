"""Main functions for figure generation from the routes
"""
from functools import partial
import datetime as dt
import plotly.offline as pyo
import plotly.io as pio

from climblog.utils.plotting import export_fig_to_json
from climblog.utils.handlers.file_handler import read_json
from climblog.utils.auth.connections import query_sql_or_csv
from climblog.utils.curve_fit import curve_fit_logistic_boundary
from climblog.etc.columns import sends_by_date_scatter_columns
from climblog.etc.params import heatmap_params
from climblog.etc.settings import use_csv_backup, read_fig_from_cache, export_fig
from climblog.etc.queries import queries

from .plot_fig import (plot_fig_for_sends_by_date_scatter,
                       plot_fig_for_grades_histogram,
                       plot_fig_for_grades_by_heatmap)

# Functions
# # generate_sends_by_date_scatter
# # generate_grades_histogram
# # generate_grades_by_heatmap

# Objects
# # generate_fig_switch


def generate_sends_by_date_scatter(location_type,
                                   filename='sends-by-date',
                                   data_dir='data',
                                   fig_dir='tmp/figures',
                                   query_db=True,
                                   ):

    fig = read_json(f'{fig_dir}/{location_type}/{filename}.json') if read_fig_from_cache else None
    
    if not fig:

        # vanilla scatterplot data
        scatter_df = query_sql_or_csv(
            db_query=queries['GET_PRIMARY_DATA'].format(datasource='boulders', location_type=location_type) if query_db else None,
            df_query=None,
            csv_filepath=f'{data_dir}/climbing-log.csv' if use_csv_backup else None,
            default_columns=sends_by_date_scatter_columns
        )
        scatter_df = scatter_df[(scatter_df['location_type'] == location_type)].copy()
        scatter_df['date_'] = scatter_df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))
        
        # add boundary
        try:
            grades_histogram_df = query_sql_or_csv(
                db_query=queries['histogram']['COUNT_GRADES'].format(datasource='boulders', location_type=location_type) if query_db else None,
                df_query=queries['histogram']['COUNT_GRADES'].format(datasource='dataframe', location_type=location_type),
                csv_filepath=f'{data_dir}/climbing-log.csv',
                default_columns=sends_by_date_scatter_columns
            )
            grades_histogram_df = grades_histogram_df.drop_duplicates(subset=[grades_histogram_df.columns[0], grades_histogram_df.columns[1]])
            
            logistic_params = curve_fit_logistic_boundary(grades_histogram_df, x='date_', y='grade')
        except:
            logistic_params = None

        fig = plot_fig_for_sends_by_date_scatter(scatter_df, logistic_params)

        if export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def generate_grades_histogram(location_type,
                              filename='grades-histogram',
                              data_dir='data',
                              fig_dir='tmp/figures',
                              query_db=True,
                              ):

    fig = read_json(f'{fig_dir}/{location_type}/{filename}.json') if read_fig_from_cache else None

    if not fig:
        grades_histogram_df = query_sql_or_csv(
            db_query=queries['histogram']['COUNT_GRADES'].format(datasource='boulders', location_type=location_type) if query_db else None,
            df_query=queries['histogram']['COUNT_GRADES'].format(datasource='dataframe', location_type=location_type),
            csv_filepath=f'{data_dir}/climbing-log.csv' if use_csv_backup else None,
            default_columns=sends_by_date_scatter_columns
        )
        grades_histogram_df = grades_histogram_df.drop_duplicates(subset=[grades_histogram_df.columns[0], grades_histogram_df.columns[1]])

        fig = plot_fig_for_grades_histogram(grades_histogram_df)

        if export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def generate_grades_by_heatmap(location_type,
                               filename,  # from params
                               xlabel,  # from params
                               db_query_name,  # from params
                               df_query_name,  # from params
                               columns=None,  # from params
                               data_dir='data',
                               fig_dir='tmp/figures',
                               query_db=True,
                               ):
    """General function to plot all heatmaps
    """

    fig = read_json(f'{fig_dir}/{location_type}/{filename}.json') if read_fig_from_cache else None

    # if figure not found, generate from raw data
    if not fig:

        # heatmap_df
        df = query_sql_or_csv(
            db_query=queries['heatmap'][db_query_name].format(datasource='boulders', location_type=location_type) if query_db else None,
            df_query=queries['heatmap'][df_query_name].format(datasource='dataframe', location_type=location_type),
            csv_filepath=f'{data_dir}/climbing-log.csv' if use_csv_backup else None,
            default_columns=sends_by_date_scatter_columns
        )
        df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])

        # hover_df
        table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
        table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
        if columns is not None:
            table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns


        fig = plot_fig_for_grades_by_heatmap(
            table_df,  # heatmap_df
            df,  # hover_df
            xlabel=xlabel,
            columns=columns,
        )

        if export_fig:
            export_fig_to_json(fig,
                               fig_dir=f'{fig_dir}/{location_type}',
                               filename=filename)
        print(f'{filename} generated from data')

    # div = pyo.plot(fig, output_type='div')  # div for fig
    div = pio.to_html(fig, full_html=True, include_plotlyjs=True, default_height=500)

    return div


generate_fig_switch = {
    'timeseries': generate_sends_by_date_scatter,
    'histogram': generate_grades_histogram,
    'year': partial(generate_grades_by_heatmap, **heatmap_params['grades_by_year']),
    'wall': partial(generate_grades_by_heatmap, **heatmap_params['grades_by_wall']),
    'hold': partial(generate_grades_by_heatmap, **heatmap_params['grades_by_hold']),
    'style': partial(generate_grades_by_heatmap, **heatmap_params['grades_by_style'])
}
