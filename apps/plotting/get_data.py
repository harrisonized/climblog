import pandasql as ps
from .queries import SCATTER, HISTOGRAM, YEAR, WALL, HOLD, STYLE


# Functions included in this file:
# # execute_query
# # get_scatter
# # get_histogram
# # get_year
# # get_wall
# # get_hold
# # get_style




def execute_query(query, dataframe, index_name=None, index_list=None, replace_grade=False):
    df = ps.sqldf(query, locals())

    # Replace grade
    if replace_grade is False:
        pass
    else:
        df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    # Set index column
    if index_name is None:
        pass
    else:
        df = df.set_index(index_name)

    # Reorder index column
    if index_list is None:
        pass
    else:
        df = df.reindex(index_list)

    return df


def get_scatter(climbing_log, color_dict, query=SCATTER):
    scatter_df = execute_query(query, climbing_log, replace_grade=True)
    scatter_df.color = scatter_df.color.replace(color_dict)  # Replace colors with hex codes
    return scatter_df


def get_histogram(climbing_log, color_dict, query=HISTOGRAM):
    df = execute_query(query, climbing_log, replace_grade=True)
    df.color = df.color.replace(color_dict)
    return df


def get_year(climbing_log, query=YEAR):
    df = execute_query(query, climbing_log, replace_grade=True)
    return df


def get_wall(climbing_log, query=WALL):
    df = execute_query(query, climbing_log, replace_grade=True)
    return df


def get_hold(climbing_log, query=HOLD):
    df = execute_query(query, climbing_log, replace_grade=True)
    return df


def get_style(climbing_log, query=STYLE):
    style_df = execute_query(query, climbing_log, replace_grade=True)
    return style_df
