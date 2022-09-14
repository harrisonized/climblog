-- run 'heroku pg:psql postgresql-regular-13122 --app harrisonized-climbing-app' to connect to heroku postgres

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

\copy boulders FROM '/home/harrisonized/github/python/climbing-app/climblog/data/climbing-log.csv' DELIMITER ',' CSV HEADER;
