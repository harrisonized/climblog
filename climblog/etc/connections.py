import os
from os.path import abspath
from climblog.utils.handlers.data_handler import dirname_n_times
from climblog.utils.auth.connections import postgres_connection

ROOT_DIR = dirname_n_times((abspath(__file__)), 3)

connection_uri = os.getenv('DATABASE_URL') or postgres_connection('climblog')
config_filepath = f'{ROOT_DIR}/configs/settings.ini'
