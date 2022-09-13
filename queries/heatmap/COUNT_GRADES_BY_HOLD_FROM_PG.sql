-- postgresql

WITH primary_data AS
(SELECT
   date_,
   grade
   display_grade,
   location,
   setter,
   description,
   LOWER(wall_type) AS wall_type,
   LOWER(style) AS style,
   LOWER(hold_type) AS hold_type
 FROM {datasource}
 WHERE location_type = '{location_type}'),

unnested_primary_data AS
(WITH RECURSIVE SPLIT(date_, grade, display_grade, location, setter, description, wall_type, style,
                      sep_hold_type, rest) AS

   (SELECT date_, grade, display_grade, location, setter, description, wall_type, style, 
      '',
      hold_type || ','
    FROM primary_data
       
    UNION ALL
  
    SELECT date_, grade, display_grade, location, setter, description, wall_type, style, 
      TRIM(SUBSTR(rest, 0, POSITION(',' IN rest))),  --postgresql only
      TRIM(SUBSTR(rest, POSITION(',' IN rest)+1))  --postgresql only
    FROM split
    WHERE rest <> '')

 SELECT
   date_,
   grade,
   display_grade,
   location,
   setter,
   description,
   wall_type,
   style,
   sep_hold_type AS hold_type
 FROM split 
 WHERE sep_hold_type <> ''),

count_table AS
(SELECT
   grade,
   hold_type,
   COUNT(hold_type) AS count_
 FROM unnested_primary_data
 GROUP BY grade, hold_type),

first_send AS
(SELECT 
   grade,
   hold_type, 
   MIN(date_) as date_
 FROM unnested_primary_data
 GROUP BY grade, hold_type)

SELECT
  f.grade,
  f.hold_type,
  c.count_,
  f.date_,
  p.display_grade,
  p.location,
  p.setter,
  p.description,
  p.wall_type,
  p.style
FROM first_send f
LEFT JOIN count_table c ON f.grade = c.grade AND f.hold_type = c.hold_type
LEFT JOIN unnested_primary_data p ON f.date_ = p.date_ AND f.grade = p.grade AND f.hold_type = p.hold_type
ORDER BY f.date_, f.grade, f.hold_type
;
