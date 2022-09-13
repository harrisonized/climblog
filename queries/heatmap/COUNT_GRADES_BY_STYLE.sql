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
   style,
   COUNT(style) AS count_
 FROM primary_data
 GROUP BY grade, style),

first_send AS
(SELECT
   grade,
   style,
   MIN(date_) as date_
 FROM primary_data
 GROUP BY grade, style)

SELECT
  f.grade,
  f.style,
  c.count_,
  f.date_,
  p.display_grade,
  p.location,
  p.setter,
  p.description,
  p.wall_type,
  p.hold_type
FROM first_send f
LEFT JOIN count_table c ON f.grade = c.grade AND f.style = c.style
LEFT JOIN primary_data p ON f.date_ = p.date_ AND f.grade = p.grade AND f.style = p.style
ORDER BY f.date_, f.grade, f.style
;
