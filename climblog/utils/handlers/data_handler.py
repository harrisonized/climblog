import os
from os.path import dirname
import collections
import pandas as pd
import pandasql as ps

# Functions
# # dirname_n_times
# # append_standard_df
# # execute_query_on_df
# # word_wrap
# # build_nested_dict
# # merge_dict_with_subdicts


def dirname_n_times(path, n=1):
    for i in range(n):
        path = dirname(path)
    return path


def append_standard_df(df, columns):
    """Forces a df to have the select_columns
    If it doesn't fills a column of NA's
    """
    empty_df = pd.DataFrame(columns=columns)
    df = empty_df.append(df)
    return df[columns]


def execute_query_on_df(query, dataframe,
                        index_name=None, index_list=None):
    """Convenience function
    """
    df = ps.sqldf(query, locals())

    # Set index column
    if index_name:
        df = df.set_index(index_name)

    # Reorder index column
    if index_list:
        df = df.reindex(index_list)

    return df


def word_wrap(string, n):
    string_list = string.split()
    parsed_list = [string_list[n * i:n * (i + 1)] for i in range((len(string_list) + n - 1) // n)]
    joined_string_list = [' '.join(parsed_list[i]) for i in range(len(parsed_list))]
    final_list = ['<br>'.join(joined_string_list)]
    return final_list[0]


def build_nested_dict(keys: list, val):
    """
    | Iterative solution to building a nested dictionary from inside out
    | See: https://stackoverflow.com/questions/40401886/how-to-create-a-nested-dictionary-from-a-list-in-python
    
    .. code-block:: python
    
       >>> build_nested_dict(['grandparents', 'parents'], 'children')
       {'grandparents': {'parents': 'children'}}
       
    """
    nested_dict = {}
    nested_dict[keys[-1]] = val
    for key in reversed(keys[0:-1]):
        nested_dict = {key: nested_dict}

    return nested_dict


def merge_dict_with_subdicts(main_dict: dict, sub_dict: dict) -> dict:
    """
    | Merge two nested dictionaries
    | See: https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries
    """
    queue = collections.deque([(main_dict, sub_dict)])

    while len(queue) > 0:
        d1, d2 = queue.pop()
        for key, val in d2.items():
            if key in d1 and isinstance(d1[key], dict) and isinstance(val, dict):
                queue.append((d1[key], val))
            else:
                d1[key] = val

    return main_dict
