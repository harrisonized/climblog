-- sqlite

WITH primary_data AS
(SELECT 
   date_,
   grade,
   display_grade,
   location,
   setter,
   description,
   LOWER(wall_type) AS wall_type,
   LOWER(hold_type) AS hold_type,
   LOWER(style) AS style,
   strftime("%Y", date_) AS year  --sqlite only
 FROM dataframe
 WHERE location_type = '{location_type}'
 ORDER BY date_),

count_table AS
(SELECT
   grade,
   year,
   COUNT(year) AS count_
 FROM primary_data
 GROUP BY grade, year),

first_send AS
(SELECT 
   grade,
   year,
   MIN(date_) as date_
 FROM primary_data
 GROUP BY grade, year)

SELECT
  f.grade,
  f.year,
  c.count_,
  f.date_,
  p.display_grade,
  p.location,
  p.setter,
  p.description, 
  p.wall_type,
  p.hold_type,
  p.style
FROM first_send f
LEFT JOIN count_table c ON f.grade = c.grade and f.year = c.year
LEFT JOIN primary_data p ON f.date_ = p.date_ AND f.grade = p.grade AND f.year = p.year
ORDER BY f.date_, f.grade, f.year
;
