WITH primary_data AS
(SELECT
   index_,
   date_,
   grade,
   display_grade,
   location,
   setter,
   description,
   LOWER(wall_type) AS wall_type,
   LOWER(hold_type) AS hold_type,
   LOWER(style) AS style,
   LOWER(color) AS color
 FROM {datasource}
 WHERE location_type = '{location_type}'
 ),
 
 first_table AS (
 SELECT grade,
    MIN(index_) AS first_index,
    COUNT(*) AS count_
FROM primary_data
GROUP BY grade)

SELECT
  f.first_index,
  f.count_,
  p.date_,
  p.grade,
  p.display_grade,
  p.location,
  p.setter,
  p.wall_type,
  p.hold_type,
  p.style,
  p.description,
  p.color
FROM first_table f
LEFT JOIN primary_data p ON f.first_index = p.index_
ORDER BY p.date_
;
