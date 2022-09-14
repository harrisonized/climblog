# function parameters

from climblog.etc.columns import (grades_by_wall_heatmap_columns,
                                  grades_by_hold_heatmap_columns,
                                  grades_by_style_heatmap_columns)

heatmap_params = {
    'grades_by_year':
        dict(filename='grades-by-year',
             xlabel='Year',
             db_query_name='COUNT_GRADES_BY_YEAR_FROM_PG',
             df_query_name='COUNT_GRADES_BY_YEAR_FROM_DF',
             columns=None,
        ),
    'grades_by_wall': 
        dict(filename='grades-by-wall-type',
             xlabel='Wall-type',
             db_query_name='COUNT_GRADES_BY_WALL',
             df_query_name='COUNT_GRADES_BY_WALL',
             columns=grades_by_wall_heatmap_columns,
        ),
    'grades_by_hold': 
        dict(filename='grades-by-hold-type',
             xlabel='Hold-type',
             db_query_name='COUNT_GRADES_BY_HOLD_FROM_PG',
             df_query_name='COUNT_GRADES_BY_HOLD_FROM_DF',
             columns=grades_by_hold_heatmap_columns,
        ),
    'grades_by_style': 
        dict(filename='grades-by-style',
             xlabel='Style',
             db_query_name='COUNT_GRADES_BY_STYLE',
             df_query_name='COUNT_GRADES_BY_STYLE',
             columns=grades_by_style_heatmap_columns,
        ),
}
