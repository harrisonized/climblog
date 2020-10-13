import pandasql as ps

# Functions included in this file:
# # execute_query_on_df

def execute_query_on_df(query, dataframe,
                        index_name=None, index_list=None,
                        replace_grade=True):
    df = ps.sqldf(query, locals())

    # Replace grade
    if replace_grade:
        df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)

    # Set index column
    if index_name:
        df = df.set_index(index_name)

    # Reorder index column
    if index_list:
        df = df.reindex(index_list)

    return df
