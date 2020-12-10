import os
from flask import Flask, render_template
from error_handler.routes import error_handler
from dashboard.routes import dashboard
from sql_terminal.routes import sql_terminal
from guest_portal.routes import guest_portal
#from new_module.routes import new_module


real_path = os.path.realpath(__file__)
dir_name = os.path.dirname(real_path)


# Initialize the app
app = Flask(__name__)
app.register_blueprint(error_handler)
app.register_blueprint(dashboard)
app.register_blueprint(sql_terminal)
app.register_blueprint(guest_portal)
#app.register_blueprint(new_module)


@app.route("/")
def home():
    return render_template("home.html")
