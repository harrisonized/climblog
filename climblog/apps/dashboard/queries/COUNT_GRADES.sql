WITH primary_data AS
(SELECT
   date_,
   CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
        WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
        ELSE grade END
        AS grade_,
   grade,
   location,
   setter,
   description,
   LOWER(wall_type) AS wall_type,
   LOWER(hold_type) AS hold_type,
   LOWER(style) AS style,
   LOWER(color) AS color
 FROM {datasource}
 WHERE location_type = '{location_type}'),

count_table AS
(SELECT grade_,
        COUNT(date_) AS count_
 FROM primary_data
 GROUP BY grade_),

first_send AS
(SELECT grade_,
        MIN(date_) as date_
 FROM primary_data
 GROUP BY grade_)

SELECT
  c.grade_,
  c.count_,
  f.date_,
  p.grade,
  p.location,
  p.setter,
  p.wall_type,
  p.hold_type,
  p.style,
  p.description,
  p.color
FROM count_table c
LEFT JOIN first_send f ON c.grade_ = f.grade_
LEFT JOIN primary_data p ON c.grade_ = p.grade_ AND f.date_ = p.date_
ORDER BY f.date_
;
