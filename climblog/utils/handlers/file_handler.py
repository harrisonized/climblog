import os
from os.path import abspath, dirname, sep
from configparser import ConfigParser
from .data_handler import build_nested_dict, merge_dict_with_subdicts

ROOT_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))

# Functions
# # walk
# # dirname_n_times
# # read_folder_as_dict
# # get_defaults_from_ini


def walk(main_dir):
    """
    | Returns a list of files
    | Slightly faster than recursive_walk
    """
    files = []
    for root, dirs, filenames in os.walk(main_dir, topdown=False):
        files.extend([f'{root}{sep}{filename}' for filename in filenames])
    return files


def dirname_n_times(path, n=1):

    for i in range(n):
        path = dirname(path)
    return path


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


def get_defaults_from_ini(section='default', cfg_path=f'{ROOT_DIR}/configs/settings.ini'):
    """To be used with conf/settings.ini"""
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'

    return cfg[section]
