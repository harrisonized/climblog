import random
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import plotly.graph_objs as go
from apps.plotting.curve_fit import logistic_func


# Objects included in this file:
# warm
# color_dict
 
# Functions included in this file:
# # word_wrap
# # plot_scatter
# # plot_histogram
# # plot_heatmap


warm = [[0.0, "rgb(255,248,248)"],
        [0.2, "rgb(254,224,144)"],
        [0.4, "rgb(253,174,97)"],
        [0.6, "rgb(244,109,67)"],
        [0.8, "rgb(215,48,39)"],
        [1.0, "rgb(165,0,38)"]]


color_dict = {'black': '#000000',
              'blue': '#1f77b4',
              'brown': '#8c564b',
              'colorless': '#7f7f7f',
              'green': '#2ca02c',
              'orange': '#ff7f0e',
              'pink': '#e377c2',
              'purple': '#9467bd',
              'red': '#d62728',
              'white': '#7f7f7f',
              'yellow': '#FFFF00'}


def word_wrap(string, n):
    string_list = string.split()
    parsed_list = [string_list[n * i:n * (i + 1)] for i in range((len(string_list) + n - 1) // n)]
    joined_string_list = [' '.join(parsed_list[i]) for i in range(len(parsed_list))]
    final_list = ['<br>'.join(joined_string_list)]
    return final_list[0]


def plot_scatter(df, popt, title, xlabel, ylabel):
    """
    """

    # Jitter
    df.date_ = df.date_.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))  # Convert to datetime
    # df.date_ = df.date_.apply(lambda x: x+dt.timedelta(seconds=30*random.random())) # Jitter
    df.grade_ = df.grade_.apply(lambda x: x - 0.15 + 0.3 * random.random())  # Jitter

    fig = go.Figure()

    hover_text = 'Grade: ' + df['vgrade'].apply(lambda x: str(x)) + '<br>' \
                 + 'Location: ' + df['location'].apply(lambda x: str(x)) + '<br>' \
                 + 'Setter: ' + df['setter'].apply(lambda x: str(x)) + '<br>' \
                 + 'Wall-type: ' + df['wall_type'].apply(lambda x: str(x)) + '<br>' \
                 + 'Hold-type: ' + df['hold_type'].apply(lambda x: str(x)) + '<br>' \
                 + 'Style: ' + df['style'].apply(lambda x: str(x)) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df['description'].apply(lambda x: word_wrap(str(x), 10)) + '<br>'

    all_records_scatter = go.Scatter(x=df.date_,
                                     y=df.grade_,
                                     mode='markers',
                                     marker={'color': df.color},
                                     text=hover_text,
                                     hovertemplate="Date: %{x}<br>"
                                                   "%{text}<br>" +
                                                   "<extra></extra>")

    date_linspace = np.linspace(
        mdates.date2num(df.date_.min()),  # Date min
        mdates.date2num(df.date_.max()),  # Date max
        num=25)

    new_grades_scatter = go.Scatter(x=mdates.num2date(date_linspace),
                                    y=logistic_func(date_linspace, *popt),
                                    mode='lines',
                                    line={'color': 'lightgreen'},
                                    hoverinfo='skip')

    fig.add_trace(all_records_scatter)
    fig.add_trace(new_grades_scatter)

    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True,
               'range': None},
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': [df.grade_.min() - 0.5, df.grade_.max() + 0.5]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        hovermode='closest'
    )

    return fig


def plot_histogram(df, title=None, xlabel=None, ylabel=None):
    """
    """

    df = df.sort_values('grade_').reset_index(drop=True)

    # Hover text
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: int(x[1:]) if type(x) == str else x)

    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + df.date_.apply(str) + '<br>' \
                 + 'Grade: ' + df.grade.apply(str) + '<br>' \
                 + 'Location: ' + df.location.apply(str) + '<br>' \
                 + 'Setter: ' + df.setter.apply(str) + '<br>' \
                 + 'Wall-type: ' + df.wall_type.apply(str) + '<br>' \
                 + 'Hold-type: ' + df.hold_type.apply(str) + '<br>' \
                 + 'Style: ' + df['style'].apply(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df.description.apply(str).apply(lambda x: word_wrap(str(x), 10)) + '<br>'

    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: 'V' + str(x) if type(x) == int else x)

    grades_hist = go.Bar(x=df.grade_, y=df.count_,
                         marker_color=df.color,
                         text=hover_text,
                         hovertemplate="Number of Recorded Sends: %{y}<br>"
                                       + "%{text}<br>"
                                       + "<extra></extra>")

    fig = go.Figure()
    fig.add_trace(grades_hist)

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'showgrid': False},
                      yaxis={'title': ylabel,
                             'showgrid': False})

    return fig


