# Harrison's Climbing App

This [live web application](https://harrisonized-climbing-app.herokuapp.com/) is a dashboard that executes SQL queries on [data](https://github.com/harrisonized/climbing-app-heroku/tree/master/data) from CSV files and creates interactive visualizations using Plotly. Everything takes place on the server side. Note that Heroku may take up to 30 seconds to come out of a sleeping website state.

In the latest update, I added a cache for figures so if they are already generated, they can be retrieved directly from Heroku's ephemeral storage rather than being regenerated from the data.

 Future goals I have for this app are:

1. Swap out the datasource with Postgres
2. Improve the look and feel of the Home page
3. Add drop-downs or menus for selecting figures on the Figure pages.