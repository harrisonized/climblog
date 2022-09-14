from flask import Blueprint, render_template
from werkzeug.debug import get_current_traceback
import logging
from climblog.utils.handlers.file_handler import read_section_from_ini

default_settings = read_section_from_ini()
show_traceback = default_settings.getboolean('show_traceback')

log = logging.getLogger(__name__)

error_handler = Blueprint('error_handler', __name__,
                          template_folder='templates',
                          static_folder='static')


@error_handler.app_errorhandler(404)
def page_not_found(error):

    if show_traceback:
        error_message = get_current_traceback()
        log.error(error_message.plaintext)
        return render_template("404.html",
                               error_message=error_message.plaintext), 404
    
    return render_template("404.html"), 404



@error_handler.app_errorhandler(405)
def method_not_allowed(error):

    if show_traceback:
        error_message = get_current_traceback()
        log.error(error_message.plaintext)
        return render_template("405.html",
                               error_message=error_message.plaintext), 405

    return render_template("405.html"), 405    


@error_handler.app_errorhandler(500)
def internal_server_error(error):
    
    if show_traceback:
        error_message = get_current_traceback()
        log.error(error_message.plaintext)
        return render_template("500.html",
                               error_message=error_message.plaintext), 500

    return render_template("500.html"), 500
