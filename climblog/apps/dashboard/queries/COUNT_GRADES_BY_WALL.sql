WITH primary_data AS
(SELECT
   date_,
   CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
        WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
        ELSE grade END AS grade_,
   grade AS vgrade,
   location,
   setter,
   description,
   LOWER(wall_type) AS wall_type,
   LOWER(hold_type) AS hold_type,
   LOWER(style) AS style
 FROM {datasource}
 WHERE location_type = '{location_type}'
 ORDER BY wall_type, grade_),

count_table AS
(SELECT
   grade_,
   wall_type,
   COUNT(wall_type) AS count_
 FROM primary_data
 GROUP BY grade_, wall_type),

first_send AS
(SELECT
   grade_,
   wall_type,
   MIN(date_) as date_
 FROM primary_data
 GROUP BY grade_, wall_type)

SELECT
  f.grade_,
  f.wall_type,
  c.count_,
  f.date_,
  p.location,
  p.setter,
  p.description,
  p.hold_type,
  p.style
FROM first_send f
LEFT JOIN count_table c ON f.grade_ = c.grade_ AND f.wall_type = c.wall_type
LEFT JOIN primary_data p ON f.date_ = p.date_ AND f.grade_ = p.grade_ AND f.wall_type = p.wall_type
ORDER BY f.date_, f.grade_, f.wall_type
;
