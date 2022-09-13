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
   LOWER(style) AS style
 FROM {datasource}
 WHERE location_type = '{location_type}'
 ORDER BY wall_type, grade),

count_table AS
(SELECT
   grade,
   wall_type,
   COUNT(wall_type) AS count_
 FROM primary_data
 GROUP BY grade, wall_type),

first_send AS
(SELECT
   grade,
   wall_type,
   MIN(date_) as date_
 FROM primary_data
 GROUP BY grade, wall_type)

SELECT
  f.grade,
  f.wall_type,
  c.count_,
  f.date_,
  p.location,
  p.setter,
  p.description,
  p.hold_type,
  p.style
FROM first_send f
LEFT JOIN count_table c ON f.grade = c.grade AND f.wall_type = c.wall_type
LEFT JOIN primary_data p ON f.date_ = p.date_ AND f.grade = p.grade AND f.wall_type = p.wall_type
ORDER BY f.date_, f.grade, f.wall_type
;
