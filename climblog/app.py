import os
from flask import Flask, render_template, Markup
from dashboard.routes import dashboard
from error_handler.routes import error_handler

real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)

# Initialize the app
app = Flask(__name__)
app.register_blueprint(dashboard)
app.register_blueprint(error_handler)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/indoor", methods=["GET"])
def indoor():
    location_type = {'title': 'Indoor',
                     'lower': 'indoor', }

    return render_template(
        "dashboard.html",
        location_type=location_type,
    )


@app.route("/outdoor", methods=["GET"])
def outdoor():
    location_type = {'title': 'Outdoor',
                     'lower': 'outdoor', }

    return render_template(
        "dashboard.html",
        location_type=location_type,
    )
