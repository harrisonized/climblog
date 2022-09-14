-- run sudo su -l postgres
-- run 'heroku pg:psql postgresql-regular-13122 --app harrisonized-climbing-app' to connect to heroku postgres

-- optional
CREATE DATABASE climblog
\c climblog

DROP TABLE boulders

CREATE TABLE boulders(
  index_ INT,
  date_ TEXT,
  location_type TEXT,
  grade INT,
  display_grade TEXT,
  location TEXT,
  color TEXT,
  description TEXT,
  wall_type TEXT,
  hold_type TEXT,
  style TEXT,
  setter TEXT
);

\copy boulders FROM 'data/climbing-log.csv' DELIMITER ',' CSV HEADER;
