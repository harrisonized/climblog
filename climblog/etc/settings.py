from climblog.utils.handlers.file_handler import read_section_from_ini
from .paths import settings_cfg_path

default_settings = read_section_from_ini(settings_cfg_path)
use_csv_backup = default_settings.getboolean('use_csv_backup')
read_fig_from_cache = default_settings.getboolean('read_fig_from_cache')
export_fig = default_settings.getboolean('export_fig')
show_traceback = default_settings.getboolean('show_traceback')
