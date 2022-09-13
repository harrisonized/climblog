import os
import json
import random
import plotly
import plotly.graph_objs as go
from climblog.etc.colors import warm

# Functions
# # export_fig_to_json
# # plot_scatter
# # plot_histogram
# # plot_heatmap


def export_fig_to_json(fig, fig_dir='figures', filename='fig'):
    os.makedirs(f'{fig_dir}', exist_ok=True)
    with open(f'{fig_dir}/{filename}.json', 'w') as outfile:
        json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)


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
