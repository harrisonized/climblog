import os
import pandas as pd
import psycopg2 as pg
from configparser import ConfigParser
from .encryption_tools import decrypt_message

INI_KEY = os.getenv('INI_KEY')  # Make sure this is in your ~/.bashrc
assert INI_KEY, 'No INI_KEY'

# Functions included in this file:
# # postgres_connection
# # heroku_postgres_connection
# # postgres_connect_fetch_close


def postgres_connection(database=None,
                        section='postgres', cfg_path='configs/cred.ini'):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    username, password, host, port = (
        decrypt_message(cfg.get(section, key), INI_KEY)
        for key in ['username', 'password', 'host', 'port']
    )

    if database:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'
    else:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}'

    return connection_uri


def heroku_postgres_connection(section='heroku-postgres', cfg_path='configs/cred.ini'):
    """Given an INI file with a ['heroku-postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port', 'db_name']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    username, password, host, port, database = (
        decrypt_message(cfg.get(section, key), INI_KEY)
        for key in ['username', 'password', 'host', 'port', 'db_name']
    )

    connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'

    return connection_uri



def postgres_connect_fetch_close(query,
                                 connection_uri=None,
                                 dbname=None,
                                 read_only=True
                                 ):
    """Opens a new connection, fetches the data, then closes the connection
    Provide the connection_uri returned by postgres_connection
    Use dbname to change the database
    """
    if not connection_uri:
    	connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')  # test locally

    connection = pg.connect(dsn=connection_uri, dbname=dbname)  # connect
    connection.set_session(readonly=read_only)
    cursor = connection.cursor()
    cursor.execute(query)

    cols = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=cols)

    connection.close()

    return df
