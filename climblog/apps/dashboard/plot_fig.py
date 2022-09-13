import datetime as dt
import numpy as np
import matplotlib.dates as mdates
import plotly.graph_objs as go
from scipy.optimize import curve_fit

from climblog.utils.plotting import plot_scatter, plot_bar, plot_heatmap
from climblog.utils.handlers.data_handler import word_wrap
from climblog.utils.curve_fit import logistic_func


# Functions included in this file:
# # curve_fit_new_grades
# # hovertext_for_heatmap
# # plot_fig_for_sends_by_date_scatter
# # plot_fig_for_grades_histogram
# # plot_fig_for_grades_by_heatmap


def curve_fit_new_grades(df, grade='grade', date_='date_', p0=None):
    """Get logistic function parameters for boundary
    """

    # filter non-increasing grades
    while True:
        num_rows = len(df)
        df = df[(df[grade]-df[grade].shift().fillna(0) > 0)]
        if len(df) == num_rows:
            break

    popt, pcov = curve_fit(
        logistic_func,
        df[date_].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
        df[grade],
        p0=p0
    )
    return popt


def hovertext_for_heatmap(df, column_list=None):
    """Used in all heatmap functions
    """
    
    # sort
    if df.columns[1] == 'year' and column_list is None:
        column_list = df[df.columns[1]].unique()
    elif df.columns[1] == 'year':
        column_list = column_list.sort()
    elif column_list is None:
        column_list = df[df.columns[1]].value_counts().index
    else:
        pass

    # derive raw input data
    df = df[df[df.columns[1]].isin(column_list)].reset_index(drop=True)  # Filter
    df.description = df.description.apply(lambda x: word_wrap(str(x), 10))

    # Hover text
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: int(x[1:]) if type(x) == str else x)

    grade_table = df.pivot(index="grade", columns=df.columns[1], values="display_grade") \
        .applymap(str).applymap(lambda x: x.replace('.0', '')) \
        .applymap(lambda x: x.replace('Vnan', 'nan')) \
        .applymap(lambda x: float(x) if x == 'nan' else x)

    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + df.pivot(index="grade", columns=df.columns[1], values="date_").applymap(str) + '<br>' \
                 + 'Grade: ' + grade_table + '<br>' \
                 + 'Location: ' + df.pivot(index="grade", columns=df.columns[1], values="location").applymap(str) + '<br>' \
                 + 'Setter: ' + df.pivot(index="grade", columns=df.columns[1], values="setter").applymap(str) + '<br>' \
                 + 'Wall-type: ' + df.pivot(index="grade", columns=df.columns[1], values="wall_type").applymap(str) + '<br>' \
                 + 'Hold-type: ' + df.pivot(index="grade", columns=df.columns[1], values="hold_type").applymap(str) + '<br>' \
                 + 'Style: ' + df.pivot(index="grade", columns=df.columns[1], values="style").applymap(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df.pivot(index="grade", columns=df.columns[1], values="description") + '<br>'

    hover_text.index = hover_text.index.map(lambda x: 'V' + str(x) if type(x) == int else x)
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: 'V' + str(x) if type(x) == int else x)

    # Annotations
    annotations = []
    for i in range(len(df)):
        annotations.append(dict(x=df[df.columns[1]][i],
                                y=df[df.columns[0]][i],
                                text=str(df[df.columns[2]][i]),
                                showarrow=False))

    return hover_text, annotations


def plot_fig_for_sends_by_date_scatter(scatter_df, logistic_params=None):

    # plot main figure
    hover_text = 'Grade: ' + scatter_df['display_grade'].apply(str) + '<br>' \
                 + 'Location: ' + scatter_df['location'].apply(str) + '<br>' \
                 + 'Setter: ' + scatter_df['setter'].apply(str) + '<br>' \
                 + 'Wall-type: ' + scatter_df['wall_type'].apply(str) + '<br>' \
                 + 'Hold-type: ' + scatter_df['hold_type'].apply(str) + '<br>' \
                 + 'Style: ' + scatter_df['style'].apply(str) + '<br>' \
                 + 'Description:<br>' +scatter_df['description'].apply(lambda x: word_wrap(str(x), 10)) + '<br>'
    hover_template = "Date: %{x}<br>%{text}<br><extra></extra>"

    fig = plot_scatter(scatter_df, x="date_", y="grade", color='color',
                       xlabel="Date", ylabel="Grade", title="Sends by Date",
                       hovertext=hover_text, hovertemplate=hover_template)
    if logistic_params is not None:
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

    return fig


def plot_fig_for_grades_histogram(grades_histogram_df):
    """df should look like the following:
    """

    # plot main figure
    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + grades_histogram_df['date_'].apply(str) + '<br>' \
                 + 'Grade: ' + grades_histogram_df['display_grade'].apply(str) + '<br>' \
                 + 'Location: ' + grades_histogram_df['location'].apply(str) + '<br>' \
                 + 'Setter: ' + grades_histogram_df['setter'].apply(str) + '<br>' \
                 + 'Wall-type: ' + grades_histogram_df['wall_type'].apply(str) + '<br>' \
                 + 'Hold-type: ' + grades_histogram_df['hold_type'].apply(str) + '<br>' \
                 + 'Style: ' + grades_histogram_df['style'].apply(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + grades_histogram_df['description'].apply(str).apply(lambda x: word_wrap(str(x), 10)) + '<br>'
    hover_template = "Number of Recorded Sends: %{y}<br>%{text}<br><extra></extra>"

    grades_histogram_df = grades_histogram_df.sort_values('grade').reset_index(drop=True)
    grades_histogram_df['grade'] = grades_histogram_df['grade'].apply(lambda x: 'V'+str(x))

    fig = plot_bar(grades_histogram_df, x='grade', y='count_', color='color',
                   xlabel='Grades Histogram', ylabel='Grade', title='Number of Recorded Sends',
                   hovertext=hover_text, hovertemplate=hover_template)

    return fig


def plot_fig_for_grades_by_heatmap(heatmap_input_df,
                                   hovertext_input_df,
                                   xlabel,
                                   ylabel='Grade',
                                   columns=None):

    # columns = [col for col in columns if col in hovertext_input_df.columns]
    hover_text, annotations = hovertext_for_heatmap(hovertext_input_df, columns)
    fig = plot_heatmap(heatmap_input_df,
                       xlabel=xlabel, ylabel=ylabel, title=f"Heatmap of {ylabel}s by {xlabel}",
                       hovertext=hover_text, annotations=annotations)

    return fig
