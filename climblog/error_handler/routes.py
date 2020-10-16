from flask import Blueprint, render_template, Markup
from werkzeug.debug import get_current_traceback


errors = Blueprint('errors', __name__,
                   template_folder='templates',
                   static_folder='static')


@errors.app_errorhandler(404)
def error_404(error):
    error_message = get_current_traceback()
    return render_template("404.html",
        error_message=error_message.plaintext), 404
