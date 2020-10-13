import os
import datetime as dt
import json
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import plotly
import plotly.graph_objs as go
import plotly.offline as pyo
from apps.plotting.text_tools import word_wrap
from apps.plotting.query_tools import execute_query_on_df
from apps.plotting.plotly_tools import color_dict, plot_scatter, plot_bar, plot_heatmap, labels_for_heatmap
from apps.plotting.curve_fit import curve_fit_new_grades, logistic_func
from .queries import SENDS_BY_DATE, GRADES_HISTOGRAM, GRADES_BY_YEAR, GRADES_BY_WALL, GRADES_BY_HOLD, GRADES_BY_STYLE


# Functions included in this file:
# # retrieve_sends_by_date_scatter
# # retrieve_grades_histogram
# # retrieve_grades_by_year_heatmap
# # retrieve_grades_by_wall_heatmap
# # retrieve_grades_by_hold_heatmap
# # retrieve_grades_by_style_heatmap


def retrieve_sends_by_date_scatter(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'sends-by-date'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        climbing_log_df = pd.read_csv(data_path)
        scatter_df = execute_query_on_df(SENDS_BY_DATE, climbing_log_df, replace_grade=True)
        scatter_df['date_'] = scatter_df['date_'].apply(lambda date: dt.datetime.strptime(date, '%Y-%m-%d'))  # Convert to datetime
        scatter_df['color'] = scatter_df['color'].replace(color_dict)  # Replace colors with hex codes

        # plot main figure
        hover_text = 'Grade: ' + scatter_df['vgrade'].apply(str) + '<br>' \
                     + 'Location: ' + scatter_df['location'].apply(str) + '<br>' \
                     + 'Setter: ' + scatter_df['setter'].apply(str) + '<br>' \
                     + 'Wall-type: ' + scatter_df['wall_type'].apply(str) + '<br>' \
                     + 'Hold-type: ' + scatter_df['hold_type'].apply(str) + '<br>' \
                     + 'Style: ' + scatter_df['style'].apply(str) + '<br>' \
                     + 'Description: ' + '<br>' \
                     + scatter_df['description'].apply(lambda x: word_wrap(str(x), 10)) + '<br>'
        hover_template = "Date: %{x}<br>%{text}<br><extra></extra>"

        fig = plot_scatter(scatter_df, x="date_", y="grade_", color='color',
                           xlabel="Date", ylabel="Grade", title="Sends by Date",
                           hovertext=hover_text, hovertemplate=hover_template)

        # plot boundary curve
        grades_histogram_df = execute_query_on_df(GRADES_HISTOGRAM, climbing_log_df, replace_grade=True)
        grades_histogram_df['color'] = grades_histogram_df['color'].replace(color_dict)
        logistic_params = curve_fit_new_grades(grades_histogram_df)
        date_linspace = np.linspace(
            mdates.date2num(scatter_df['date_'].min()),  # Date min
            mdates.date2num(scatter_df['date_'].max()),  # Date max
            num=25)
        new_grades_scatter = go.Scatter(x=mdates.num2date(date_linspace),
                                        y=logistic_func(date_linspace, *logistic_params),
                                        mode='lines',
                                        line={'color': 'lightgreen'},
                                        hoverinfo='skip')
        fig.add_trace(new_grades_scatter)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_histogram(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'grades-histogram'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        climbing_log_df = pd.read_csv(data_path)
        grades_histogram_df = execute_query_on_df(GRADES_HISTOGRAM, climbing_log_df, replace_grade=True)
        grades_histogram_df['color'] = grades_histogram_df['color'].replace(color_dict)

        # plot main figure
        hover_text = 'FIRST RECORDED SEND<br>' \
                     + 'Date: ' + grades_histogram_df['date_'].apply(str) + '<br>' \
                     + 'Grade: ' + grades_histogram_df['grade'].apply(str) + '<br>' \
                     + 'Location: ' + grades_histogram_df['location'].apply(str) + '<br>' \
                     + 'Setter: ' + grades_histogram_df['setter'].apply(str) + '<br>' \
                     + 'Wall-type: ' + grades_histogram_df['wall_type'].apply(str) + '<br>' \
                     + 'Hold-type: ' + grades_histogram_df['hold_type'].apply(str) + '<br>' \
                     + 'Style: ' + grades_histogram_df['style'].apply(str) + '<br>' \
                     + 'Description: ' + '<br>' \
                     + grades_histogram_df['description'].apply(str).apply(lambda x: word_wrap(str(x), 10)) + '<br>'
        hover_template = "Number of Recorded Sends: %{y}<br>%{text}<br><extra></extra>"

        grades_histogram_df = grades_histogram_df.sort_values('grade_').reset_index(drop=True)
        grades_histogram_df['grade_'] = grades_histogram_df['grade_'].apply(lambda x: 'V'+str(x))
        fig = plot_bar(grades_histogram_df, x='grade_', y='count_', color='color',
                       xlabel='Grades Histogram', ylabel='Grade', title='Number of Recorded Sends',
                       hovertext=hover_text, hovertemplate=hover_template)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_year_heatmap(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'grades-by-year'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        df = pd.read_csv(data_path)
        year_df = execute_query_on_df(GRADES_BY_YEAR, df, replace_grade=True)

        table_df = year_df.reset_index().pivot(index=year_df.columns[1], columns=year_df.columns[0], values="count_").fillna(0)
        table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades

        # plot main figure
        hover_text, annotations = labels_for_heatmap(year_df)
        fig = plot_heatmap(table_df,
                           "Year", "Grade", "Heatmap of Grades by Year",
                           hover_text, annotations)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_wall_heatmap(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'grades-by-wall-type'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        df = pd.read_csv(data_path)
        wall_df = execute_query_on_df(GRADES_BY_WALL, df, replace_grade=True)

        columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
        table_df = wall_df.reset_index().pivot(index=wall_df.columns[1], columns=wall_df.columns[0], values="count_").fillna(0)
        table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
        table_df = table_df[columns]  # sort columns

        # plot main figure
        hover_text, annotations = labels_for_heatmap(wall_df, columns)
        fig = plot_heatmap(table_df,
                           "Wall-type", "Grade", "Heatmap of Grades by Wall-type",
                           hover_text, annotations)
        fig.layout.update(annotations=annotations)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_hold_heatmap(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'grades-by-hold-type'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        df = pd.read_csv(data_path)
        hold_df = execute_query_on_df(GRADES_BY_HOLD, df, replace_grade=True)

        columns = ['jug', 'crimp', 'sloper', 'pinch']
        table_df = hold_df.reset_index().pivot(index=hold_df.columns[1], columns=hold_df.columns[0], values="count_").fillna(0)
        table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
        table_df = table_df[columns]  # sort columns

        # plot main figure
        hover_text, annotations = labels_for_heatmap(hold_df, columns)
        fig = plot_heatmap(table_df,
                           "Hold-type", "Grade", "Heatmap of Grades by Hold-type",
                           hover_text, annotations)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div


def retrieve_grades_by_style_heatmap(fig_dir, data_path):
    """If figure file is found in tmp folder, read in figure file and generate div
    Else read in data and generate figure and save in tmp folder
    """

    filename = 'grades-by-style'

    if os.path.exists(f'tmp/{fig_dir}/{filename}.json'):

        with open(f'tmp/{fig_dir}/{filename}.json') as file:
            fig = json.load(file)

        div = pyo.plot(fig, output_type='div')

    else:

        # get data
        df = pd.read_csv(data_path)
        style_df = execute_query_on_df(GRADES_BY_STYLE, df, replace_grade=True)

        columns = ['mantle', 'natural', 'dyno', 'comp']
        table_df = style_df.reset_index().pivot(index=style_df.columns[1], columns=style_df.columns[0], values="count_").fillna(0)
        table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
        table_df = table_df[columns]  # sort columns

        # plot main figure
        hover_text, annotations = labels_for_heatmap(style_df, columns)
        fig = plot_heatmap(table_df,
                           "Style", "Grade", "Heatmap of Grades by Style",
                           hover_text, annotations)

        # save
        os.makedirs(f'tmp/{fig_dir}', exist_ok=True)
        with open(f'tmp/{fig_dir}/{filename}.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)

        div = pyo.plot(fig, output_type='div')  # div for fig

    return div
