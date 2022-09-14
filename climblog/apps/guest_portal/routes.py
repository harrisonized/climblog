"""
Displays climbing data for any files you upload
Please follow the format set by climbing-log.csv
"""

import os
import shutil
from glob import glob
import json
import pandas as pd
from flask import Blueprint, render_template, request, redirect, Markup
from climblog.utils.handlers.data_handler import append_standard_df
from climblog.etc.columns import sends_by_date_scatter_columns
from climblog.apps.dashboard.generate_fig import generate_fig_switch

data_dir = 'tmp/guest_portal/data'
fig_dir = 'tmp/guest_portal/figures'


guest_portal = Blueprint('guest_portal', __name__,
                         template_folder='templates',
                         static_folder='static',
                         )

# ----------------------------------------------------------------------
# Home pages

@guest_portal.route("/guest_portal", methods=["GET", "POST"])
def portal():
    uploads = [file[9:] for file in glob(f'{data_dir}/*')]
    upload_filename = 'climbing-log.csv' if 'climbing-log.csv' in uploads else False
    return render_template("guest_portal.html",
                           upload_file=upload_filename)


@guest_portal.route("/guest_portal/indoor", methods=["GET"])
def indoor():
    location_type = {'title': 'Indoor',
                     'lower': 'indoor', }

    return render_template(
        "guest_dashboard.html",
        location_type=location_type
    )


@guest_portal.route("/guest_portal/outdoor", methods=["GET"])
def outdoor():
    location_type = {'title': 'Outdoor',
                     'lower': 'outdoor', }

    return render_template(
        "guest_dashboard.html",
        location_type=location_type
    )

# ----------------------------------------------------------------------
# Actions

@guest_portal.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    for file in files:
        if file.filename in ['climbing-log.csv']:

            # check if actual csv
            try:
                raw_df = pd.read_csv(file)
            except:
                raw_df = pd.DataFrame(sends_by_date_scatter_columns)
            df = append_standard_df(raw_df, columns=sends_by_date_scatter_columns)

            if not df.empty:
                os.makedirs(data_dir, exist_ok=True)  # make sure folder exists
                df.to_csv(f'{data_dir}/{file.filename}', index=None)
                print(f'{file.filename} uploaded')
            else:
                print(f'{file.filename} empty! NOT uploaded!')
        else:
            print(f'{file.filename} ignored')

    return redirect("/guest_portal#apps")


@guest_portal.route("/delete", methods=["POST"])
def delete():
    shutil.rmtree(data_dir, ignore_errors=True)
    shutil.rmtree(fig_dir, ignore_errors=True)
    return redirect("/guest_portal#upload")

# ----------------------------------------------------------------------
# Figures

@guest_portal.route("/fig/guest_portal/<location_type>/<plot_type>", methods=["GET"])
def plot(location_type, plot_type):

    div = generate_fig_switch[plot_type](location_type, fig_dir=fig_dir, data_dir=data_dir, query_db=False)

    return render_template(
        "fig.html",
        div=Markup(div)
    )
