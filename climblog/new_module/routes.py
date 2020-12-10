from flask import Blueprint, render_template

new_module = Blueprint('new_module', __name__,
                       template_folder='templates',
                       static_folder='static')

@new_module.route("/test", methods=["GET", "POST"])
def new_module():
    return render_template("new_module.html")
