"""
Note this file contains _NO_ flask functionality.
Instead, it isolates all the SQL commands and table joins so that main.py has less clutter.
"""
import pandas as pd
import pandas.io.sql as pd_sql
import pandasql as ps



"""
General Functions
"""

def execute_query(query, dataframe, index_name=None, index_list=None, replace_grade=False):
    df = ps.sqldf(query, locals())
    
    # Replace grade
    if replace_grade == False:
        pass
    else:
        df['grade_'] = df['grade_'].apply(lambda x: x.replace('V', '')).astype(int)
    
    # Set index column
    if index_name == None:
        pass
    else:
        df = df.set_index(index_name)
    
    # Reorder index column
    if index_list == None:
        pass
    else:
        df = df.reindex(index_list)
    
    return df



"""
Sends by Date Scatter
"""

def get_new_grades(climbing_log, color_dict):
    query = """
    WITH all_records AS
    (SELECT date_,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      color
    FROM dataframe
    ORDER BY date_)

    SELECT date_, grade_, color
    FROM all_records
    GROUP BY grade_
    HAVING MIN(date_)
    ORDER BY date_
    ;
    """
    df = execute_query(query, climbing_log, replace_grade=True)
    df.color = df.color.replace(color_dict) # Replace colors with hex codes
    return df

def get_hist(climbing_log, color_dict):
    query = """
    WITH count_table AS
    (SELECT CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      COUNT(strftime("%Y", date_)) AS count_
    FROM dataframe
    GROUP BY grade_
    ORDER BY grade_),

    hover_info AS
    (SELECT CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      date_,
      grade,
      location,
      setter,
      wall_type,
      hold_type,
      style,
      description,
      color
    FROM dataframe
    GROUP BY grade_
    HAVING MIN(date_)
    ORDER BY date_)

    SELECT c.grade_, c.count_,
      h.date_,
      h.grade,
      h.location,
      h.setter,
      h.wall_type,
      h.hold_type,
      h.style,
      h.description,
      color
    FROM count_table c
    LEFT JOIN hover_info h
    ON c.grade_=h.grade_
    ORDER BY h.date_
    ;
    """
    df = execute_query(query, climbing_log, replace_grade=True)
    df.color = df.color.replace(color_dict)
    return df

def get_scatter(climbing_log, color_dict):
    query = """
    SELECT date_,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      color,
      location,
      setter,
      description,
      grade AS vgrade,
      wall_type,
      hold_type,
      style
    FROM dataframe;
    """
    scatter_df = execute_query(query, climbing_log, replace_grade=True)
    scatter_df.color = scatter_df.color.replace(color_dict) # Replace colors with hex codes
    return scatter_df



"""
Heatmaps
"""

def get_year(climbing_log):
    query =  """
    WITH count_table AS
    (SELECT strftime("%Y", date_) AS year,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      COUNT(strftime("%Y", date_)) AS count_
    FROM dataframe
    GROUP BY year, grade_
    ORDER BY year, grade_),

    filter_table AS
    (SELECT strftime("%Y", date_) AS year,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      date_,
      location,
      setter,
      description,
      grade AS vgrade,
      wall_type,
      hold_type,
      style
    FROM dataframe
    ORDER BY year, grade_),

    hover_info AS
    (SELECT year, grade_,
      date_,
      location,
      setter,
      description,
      wall_type,
      hold_type,
      style
    FROM filter_table
    GROUP BY year, grade_
    HAVING MIN(year)
    ORDER BY year)

    SELECT c.year, c.grade_, c.count_,
      h.date_,
      h.location,
      h.setter,
      h.description,
      h.wall_type,
      h.hold_type,
      h.style
    FROM count_table c
    LEFT JOIN hover_info h
    ON c.grade_=h.grade_ AND c.year=h.year
    ;
    """
    df = execute_query(query, climbing_log, replace_grade=True)
    return df

