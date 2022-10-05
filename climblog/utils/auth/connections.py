"""Process ini files and postgres
"""

import os
import pandas as pd
import pandas.io.sql as pd_sql
import psycopg2 as pg
from ..handlers.data_handler import execute_query_on_df
from ...etc.paths import postgres_connection_uri


# Functions
# # postgres_connect_fetch_close
# # query_sql_or_csv

def postgres_connect_fetch_close(query,
                                 connection_uri=os.getenv('DATABASE_URL') or postgres_connection_uri,
                                 dbname=None,
                                 read_only=True
                                 ):
    """Opens a new connection, fetches the data, then closes the connection
    Provide the connection_uri returned by postgres_connection
    Use dbname to change the database
    """
    connection = pg.connect(dsn=connection_uri, dbname=dbname)  # connect
    connection.set_session(readonly=read_only)

    cursor = connection.cursor()
    cursor.execute(query)

    cols = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=cols)

    connection.close()

    return df


def query_sql_or_csv(db_query,
                     df_query=None,
                     csv_filepath=None,
                     default_columns=None,
                     connection_uri=None):
    """Swtich case to get data from database or csv
    """

    try:
        df = pd_sql.read_sql(db_query, connection_uri)
        assert df.empty is False, 'No data returned'

    except:
        try:
            df = pd.read_csv(csv_filepath)
        except:
            df = pd.DataFrame(columns=default_columns)  # empty data

        if df_query:
            df = execute_query_on_df(df_query, df)

    return df
