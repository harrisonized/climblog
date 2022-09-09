import os
import datetime as dt
import pandas as pd
import pandas.io.sql as pd_sql
from climblog.etc.columns import default_columns
from climblog.utils.auth.connections import postgres_connection
from climblog.utils.data_handler import execute_query_on_df
from climblog.etc.colors import color_name_to_hex, color_grade_to_name
from climblog.utils.queries import queries

connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')  # test locally
data_dir = 'data'


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


def get_data_for_sends_by_date_scatter_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        df = pd.read_csv(csv_path)
    except:
        df = pd.DataFrame(columns=default_columns)

    df['location_type'] = location_type
    df = df.rename(columns={'grade': 'vgrade'})

    df['grade_'] = df['vgrade'].apply(lambda x: x.split('-')[0]).apply(lambda x: x.replace('V', '')).astype(int)
    df['date_'] = df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))
    
    df.loc[df['color'].isna(), ['color']] = df.loc[df['color'].isna()]['grade_'].replace(color_grade_to_name)  # add a color if null
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes
    
    return df


def get_data_for_sends_by_date_scatter_from_postgres(location_type):
    df = pd_sql.read_sql(
        queries['GET_PRIMARY_DATA'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    df['date_'] = df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))  # Convert to datetime
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes

    return df


def get_data_for_grades_histogram_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        raw_df = pd.read_csv(csv_path)
    except:
        raw_df = pd.DataFrame(columns=default_columns)
    
    raw_df['location_type'] = location_type

    df = execute_query_on_df(
        queries['COUNT_GRADES'].format(datasource='dataframe', location_type=location_type), raw_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
   
    df.loc[df['color'].isna(), ['color']] = df.loc[df['color'].isna()]['grade_'].replace(color_grade_to_name)
    df['color'] = df['color'].replace(color_name_to_hex)

    return df


def get_data_for_grades_histogram_from_postgres(location_type):
    df = pd_sql.read_sql(
        queries['COUNT_GRADES'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes

    return df


def get_data_for_grades_by_year_heatmap_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        raw_df = pd.read_csv(csv_path)
    except:
        raw_df = pd.DataFrame(columns=default_columns)

    raw_df['location_type'] = location_type

    df = execute_query_on_df(
        queries['COUNT_GRADES_BY_YEAR_FROM_DF'].format(location_type=location_type), raw_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = df.reset_index().pivot(index=df.columns[0],
                                      columns=df.columns[1],
                                      values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, df


def get_data_for_grades_by_year_heatmap_from_postgres(location_type):
    df = pd_sql.read_sql(
        queries['COUNT_GRADES_BY_YEAR_FROM_PG'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    return table_df, df


def get_data_for_grades_by_wall_heatmap_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        raw_df = pd.read_csv(csv_path)
    except:
        raw_df = pd.DataFrame(columns=default_columns)

    raw_df['location_type'] = location_type

    df = execute_query_on_df(
        queries['COUNT_GRADES_BY_WALL'].format(datasource='dataframe', location_type=location_type), raw_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df


def get_data_for_grades_by_wall_heatmap_from_postgres(location_type):
    df = pd.read_sql(
        queries['COUNT_GRADES_BY_WALL'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df


def get_data_for_grades_by_hold_heatmap_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        raw_df = pd.read_csv(csv_path)
    except:
        raw_df = pd.DataFrame(columns=default_columns)

    raw_df['location_type'] = location_type

    df = execute_query_on_df(
        queries['COUNT_GRADES_BY_HOLD_FROM_DF'].format(location_type=location_type), raw_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df


def get_data_for_grades_by_hold_heatmap_from_postgres(location_type):
    df = pd_sql.read_sql(
        queries['COUNT_GRADES_BY_HOLD_FROM_PG'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['jug', 'crimp', 'sloper', 'pinch']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df


def get_data_for_grades_by_style_heatmap_from_csv(location_type, is_tmp=False):
    csv_path = f'{data_dir}/climbing-log-{location_type}.csv'

    if is_tmp:
        csv_path = f'tmp/{csv_path}'

    try:
        raw_df = pd.read_csv(csv_path)
    except:
        raw_df = pd.DataFrame(columns=default_columns)

    raw_df['location_type'] = location_type

    df = execute_query_on_df(
        queries['COUNT_GRADES_BY_STYLE'].format(datasource='dataframe', location_type=location_type), raw_df)

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df


def get_data_for_grades_by_style_heatmap_from_postgres(location_type):
    df = pd.read_sql(
        queries['COUNT_GRADES_BY_STYLE'].format(datasource='boulders', location_type=location_type), connection_uri)
    assert df.empty is False, 'No data returned'

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    columns = ['mantle', 'natural', 'dyno', 'comp']
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df
