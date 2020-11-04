from flask import Blueprint, render_template, Markup
from werkzeug.debug import get_current_traceback
import logging


log = logging.getLogger(__name__)

errors = Blueprint('errors', __name__,
                   template_folder='templates',
                   static_folder='static')

@errors.app_errorhandler(404)
def error_404(error):
    error_message = get_current_traceback()
    log.error(error_message.plaintext)
    return render_template("404.html",
        error_message=error_message.plaintext), 404