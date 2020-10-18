import os

real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)


# Queries included in this file:
# GET_PRIMARY_DATA
# COUNT_GRADES
# COUNT_GRADES_BY_YEAR_FROM_DF
# COUNT_GRADES_BY_YEAR_FROM_PG
# COUNT_GRADES_BY_WALL
# COUNT_GRADES_BY_HOLD_FROM_DF
# COUNT_GRADES_BY_HOLD_FROM_PG
# COUNT_GRADES_BY_STYLE


with open(f'{dir_name}/queries/GET_PRIMARY_DATA.sql') as f:
    GET_PRIMARY_DATA = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES.sql') as f:
    COUNT_GRADES = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_YEAR_FROM_DF.sql') as f:
    COUNT_GRADES_BY_YEAR_FROM_DF = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_YEAR_FROM_PG.sql') as f:
    COUNT_GRADES_BY_YEAR_FROM_PG = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_WALL.sql') as f:
    COUNT_GRADES_BY_WALL = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_HOLD_FROM_DF.sql') as f:
    COUNT_GRADES_BY_HOLD_FROM_DF = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_HOLD_FROM_PG.sql') as f:
    COUNT_GRADES_BY_HOLD_FROM_PG = f.read()

with open(f'{dir_name}/queries/COUNT_GRADES_BY_STYLE.sql') as f:
    COUNT_GRADES_BY_STYLE = f.read()
