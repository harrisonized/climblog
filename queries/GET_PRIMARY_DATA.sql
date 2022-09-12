SELECT
  date_,
  CASE WHEN grade IN ('V6-V7', 'V6') THEN 'V6' 
       WHEN grade IN ('V7-V8', 'V7') THEN 'V7'
       ELSE grade END
       AS grade_,
  grade AS vgrade,
  location,
  setter,
  description,
  LOWER(wall_type) AS wall_type,
  LOWER(hold_type) AS hold_type,
  LOWER(style) AS style,
  LOWER(color) AS color
FROM {datasource}
WHERE location_type = '{location_type}'
ORDER BY date_, grade_
;
