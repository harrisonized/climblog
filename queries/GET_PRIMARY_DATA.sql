SELECT
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
ORDER BY date_
;
