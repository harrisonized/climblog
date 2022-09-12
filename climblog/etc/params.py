from climblog.etc.columns import (grades_by_wall_heatmap_columns,
                                  grades_by_hold_heatmap_columns,
                                  grades_by_style_heatmap_columns)

heatmap_params = {
    'grades_by_year':
        dict(filename='grades-by-year',
             xlabel='Year',
             query_pg='COUNT_GRADES_BY_YEAR_FROM_PG',
             query_df='COUNT_GRADES_BY_YEAR_FROM_DF',
             columns=None,
        ),
    'grades_by_wall': 
        dict(filename='grades-by-wall-type',
             xlabel='Wall-type',
             query_pg='COUNT_GRADES_BY_WALL',
             query_df='COUNT_GRADES_BY_WALL',
             columns=grades_by_wall_heatmap_columns,
        ),
    'grades_by_hold': 
        dict(filename='grades-by-hold-type',
             xlabel='Hold-type',
             query_pg='COUNT_GRADES_BY_HOLD_FROM_PG',
             query_df='COUNT_GRADES_BY_HOLD_FROM_DF',
             columns=grades_by_hold_heatmap_columns,
        ),
    'grades_by_style': 
        dict(filename='grades-by-style',
             xlabel='Style',
             query_pg='COUNT_GRADES_BY_STYLE',
             query_df='COUNT_GRADES_BY_STYLE',
             columns=grades_by_style_heatmap_columns,
        ),
}
