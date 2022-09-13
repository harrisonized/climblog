import os
import datetime as dt
import pandas as pd
import pandas.io.sql as pd_sql
from climblog.utils.auth.connections import postgres_connection
from climblog.utils.handlers.data_handler import execute_query_on_df
from climblog.etc.colors import color_name_to_hex, color_grade_to_name
from climblog.etc.columns import default_columns
from climblog.factories import queries

connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')  # test locally
data_dir = 'data'


# Functions included in this file:
# # get_data_for_sends_by_date_scatter
# # get_data_for_grades_histogram
# # get_data_for_grades_by_heatmap


def get_data_for_sends_by_date_scatter(location_type, is_tmp=False):

    try:
        df = pd_sql.read_sql(
            queries['GET_PRIMARY_DATA'].format(datasource='boulders', location_type=location_type), connection_uri)
        assert df.empty is False, 'No data returned'

    except:
        csv_path = f'{data_dir}/climbing-log.csv'

        if is_tmp:
            csv_path = f'tmp/{csv_path}'

        try:
            df = pd.read_csv(csv_path)
        except:
            df = pd.DataFrame(columns=default_columns)

        df = df[(df['location_type'] == location_type)].copy()

    df['date_'] = df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))
    df.loc[df['color'].isna(), 'color'] = df.loc[df['color'].isna(), 'grade'].replace(color_grade_to_name)  # add a color if null
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes
    
    return df


def get_data_for_grades_histogram(location_type, is_tmp=False):

    try:
        df = pd_sql.read_sql(
            queries['histogram']['COUNT_GRADES'].format(datasource='boulders', location_type=location_type), connection_uri)
        assert df.empty is False, 'No data returned'

    except:
        csv_path = f'{data_dir}/climbing-log.csv'

        if is_tmp:
            csv_path = f'tmp/{csv_path}'

        try:
            raw_df = pd.read_csv(csv_path)
        except:
            raw_df = pd.DataFrame(columns=default_columns)
        
        df = execute_query_on_df(
            queries['histogram']['COUNT_GRADES'].format(datasource='dataframe', location_type=location_type),
            raw_df
        )

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    df.loc[df['color'].isna(), 'color'] = df.loc[df['color'].isna(), 'grade'].replace(color_grade_to_name)
    df['color'] = df['color'].replace(color_name_to_hex)

    return df


def get_data_for_grades_by_heatmap(location_type,
                                   query_pg,
                                   query_df,
                                   columns=None,
                                   query_dir='heatmap',
                                   is_tmp=False):

    try:
        df = pd_sql.read_sql(
            queries[query_dir][query_pg].format(datasource='boulders', location_type=location_type), connection_uri)
        assert df.empty is False, 'No data returned'        

    except:
        csv_path = f'{data_dir}/climbing-log.csv'

        if is_tmp:
            csv_path = f'tmp/{csv_path}'

        try:
            raw_df = pd.read_csv(csv_path)
        except:
            raw_df = pd.DataFrame(columns=default_columns)

        df = execute_query_on_df(
            queries[query_dir][query_df].format(datasource='dataframe', location_type=location_type),
            raw_df
        )

    df = df.drop_duplicates(subset=[df.columns[0], df.columns[1]])
    # df['grade'] = df['grade'].apply(lambda x: x.replace('V', '')).astype(int)
    table_df = df.reset_index().pivot(index=df.columns[0], columns=df.columns[1], values="count_").fillna(0)
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

    if columns is not None:
        table_df = table_df[[column for column in columns if column in table_df.columns]]  # sort columns

    return table_df, df
