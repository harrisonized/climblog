"""
Note this file contains _NO_ flask functionality.
Instead, it isolates all the plotting functions so that main.py has less clutter.
"""
import json
import numpy as np
import pandas as pd
import pandas.io.sql as pd_sql
import pandasql as ps
import datetime as dt
import matplotlib.dates as mdates
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly



warm = [[0.0, "rgb(255,248,248)"],
        [0.2, "rgb(254,224,144)"],
        [0.4, "rgb(253,174,97)"],
        [0.6, "rgb(244,109,67)"],
        [0.8, "rgb(215,48,39)"],
        [1.0, "rgb(165,0,38)"]]



"""
Send Tracker
"""

def logistic_func(x, a, b, c, d):
    return a*np.log(b*x+c)+d

def plot_scatter(date_linspace, scatter_df, popt):
    fig = go.Figure()

    new_grades_scatter = go.Scatter(x=mdates.num2date(date_linspace),
                         y=logistic_func(date_linspace, *popt),
                         mode='lines',
                         line={'color':'lightgreen'},
                         hoverinfo='skip')

    all_records_scatter = go.Scatter(x=scatter_df.index,
                         y=scatter_df.grade_,
                         mode='markers', 
                         marker={'color':scatter_df.color},
                         name='grade')

    fig.add_trace(new_grades_scatter)
    fig.add_trace(all_records_scatter)

    fig.layout.update(
        title = go.layout.Title(text="Sends by Date"),
        xaxis = {'title_text': "Date",
                 'showgrid': True,
                 'range': None},
        yaxis = {'title_text': "Grade",
                 'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
                 'range': [5, 12]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
        
    return fig



"""
Heatmaps
"""

def plot_heatmap(df, table_df, xlabel=None, ylabel=None, title=None):
    data = go.Heatmap(z=table_df,
        x=table_df.columns,
        y=table_df.index,
        colorscale=warm)

    json_str = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    data = json.loads(json_str)

    annotations = []
    for i in range(len(df)):
        annotations.append(dict(x=df[df.columns[0]][i],
                                y=df[df.columns[1]][i],
                                text=str(df[df.columns[2]][i]),
                                showarrow=False))

    fig = go.Figure(data=data)

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis = {'title': xlabel,
                               'showgrid': False,
                               'tickvals': table_df.columns,
                               'ticktext': table_df.columns},
                      yaxis = {'title': ylabel,
                               'showgrid': False,
                               'tickvals': table_df.index,
                               'ticktext': table_df.index},
                      annotations=annotations)
    
    return fig

def convert_json(fig):
    json_str = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig_dict = json.loads(json_str)
    #fig_go = go.Figure(data = fig_dict['data'], layout = fig_dict['layout'])
    div = pyo.plot(fig_dict, output_type='div')
    return div


if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what empty string predicts")
    print('input string is ')
    chat_in = 'bob'
    pprint(chat_in)

    x_input, probs = make_prediction(chat_in)
    print(f'Input values: {x_input}')
    print('Output probabilities')
    pprint(probs)