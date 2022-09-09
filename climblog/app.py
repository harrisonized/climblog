from flask import Flask, render_template
from apps.dashboard.routes import dashboard
from apps.guest_portal.routes import guest_portal
from apps.sql_terminal.routes import sql_terminal
from apps.error_handler.routes import error_handler
#from apps.new_module.routes import new_module

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
