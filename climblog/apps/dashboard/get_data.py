import os
import datetime as dt
import pandas as pd
import pandas.io.sql as pd_sql
from apps.auth.connections import postgres_connection
from apps.utils.query.query_tools import execute_query_on_df
from apps.utils.plotting.colors import color_name_to_hex
from .queries import (GET_PRIMARY_DATA,
                      COUNT_GRADES,
                      COUNT_GRADES_BY_YEAR_FROM_DF,
                      COUNT_GRADES_BY_YEAR_FROM_PG,
                      COUNT_GRADES_BY_WALL,
                      COUNT_GRADES_BY_HOLD_FROM_DF,
                      COUNT_GRADES_BY_HOLD_FROM_PG,
                      COUNT_GRADES_BY_STYLE)

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
    df = pd.read_csv(csv_path)

    df['grade_'] = df['grade'].apply(lambda x: x.split('-')[0]).apply(lambda x: x.replace('V', '')).astype(int)
    df['date_'] = df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes
    df = df.rename(columns = {'grade': 'vgrade'})

    return df


def get_data_for_sends_by_date_scatter_from_postgres(location_type):

    df = pd_sql.read_sql(
        GET_PRIMARY_DATA.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    df['date_'] = df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))  # Convert to datetime
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes
    
    return df


def get_data_for_grades_histogram_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)

    df = execute_query_on_df(
        COUNT_GRADES.format(datasource='dataframe', location_type=location_type), climbing_log_df)
    
    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    df['color'] = df['color'].replace(color_name_to_hex)

    return df


def get_data_for_grades_histogram_from_postgres(location_type):

    df = pd_sql.read_sql(
       COUNT_GRADES.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes
    
    return df


def get_data_for_grades_by_year_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    df = execute_query_on_df(
        COUNT_GRADES_BY_YEAR_FROM_DF.format(location_type=location_type), climbing_log_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = df.reset_index().pivot(index=df.columns[0],
                                      columns=df.columns[1],
                                      values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, df


def get_data_for_grades_by_year_heatmap_from_postgres(location_type):

    df = pd_sql.read_sql(
       COUNT_GRADES_BY_YEAR_FROM_PG.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'
    
    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, df


def get_data_for_grades_by_wall_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)
    df = execute_query_on_df(
        COUNT_GRADES_BY_WALL.format(datasource='dataframe', location_type=location_type), climbing_log_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df


def get_data_for_grades_by_wall_heatmap_from_postgres(location_type):

    df = pd.read_sql(
        COUNT_GRADES_BY_WALL.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df


def get_data_for_grades_by_hold_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)

    df = execute_query_on_df(
        COUNT_GRADES_BY_HOLD_FROM_DF.format(location_type=location_type), climbing_log_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df


def get_data_for_grades_by_hold_heatmap_from_postgres(location_type):

    df = pd_sql.read_sql(
        COUNT_GRADES_BY_HOLD_FROM_PG.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'
    
    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df


def get_data_for_grades_by_style_heatmap_from_csv(location_type):

    csv_path = f'data/climbing-log-{location_type}.csv'
    climbing_log_df = pd.read_csv(csv_path)

    df = execute_query_on_df(
        COUNT_GRADES_BY_STYLE.format(datasource='dataframe', location_type=location_type), climbing_log_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df


def get_data_for_grades_by_style_heatmap_from_postgres(location_type):
    
    df = pd.read_sql(
        COUNT_GRADES_BY_STYLE.format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[columns]  # sort columns

    return table_df, df
