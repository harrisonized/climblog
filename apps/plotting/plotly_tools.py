import random
import plotly.graph_objs as go
from apps.plotting.text_tools import word_wrap

# Objects included in this file:
# warm
# color_dict

# Functions included in this file:
# # word_wrap
# # plot_scatter
# # plot_histogram
# # plot_heatmap
# # labels_for_heatmap


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


def plot_scatter(df, x, y, color=None,
                 xlabel=None, ylabel=None, title=None,
                 hovertext=None, hovertemplate=None,
                 jitter=True, layout=True):
    """Generic plotting function
    """

    if jitter:
        df[y] = df[y].apply(lambda num: num - 0.15 + 0.3 * random.random())  # Jitter

    fig = go.Figure()

    scatter = go.Scatter(x=df[x],
                         y=df[y],
                         mode='markers',
                         marker={'color': df[color]} if color else None,
                         text=hovertext,
                         hovertemplate=hovertemplate)

    fig.add_trace(scatter)

    if layout:
        fig.layout.update(
            title=go.layout.Title(text=title),
            xaxis={'title_text': xlabel,
                   'showgrid': True,
                   'range': None},
            yaxis={'title_text': ylabel,
                   'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
                   'range': [df[y].min() - 0.5, df[y].max() + 0.5]},
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            hovermode='closest'
        )

    return fig


def plot_bar(df, x, y, color=None,
             xlabel=None, ylabel=None, title=None,
             hovertext=None, hovertemplate=None):
    """Generic plotting function
    """

    bar = go.Bar(x=df[x],
                 y=df[y],
                 marker_color=df[color] if color else None,
                 text=hovertext,
                 hovertemplate=hovertemplate)

    fig = go.Figure()
    fig.add_trace(bar)

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'showgrid': False},
                      yaxis={'title': ylabel,
                             'showgrid': False})

    return fig


def plot_heatmap(table_df,
                 xlabel=None, ylabel=None, title=None,
                 hovertext=None, annotations=None):
    """Generic plotting function
    """

    heatmap = go.Heatmap(z=table_df,
                         x=table_df.columns,
                         y=table_df.index,
                         hoverinfo='text',
                         text=hovertext[table_df.columns.to_list()],
                         colorscale=warm)

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
                             'ticktext': table_df.index})

    if annotations:
        fig.layout.update(annotations=annotations)

    return fig


def labels_for_heatmap(df, column_list=None):
    """Special function
    """

    # sort
    if df.columns[0] == 'year' and column_list is None:
        column_list = df[df.columns[0]].unique()
    elif df.columns[0] == 'year':
        column_list = column_list.sort()
    elif column_list is None:
        column_list = df[df.columns[0]].value_counts().index
    else:
        pass

    # derive raw input data
    df = df[df[df.columns[0]].isin(column_list)].reset_index(drop=True)  # Filter
    df.description = df.description.apply(lambda x: word_wrap(str(x), 10))

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

    # Annotations
    annotations = []
    for i in range(len(df)):
        annotations.append(dict(x=df[df.columns[0]][i],
                                y=df[df.columns[1]][i],
                                text=str(df[df.columns[2]][i]),
                                showarrow=False))

    return hover_text, annotations
