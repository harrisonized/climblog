-- postgresql

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
   LOWER(style) AS style,
   LOWER(hold_type) AS hold_type
 FROM route_info
 WHERE location_type = '{location_type}'),

unnested_primary_data AS
(WITH RECURSIVE SPLIT(date_, grade_, location, setter, description, wall_type, style,
                      sep_hold_type, rest) AS

   (SELECT date_, grade_, location, setter, description, wall_type, style, 
      '',
      hold_type || ','
    FROM primary_data
       
    UNION ALL
  
    SELECT date_, grade_, location, setter, description, wall_type, style, 
      TRIM(SUBSTR(rest, 0, POSITION(',' IN rest))),  --postgresql only
      TRIM(SUBSTR(rest, POSITION(',' IN rest)+1))  --postgresql only
    FROM split
    WHERE rest <> '')

 SELECT
   date_,
   grade_,
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
   grade_,
   hold_type,
   COUNT(hold_type) AS count_
 FROM unnested_primary_data
 GROUP BY grade_, hold_type),

first_send AS
(SELECT 
   grade_,
   hold_type, 
   MIN(date_) as date_
 FROM unnested_primary_data
 GROUP BY grade_, hold_type)

SELECT
  f.grade_,
  f.hold_type,
  c.count_,
  f.date_,
  p.location,
  p.setter,
  p.description,
  p.wall_type,
  p.style
FROM first_send f
LEFT JOIN count_table c ON f.grade_ = c.grade_ AND f.hold_type = c.hold_type
LEFT JOIN unnested_primary_data p ON f.date_ = p.date_ AND f.grade_ = p.grade_ AND f.hold_type = p.hold_type
ORDER BY f.date_, f.grade_, f.hold_type
;
