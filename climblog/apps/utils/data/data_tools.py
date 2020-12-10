import pandas as pd


# Objects included in this file:
# # default_columns

# Functions included in this file:
# # append_standard_df


default_columns = ["date_",
                   "color",
                   "description",
                   "hold_type",
                   "wall_type",
                   "style",
                   "grade",
                   "setter",
                   "location",
                   "location_type"
                   ]


def append_standard_df(df, columns=default_columns):
    """Forces a df to have the select_columns
    If it doesn't fills a column of NA's
    """
    empty_df = pd.DataFrame(columns=columns)
    df = empty_df.append(df)
    return df[columns]