def plot_heatmap(df, title=None, xlabel=None, ylabel=None, column_list=None):
    """
    """

    # Clean column_list
    if df.columns[0] == 'year' and column_list is None:
        column_list = df[df.columns[0]].unique()
    elif df.columns[0] == 'year':
        column_list.sort()
    elif column_list is None:
        column_list = df[df.columns[0]].value_counts().index
    else:
        pass

    # Derive raw input data
    df = df[df[df.columns[0]].isin(column_list)].reset_index(drop=True)  # Filter
    df.description = df.description.apply(lambda x: word_wrap(str(x), 10))
    table_df = df.reset_index().pivot(index=df.columns[1], columns=df.columns[0], values="count_").fillna(0)  # Pivot
    table_df.index = table_df.index.map(lambda x: 'V' + str(x))  # Add V to Vgrades
    column_list = [item for item in column_list if item in table_df.columns]  # Filter out missing columns
    table_df = table_df[column_list]  # Organize columns

    # Hover text
    df[df.columns[1]] = df[df.columns[1]].apply(lambda x: int(x[1:]) if type(x) == str else x)

    grade_table = df.pivot(index="grade_", columns=df.columns[0], values="grade_") \
        .applymap(str).applymap(lambda x: x.replace('.0', '')) \
        .applymap(lambda x: 'V' + str(x)) \
        .applymap(lambda x: x.replace('Vnan', 'nan')) \
        .applymap(lambda x: float(x) if x == 'nan' else x)

    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + df.pivot(index="grade_", columns=df.columns[0], values="date_").applymap(str) + '<br>' \
                 + 'Grade: ' + grade_table + '<br>' \
                 + 'Location: ' + df.pivot(index="grade_", columns=df.columns[0], values="location").applymap(
        str) + '<br>' \
                 + 'Setter: ' + df.pivot(index="grade_", columns=df.columns[0], values="setter").applymap(str) + '<br>' \
                 + 'Wall-type: ' + df.pivot(index="grade_", columns=df.columns[0], values="wall_type").applymap(
        str) + '<br>' \
                 + 'Hold-type: ' + df.pivot(index="grade_", columns=df.columns[0], values="hold_type").applymap(
        str) + '<br>' \
                 + 'Style: ' + df.pivot(index="grade_", columns=df.columns[0], values="style").applymap(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df.pivot(index="grade_", columns=df.columns[0], values="description") + '<br>'

    hover_text.index = hover_text.index.map(lambda x: 'V' + str(x) if type(x) == int else x)
    df[df.columns[1]] = df[df.columns[1]].apply(lambda x: 'V' + str(x) if type(x) == int else x)

    # Heatmap
    heatmap = go.Heatmap(z=table_df,
                         x=table_df.columns,
                         y=table_df.index,
                         hoverinfo='text',
                         text=hover_text[list(table_df.columns)],
                         colorscale=warm)

    # Annotations
    annotations = []
    for i in range(len(df)):
        annotations.append(dict(x=df[df.columns[0]][i],
                                y=df[df.columns[1]][i],
                                text=str(df[df.columns[2]][i]),
                                showarrow=False))

    # Plot figure
    fig = go.Figure()
    fig.add_trace(heatmap)

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'showgrid': False,
                             'tickvals': table_df.columns,
                             'ticktext': table_df.columns},
                      yaxis={'title': ylabel,
                             'showgrid': False,
                             'tickvals': table_df.index,
                             'ticktext': table_df.index},
                      annotations=annotations)

    return fig
