# Climb Log

Live web application found [here](https://harrisonized-climbing-app.herokuapp.com/).

Template based on [Dimension](https://html5up.net/dimension) by [HTML5UP](https://html5up.net).



## Introduction

This is a dashboard that executes SQL queries on data stored in a [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) database, then uses that data to create interactive visualizations using [Plotly](https://plotly.com/python/). If the data cannot be retrieved from the postgres database, this app will instead use data from [CSV](https://github.com/harrisonized/harrisonized-climbing-app/tree/master/data) files. Once the visualizations are created, this app caches them as JSON files saved in `/tmp`, which is Heroku's ephemeral file storage system. Refreshing the page will result in the figure being read directly from the saved files rather than being regenerated from the data. Everything takes place on the server side.

Note that Heroku may take up to 30 seconds to come out of a sleeping website state.



## Latest Updates

Reverse-chronological order:

1. Upgrade library with potential security issue (cryptography>=3.2)
2. Fix Google Chrome iframe axis scaling bug (See: [here](https://community.plotly.com/t/cant-show-heatmap-inside-div-error-something-went-wrong-with-axis-scaling/30616))
3. Add error handling and logging
4. Generate routes dynamically
5. Improve the look and feel of the app. Fix bug in which javascript from HTML5UP and Plotly were interfering with each other. Fix bug in which iframe wasn't being displayed correctly on phone.
6. Add logic to preferentially get data from Postgres database, then use the data from CSV files if Postgres is unavailable.
7. Create Heroku Postgres database and swap out datasource from CSV files to newly created database
8. Add an auth module to encrypt database URIs and unit test for database connections
9. Add figure caching



## Future Goals

1. Be able to export data to CSV files
2. Generate figures in the background when the app is started
3. Enable users to upload their own CSVs and generate their own figures



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