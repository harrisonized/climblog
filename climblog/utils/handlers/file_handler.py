"""All functions related to reading files or directories
"""

import os
from os.path import abspath, dirname, sep
import json
import pandas as pd
import pandas.io.sql as pd_sql
from configparser import ConfigParser
from climblog.etc.connections import connection_uri, config_filepath
from .data_handler import execute_query_on_df, build_nested_dict, merge_dict_with_subdicts


# Functions
# # walk
# # read_section_from_ini
# # read_folder_as_dict
# # read_sql_or_csv
# # read_json


def walk(main_dir):
    """
    | Returns a list of files
    | Slightly faster than recursive_walk
    """
    files = []
    for root, dirs, filenames in os.walk(main_dir, topdown=False):
        files.extend([f'{root}{sep}{filename}' for filename in filenames])
    return files


def read_section_from_ini(section='default', cfg_path=config_filepath):
    """To be used with conf/settings.ini"""
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'

    return cfg[section]


def read_folder_as_dict(dirpath, ext='.sql'):
    """
    | Enter the path of a directory, the folders become keys, text files become values
    | Nested directories become nested keys
    """

    if dirpath[-1] == sep:
        dirpath = dirpath[:-1]

    files = [path.replace(f'{dirpath}{sep}', "") for path in walk(dirpath) if ext in path]

    text_dict = {}
    for file in sorted(files):

        # get new data
        keys = file.replace(ext, '').split(sep)
        # print(keys)
        with open(f"{dirpath}{sep}{file}") as f:
            val = f.read()
        sub_dict = build_nested_dict(keys, val)

        # add nested sub_dict to text_dict
        text_dict = merge_dict_with_subdicts(text_dict, sub_dict)

    return text_dict


def query_sql_or_csv(db_query,
                     df_query=None,
                     csv_filepath=None,
                     default_columns=None,
                     connection_uri=connection_uri):

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


def read_json(filepath, debug=False):
    """Retrieves figure from hardcoded path
    """
    if os.path.exists(filepath):
        with open(filepath) as f:
            fig = json.load(f)
        filename = os.path.basename(filepath)

        if debug:
            print(f'{filename} generated from tmp')

        return fig
