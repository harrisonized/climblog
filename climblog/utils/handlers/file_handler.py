"""All functions related to reading files or directories
"""

import os
from os.path import sep
from collections import defaultdict
import json
from configparser import ConfigParser
from .data_handler import build_nested_dict, merge_dict_with_subdicts
from ..auth.encryption_tools import decrypt_message


# Functions
# # walk
# # read_folder_as_dict
# # read_json
# # read_section_from_ini
# # read_ini_as_dict
# # connection_uri_from_ini


def walk(main_dir):
    """
    | Returns a list of files
    | Slightly faster than recursive_walk
    """
    files = []
    for root, dirs, filenames in os.walk(main_dir, topdown=False):
        files.extend([f'{root}{sep}{filename}' for filename in filenames])
    return files


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


def read_section_from_ini(filepath, section='default'):
    """To be used with conf/settings.ini"""
    assert os.path.exists(filepath), f'Missing file at {filepath}'
    
    cfg = ConfigParser()
    cfg.read(filepath)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'

    return cfg[section]


def read_ini_as_dict(filepath, ini_key=None, sections=[]):
    
    assert os.path.exists(filepath), f'Missing file at {filepath}'
    
    config_parser = ConfigParser()
    config_parser.read(filepath)
    all_sections = config_parser.sections()
    
    if not sections:
        sections = all_sections
    else:
        sections = [section for section in sections if section in all_sections]

    ini_dict = defaultdict(dict)
    for section in sections:
        for key in config_parser[section]:
            val = config_parser[section][key]
            if ini_key:
                val = decrypt_message(val, ini_key)
            ini_dict[section][key] = val

    return ini_dict


def connection_uri_from_ini(
        filepath,
        section='postgres',  # or 'heroku-postgres'
        ini_key=None,  # enter if encrypted, otherwise leave blank
        
        # overwrite the original file
        username=None,
        password=None,
        host=None,
        port=None,
        db_name=None,
    ):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    if db_name:
        orig_db_name = db_name

    ini_dict = read_ini_as_dict(filepath, ini_key, sections=[section]).get(section, {})

    # get fields
    if not username:
        username = ini_dict.get('username')
    if not password:
        password = ini_dict.get('password')
    if not host:
        host = ini_dict.get('host')
    if not port:
        port = ini_dict.get('port')
    if not db_name:
        db_name = ini_dict.get('db_name')
    
    if db_name:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}/{db_name}'
    else:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}'

    return connection_uri
