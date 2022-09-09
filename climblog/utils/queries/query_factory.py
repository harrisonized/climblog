"""imports queries from the queries folder

Example:
>>> from climblog.queries import queries
"""
from os.path import abspath, sep
from climblog.utils.file_handler import dirname_n_times, read_folder_as_dict

ROOT_DIR = dirname_n_times(abspath(__file__), 4)

# load queries
query_dict = read_folder_as_dict(
    dirpath=f"{ROOT_DIR}{sep}queries{sep}",
    ext='.sql',
)

# add queries to the namespace
for subdir, query_subdict in query_dict.items():
    globals()[subdir] = query_subdict
