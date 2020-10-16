# Harrison's Climbing App

This [live web application](https://harrisonized-climbing-app.herokuapp.com/) is a dashboard that executes SQL queries on data stored in a [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) database, then uses that data to create interactive visualizations using [Plotly](https://plotly.com/python/). If the data cannot be retrieved from the postgres database, this app will instead use data from [CSV](https://github.com/harrisonized/harrisonized-climbing-app/tree/master/data) files. Once the visualizations are created, this app caches them as JSON files saved in `/tmp`, which is Heroku's ephemeral file storage system. Refreshing the page will result in the figure being read directly from the saved files rather than being regenerated from the data. Everything takes place on the server side.

Note that Heroku may take up to 30 seconds to come out of a sleeping website state.

Here are some of the latest updates in reverse-chronological order:

1. Add error handling and logging
2. Generate routes dynamically
3. Improve the look and feel of the app. Fix bug in which javascript from HTML5UP and Plotly were interfering with each other. Fix bug in which iframe wasn't being displayed correctly on phone.
4. Add logic to preferentially get data from Postgres database, then use the data from CSV files if Postgres is unavailable.
5. Create Heroku Postgres database and swap out datasource from CSV files to newly created database
6. Add an auth module to encrypt database URIs and unit test for database connections
7. Add figure caching

Future goals for this project include:

3. Generate figures in the background when the app is started
2. Be able to export data to CSV files
3. Enable users to upload their own CSVs and generate their own figures