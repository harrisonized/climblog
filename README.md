# Climb Log

Live web application found [here](https://harrisonized-climbing-app.herokuapp.com/).

Template based on [Dimension](https://html5up.net/dimension) by [HTML5UP](https://html5up.net).



## Introduction

This is an app that executes SQL queries on data stored in a [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) database, then uses that data to create interactive visualizations using [Plotly](https://plotly.com/python/). If the data cannot be retrieved from the postgres database or if you are interacting with it through the [guest portal](https://harrisonized-climbing-app.herokuapp.com/guest_portal), this app will instead use data from [CSV](https://github.com/harrisonized/harrisonized-climbing-app/tree/master/data) files. Once the visualizations are created, this app caches them as JSON files saved in `/tmp`, which is Heroku's ephemeral file storage system. Refreshing the page will result in the figure being read directly from the saved files rather than being regenerated from the data. Everything takes place on the server side.

Note that Heroku may take up to 30 seconds to come out of a [sleeping website state](https://devcenter.heroku.com/articles/free-dyno-hours#dyno-sleeping), and if there is no web traffic to the site after 30 minutes, it will sleep.



## Getting Started

1. Install the requirements and this library
2. Follow the instructions in `sql/create-database.sql` in your local postgres server to add the data in climbing-log.csv to your local database.
3. Add an INI_KEY environmental variable to your bashrc. You can generate it via `from climblog.utils.auth.encryption_tools import generate_new_key` in your python terminal.
4. Update the configs in `configs/cred.ini` with your postgres credentials. It may also be okay if you skip this step.
5. Run the server:  `python climblog/main.py`
6. Access the server: http://localhost:5000



## Latest Updates

| Date       | Update                                                       |
| ---------- | ------------------------------------------------------------ |
| 2022-10-04 | Move settings and paths to files in the etc folder           |
| 2022-09-13 | Make the application as compact as possible by removing redundant functions |
| 2020-12-09 | Enable users to upload their own CSVs to generate their own figures |
| 2020-12-07 | Add read-only SQL terminal                                   |
| 2020-11-04 | Fix Google Chrome iframe axis scaling bug (See: [here](https://community.plotly.com/t/cant-show-heatmap-inside-div-error-something-went-wrong-with-axis-scaling/30616)) |
| 2020-10-15 | Add error handling and logging, generate routes dynamically  |
| 2020-10-14 | Improve the look and feel of the app. Fix bug in which javascript from HTML5UP and Plotly were interfering with each other. Fix bug in which iframe wasn't being displayed correctly on phone. |
| 2020-10-13 | Create Heroku Postgres database and swap out datasource from CSV files to newly created database. Add an auth module to encrypt database URIs and unit test for database connections. Add logic to preferentially get data from Postgres database, then use the data from CSV files if Postgres is unavailable. |
| 2020-10-12 | Add figure caching                                           |



## License

    Climb Log
    Copyright (C) 2020  Harrison Wang
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.