def get_wall(climbing_log):
    query = """
    WITH count_table AS
    (SELECT wall_type, 
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      COUNT(wall_type) AS count_
    FROM dataframe
    GROUP BY wall_type, grade_
    ORDER BY count_ DESC),

    filter_table AS
    (SELECT wall_type,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      date_,
      location,
      setter,
      description,
      grade AS vgrade,
      wall_type,
      hold_type,
      style
    FROM dataframe
    ORDER BY wall_type, grade_),

    hover_info AS
    (SELECT wall_type, grade_,
      date_,
      location,
      setter,
      description,
      hold_type,
      style
    FROM filter_table
    GROUP BY wall_type, grade_
    HAVING MIN(date_)
    ORDER BY date_)

    SELECT c.wall_type, c.grade_, c.count_,
      h.date_,
      h.location,
      h.setter,
      h.description,
      h.hold_type,
      h.style
    FROM count_table c
    LEFT JOIN hover_info h
    ON c.wall_type=h.wall_type AND c.grade_=h.grade_
    ;
    """
    df = execute_query(query, climbing_log, replace_grade=True)
    return df

def get_hold(climbing_log):
    query = """
    WITH unnested_hold_table AS
    (WITH RECURSIVE SPLIT(date_,
      grade,
      location,
      setter,
      wall_type,
      style,
      description,
      sep_hold_type,
      rest) AS
    
    (SELECT date_,
      grade,
      location,
      setter,
      wall_type,
      style,
      description, '', hold_type || ','
      FROM dataframe
      WHERE date_
      UNION ALL
      SELECT date_, grade, location, setter, wall_type, style, description,
        TRIM(SUBSTR(rest, 0, INSTR(rest, ','))),
        TRIM(SUBSTR(rest, INSTR(rest, ',')+1))
      FROM split
      WHERE rest <> '')

    SELECT date_,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade,
      location,
      setter,
      wall_type,
      style,
      description,
      sep_hold_type
    FROM split 
    WHERE sep_hold_type <> ''
    ORDER BY date_, sep_hold_type),
    
    count_table AS
    (SELECT sep_hold_type AS hold_type,
        grade AS grade_,
        COUNT(sep_hold_type) AS count_
    FROM unnested_hold_table
    GROUP BY sep_hold_type, grade
    ORDER BY count_ DESC),
    
    filter_table AS
    (SELECT sep_hold_type AS hold_type,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      date_,
      location,
      setter,
      description,
      grade AS vgrade,
      wall_type,
      style
    FROM unnested_hold_table
    ORDER BY sep_hold_type, grade_),
    
    hover_info AS
    (SELECT hold_type, grade_,
      date_,
      location,
      setter,
      description,
      style,
      wall_type
    FROM filter_table
    GROUP BY hold_type, grade_
    HAVING MIN(date_)
    ORDER BY date_)
    
    SELECT c.hold_type AS hold_type, c.grade_, c.count_,
      h.date_,
      h.location,
      h.setter,
      h.description,
      h.wall_type,
      h.style
    FROM count_table c
    LEFT JOIN hover_info h
    ON c.hold_type=h.hold_type AND c.grade_=h.grade_    
    ;
    """
    df = execute_query(query, climbing_log, replace_grade=True)
    return df

def get_style(climbing_log):
    query = """
    WITH count_table AS
    (SELECT style, 
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      COUNT(style) AS count_
    FROM dataframe
    GROUP BY style, grade_
    ORDER BY count_ DESC),

    filter_table AS
    (SELECT style,
      CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
      WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
      ELSE grade END AS grade_,
      date_,
      location,
      setter,
      description,
      grade AS vgrade,
      wall_type,
      hold_type
    FROM dataframe
    ORDER BY wall_type, grade_),

    hover_info AS
    (SELECT style, grade_,
      date_,
      location,
      setter,
      description,
      hold_type,
      wall_type
    FROM filter_table
    GROUP BY style, grade_
    HAVING MIN(date_)
    ORDER BY date_)

    SELECT c.style, c.grade_, c.count_,
      h.date_,
      h.location,
      h.setter,
      h.description,
      h.hold_type,
      h.wall_type
    FROM count_table c
    LEFT JOIN hover_info h
    ON c.style=h.style AND c.grade_=h.grade_
    ;
    """
    style_df = execute_query(query, climbing_log, replace_grade=True)
    return style_df



# This section checks that the prediction code runs properly
# To test, use "python predictor_api.py" in the terminal.

# if __name__='__main__' section only runs
# when running this file; it doesn't run when importing

if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what empty string predicts")
    print('input string is ')
    chat_in = 'bob'
    pprint(chat_in)

    x_input, probs = make_prediction(chat_in)
    print(f'Input values: {x_input}')
    print('Output probabilities')
    pprint(probs)