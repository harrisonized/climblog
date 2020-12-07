import os
from flask import Flask, render_template
from error_handler.routes import error_handler
from dashboard.routes import dashboard
from sql_terminal.routes import sql_terminal

real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)

# Initialize the app
app = Flask(__name__)
app.register_blueprint(error_handler)
app.register_blueprint(dashboard)
app.register_blueprint(sql_terminal)


@app.route("/")
def home():
    return render_template("home.html")
