import os
import shutil
from glob import glob
import json
import pandas as pd
from flask import Blueprint, render_template, request, redirect, Markup
from climblog.utils.handlers.data_handler import append_standard_df
from climblog.apps.guest_portal.retrieve_fig import (retrieve_sends_by_date_scatter,
                                            retrieve_grades_histogram,
                                            retrieve_grades_by_year_heatmap,
                                            retrieve_grades_by_wall_heatmap,
                                            retrieve_grades_by_hold_heatmap,
                                            retrieve_grades_by_style_heatmap)

retrieve_fig = {'timeseries': retrieve_sends_by_date_scatter,
                'histogram': retrieve_grades_histogram,
                'year': retrieve_grades_by_year_heatmap,
                'wall': retrieve_grades_by_wall_heatmap,
                'hold': retrieve_grades_by_hold_heatmap,
                'style': retrieve_grades_by_style_heatmap,
                }


guest_portal = Blueprint('guest_portal', __name__,
                         template_folder='templates',
                         static_folder='static',
                         )


@guest_portal.route("/guest_portal", methods=["GET", "POST"])
def portal():
    uploads = [file[9:] for file in glob('tmp/data/*')]
    upload_indoor = 'climbing-log-indoor.csv' if 'climbing-log-indoor.csv' in uploads else False
    upload_outdoor = 'climbing-log-outdoor.csv' if 'climbing-log-outdoor.csv' in uploads else False
    return render_template("guest_portal.html",
                           upload_indoor=upload_indoor,
                           upload_outdoor=upload_outdoor)


@guest_portal.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    for file in files:
        if file.filename in ['climbing-log-indoor.csv',
                             'climbing-log-outdoor.csv']:

            # check if actual csv
            try:
                raw_df = pd.read_csv(file)
            except:
                raw_df = pd.DataFrame()
            df = append_standard_df(raw_df)

            if not df.empty:
                os.makedirs('tmp/data', exist_ok=True)  # make sure folder exists
                df.to_csv(f'tmp/data/{file.filename}', index=None)
                print(f'{file.filename} uploaded')
            else:
                print(f'{file.filename} empty! NOT uploaded!')
        else:
            print(f'{file.filename} ignored')

    return redirect("/guest_portal#apps")


@guest_portal.route("/delete", methods=["POST"])
def delete():
    shutil.rmtree('tmp/data', ignore_errors=True)
    shutil.rmtree('tmp/figures/guest_portal', ignore_errors=True)
    return redirect("/guest_portal#upload")


@guest_portal.route("/guest_portal/indoor", methods=["GET"])
def indoor():
    location_type = {'title': 'Indoor',
                     'lower': 'indoor', }

    return render_template(
        "guest_dashboard.html",
        location_type=location_type,
    )


@guest_portal.route("/guest_portal/outdoor", methods=["GET"])
def outdoor():
    location_type = {'title': 'Outdoor',
                     'lower': 'outdoor', }

    return render_template(
        "guest_dashboard.html",
        location_type=location_type,
    )


@guest_portal.route("/fig/guest_portal/<location_type>/<plot_type>", methods=["GET"])
def plot(location_type, plot_type):

    div = retrieve_fig[plot_type](location_type)

    return render_template(
        "fig.html",
        div=Markup(div)
    )
