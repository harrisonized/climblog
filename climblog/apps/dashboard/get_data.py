import os
import datetime as dt
import pandas as pd
import pandas.io.sql as pd_sql
from apps.dashboard.query.query_tools import execute_query_on_df
from apps.auth.connections import postgres_connection
from .plotting.colors import color_dict
from .queries import SENDS_BY_DATE, GRADES_HISTOGRAM, GRADES_BY_YEAR, GRADES_BY_WALL, GRADES_BY_HOLD, GRADES_BY_STYLE

connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')  # test locally


# Functions included in this file:
# # get_data_for_sends_by_date_scatter_from_csv
# # get_data_for_sends_by_date_scatter_from_postgres
# # get_data_for_grades_histogram_from_csv
# # get_data_for_grades_histogram_from_postgres
# # get_data_for_grades_by_year_heatmap_from_csv
# # get_data_for_grades_by_year_heatmap_from_postgres
# # get_data_for_grades_by_wall_heatmap_from_csv
# # get_data_for_grades_by_wall_heatmap_from_postgres
# # get_data_for_grades_by_hold_heatmap_from_csv
# # get_data_for_grades_by_hold_heatmap_from_postgres
# # get_data_for_grades_by_style_heatmap_from_csv
# # get_data_for_grades_by_style_heatmap_from_postgres


def get_data_for_sends_by_date_scatter_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    scatter_df = execute_query_on_df(SENDS_BY_DATE, climbing_log_df)
    scatter_df['grade_'] = scatter_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    scatter_df['date_'] = scatter_df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))  # Convert to datetime
    scatter_df['color'] = scatter_df['color'].replace(color_dict)  # Replace colors with hex codes

    return scatter_df


def get_data_for_sends_by_date_scatter_from_postgres(location_type):
    """Refactor this
    """

    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'

    scatter_df = execute_query_on_df(SENDS_BY_DATE, climbing_log_df)
    scatter_df['grade_'] = scatter_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    scatter_df['date_'] = scatter_df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))  # Convert to datetime
    scatter_df['color'] = scatter_df['color'].replace(color_dict)  # Replace colors with hex codes

    return scatter_df


def get_data_for_grades_histogram_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    grades_histogram_df = execute_query_on_df(GRADES_HISTOGRAM, climbing_log_df)
    grades_histogram_df['grade_'] = grades_histogram_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    grades_histogram_df['color'] = grades_histogram_df['color'].replace(color_dict)

    return grades_histogram_df


def get_data_for_grades_histogram_from_postgres(location_type):
    """Refactor this
    """

    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'
    
    grades_histogram_df = execute_query_on_df(GRADES_HISTOGRAM, climbing_log_df)
    grades_histogram_df['grade_'] = grades_histogram_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    grades_histogram_df['color'] = grades_histogram_df['color'].replace(color_dict)

    return grades_histogram_df


def get_data_for_grades_by_year_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    year_df = execute_query_on_df(GRADES_BY_YEAR, climbing_log_df)
    year_df['grade_'] = year_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = year_df.reset_index().pivot(index=year_df.columns[1], columns=year_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, year_df


def get_data_for_grades_by_year_heatmap_from_postgres(location_type):
    """Refactor this
    """

    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'
    
    year_df = execute_query_on_df(GRADES_BY_YEAR, climbing_log_df)
    year_df['grade_'] = year_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = year_df.reset_index().pivot(index=year_df.columns[1], columns=year_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, year_df


def get_data_for_grades_by_wall_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    wall_df = execute_query_on_df(GRADES_BY_WALL, climbing_log_df)
    wall_df['grade_'] = wall_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = wall_df.reset_index().pivot(index=wall_df.columns[1], columns=wall_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, wall_df


def get_data_for_grades_by_wall_heatmap_from_postgres(location_type):
    """Refactor this
    """

    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'
    
    wall_df = execute_query_on_df(GRADES_BY_WALL, climbing_log_df)
    wall_df['grade_'] = wall_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = wall_df.reset_index().pivot(index=wall_df.columns[1], columns=wall_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, wall_df


def get_data_for_grades_by_hold_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    hold_df = execute_query_on_df(GRADES_BY_HOLD, climbing_log_df)
    hold_df['grade_'] = hold_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = hold_df.reset_index().pivot(index=hold_df.columns[1], columns=hold_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, hold_df


def get_data_for_grades_by_hold_heatmap_from_postgres(location_type):
    """Refactor this
    """

    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'
    
    hold_df = execute_query_on_df(GRADES_BY_HOLD, climbing_log_df)
    hold_df['grade_'] = hold_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = hold_df.reset_index().pivot(index=hold_df.columns[1], columns=hold_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, hold_df


def get_data_for_grades_by_style_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    style_df = execute_query_on_df(GRADES_BY_STYLE, climbing_log_df)
    style_df['grade_'] = style_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = style_df.reset_index().pivot(index=style_df.columns[1], columns=style_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, style_df


def get_data_for_grades_by_style_heatmap_from_postgres(location_type):
    """Refactor this
    """
    
    query = f"""
    SELECT *
    FROM route_info
    WHERE location_type = '{location_type}'
    ;
    """
    climbing_log_df = pd_sql.read_sql(query, connection_uri)
    assert climbing_log_df.empty is False, 'No data returned'
    
    style_df = execute_query_on_df(GRADES_BY_STYLE, climbing_log_df)
    style_df['grade_'] = style_df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = style_df.reset_index().pivot(index=style_df.columns[1], columns=style_df.columns[0], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, style_df
