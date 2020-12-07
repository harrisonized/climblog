import os
import pandas as pd
import psycopg2 as pg
from apps.utils.auth.connections import postgres_connection

connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')  # test locally


# Functions included in this file:
# # postgres_connect_fetch_close


def postgres_connect_fetch_close(query,
                                 connection_uri=connection_uri,
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
