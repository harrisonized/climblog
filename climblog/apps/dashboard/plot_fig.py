"""Plotting functions specific to climblog data
"""

import numpy as np
import plotly.graph_objs as go
import matplotlib.dates as mdates

from climblog.utils.curve_fit import logistic_func
from climblog.utils.plotting import plot_scatter, plot_bar, plot_heatmap
from climblog.utils.handlers.data_handler import word_wrap
from climblog.etc.colors import color_name_to_hex, color_grade_to_name


# Functions
# # curve_fit_new_grades
# # hovertext_for_heatmap
# # plot_fig_for_sends_by_date_scatter
# # plot_fig_for_grades_histogram
# # plot_fig_for_grades_by_heatmap


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


def plot_fig_for_sends_by_date_scatter(df, logistic_params=None):

    df.loc[df['color'].isna(), 'color'] = df.loc[df['color'].isna(), 'grade'].replace(color_grade_to_name)  # add a color if null
    df['color'] = df['color'].replace(color_name_to_hex)  # Replace colors with hex codes

    # plot main figure
    hover_text = 'Grade: ' + df['display_grade'].apply(str) + '<br>' \
                 + 'Location: ' + df['location'].apply(str) + '<br>' \
                 + 'Setter: ' + df['setter'].apply(str) + '<br>' \
                 + 'Wall-type: ' + df['wall_type'].apply(str) + '<br>' \
                 + 'Hold-type: ' + df['hold_type'].apply(str) + '<br>' \
                 + 'Style: ' + df['style'].apply(str) + '<br>' \
                 + 'Description:<br>' +df['description'].apply(lambda x: word_wrap(str(x), 10)) + '<br>'
    hover_template = "Date: %{x}<br>%{text}<br><extra></extra>"

    fig = plot_scatter(df, x="date_", y="grade", color='color',
                       xlabel="Date", ylabel="Grade", title="Sends by Date",
                       hovertext=hover_text, hovertemplate=hover_template)
    if logistic_params is not None:
        date_linspace = np.linspace(
            mdates.date2num(df['date_'].min()),  # Date min
            mdates.date2num(df['date_'].max()),  # Date max
            num=25)
        new_grades_scatter = go.Scatter(x=mdates.num2date(date_linspace),
                                        y=logistic_func(date_linspace, *logistic_params),
                                        mode='lines',
                                        line={'color': 'lightgreen'},
                                        hoverinfo='skip')
        fig.add_trace(new_grades_scatter)

    return fig


def plot_fig_for_grades_histogram(df):
    """df should look like the following:
    """

    # plot main figure
    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + df['date_'].apply(str) + '<br>' \
                 + 'Grade: ' + df['display_grade'].apply(str) + '<br>' \
                 + 'Location: ' + df['location'].apply(str) + '<br>' \
                 + 'Setter: ' + df['setter'].apply(str) + '<br>' \
                 + 'Wall-type: ' + df['wall_type'].apply(str) + '<br>' \
                 + 'Hold-type: ' + df['hold_type'].apply(str) + '<br>' \
                 + 'Style: ' + df['style'].apply(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df['description'].apply(str).apply(lambda x: word_wrap(str(x), 10)) + '<br>'
    hover_template = "Number of Recorded Sends: %{y}<br>%{text}<br><extra></extra>"

    df = df.sort_values('grade').reset_index(drop=True)
    df['grade'] = df['grade'].apply(lambda x: 'V'+str(x))

    df.loc[df['color'].isna(), 'color'] = df.loc[df['color'].isna(), 'grade'].replace(color_grade_to_name)
    df['color'] = df['color'].replace(color_name_to_hex)

    fig = plot_bar(df, x='grade', y='count_', color='color',
                   xlabel='Grades Histogram', ylabel='Grade', title='Number of Recorded Sends',
                   hovertext=hover_text, hovertemplate=hover_template)

    return fig


def plot_fig_for_grades_by_heatmap(heatmap_df,
                                   hovertext_df,
                                   xlabel,
                                   ylabel='Grade',
                                   columns=None):

    # columns = [col for col in columns if col in hovertext_input_df.columns]
    hover_text, annotations = hovertext_for_heatmap(hovertext_df, columns)
    fig = plot_heatmap(heatmap_df,
                       xlabel=xlabel, ylabel=ylabel, title=f"Heatmap of {ylabel}s by {xlabel}",
                       hovertext=hover_text, annotations=annotations)

    return fig
