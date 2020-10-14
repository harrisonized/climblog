import os

real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)


# Queries included in this file:
# SENDS_BY_DATE
# GRADES_HISTOGRAM
# GRADES_BY_YEAR
# GRADES_BY_WALL
# GRADES_BY_HOLD
# GRADES_BY_STYLE


with open(f'{dir_name}/queries/SENDS_BY_DATE.txt') as f:
    SENDS_BY_DATE = f.read()

with open(f'{dir_name}/queries/GRADES_HISTOGRAM.txt') as f:
    GRADES_HISTOGRAM = f.read()

with open(f'{dir_name}/queries/GRADES_BY_YEAR.txt') as f:
    GRADES_BY_YEAR = f.read()

with open(f'{dir_name}/queries/GRADES_BY_WALL.txt') as f:
    GRADES_BY_WALL = f.read()

with open(f'{dir_name}/queries/GRADES_BY_HOLD.txt') as f:
    GRADES_BY_HOLD = f.read()

with open(f'{dir_name}/queries/GRADES_BY_STYLE.txt') as f:
    GRADES_BY_STYLE = f.read()
