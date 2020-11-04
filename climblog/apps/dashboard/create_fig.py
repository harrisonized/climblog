import numpy as np
import matplotlib.dates as mdates
import plotly.graph_objs as go
from .plotting.plotly import plot_scatter, plot_bar, plot_heatmap
from .formatting.text_tools import word_wrap
from .math.curve_fit import logistic_func


# Functions included in this file:
# # hovertext_for_heatmap
# # create_sends_by_date_scatter
# # create_grades_histogram
# # create_grades_by_year_heatmap
# # create_grades_by_wall_heatmap
# # create_grades_by_hold_heatmap
# # create_grades_by_style_heatmap





def hovertext_for_heatmap(df, column_list=None):
    
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

    grade_table = df.pivot(index="grade_", columns=df.columns[1], values="grade_") \
        .applymap(str).applymap(lambda x: x.replace('.0', '')) \
        .applymap(lambda x: 'V' + str(x)) \
        .applymap(lambda x: x.replace('Vnan', 'nan')) \
        .applymap(lambda x: float(x) if x == 'nan' else x)

    hover_text = 'FIRST RECORDED SEND<br>' \
                 + 'Date: ' + df.pivot(index="grade_", columns=df.columns[1], values="date_").applymap(str) + '<br>' \
                 + 'Grade: ' + grade_table + '<br>' \
                 + 'Location: ' + df.pivot(index="grade_", columns=df.columns[1], values="location").applymap(str) + '<br>' \
                 + 'Setter: ' + df.pivot(index="grade_", columns=df.columns[1], values="setter").applymap(str) + '<br>' \
                 + 'Wall-type: ' + df.pivot(index="grade_", columns=df.columns[1], values="wall_type").applymap(str) + '<br>' \
                 + 'Hold-type: ' + df.pivot(index="grade_", columns=df.columns[1], values="hold_type").applymap(str) + '<br>' \
                 + 'Style: ' + df.pivot(index="grade_", columns=df.columns[1], values="style").applymap(str) + '<br>' \
                 + 'Description: ' + '<br>' \
                 + df.pivot(index="grade_", columns=df.columns[1], values="description") + '<br>'

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


def create_sends_by_date_scatter(scatter_df, logistic_params):

    # plot main figure
    hover_text = 'Grade: ' + scatter_df['vgrade'].apply(str) + '<br>' \
                 + 'Location: ' + scatter_df['location'].apply(str) + '<br>' \
                 + 'Setter: ' + scatter_df['setter'].apply(str) + '<br>' \
                 + 'Wall-type: ' + scatter_df['wall_type'].apply(str) + '<br>' \
                 + 'Hold-type: ' + scatter_df['hold_type'].apply(str) + '<br>' \
                 + 'Style: ' + scatter_df['style'].apply(str) + '<br>' \
                 + 'Description:<br>' +scatter_df['description'].apply(lambda x: word_wrap(str(x), 10)) + '<br>'
    hover_template = "Date: %{x}<br>%{text}<br><extra></extra>"

    fig = plot_scatter(scatter_df, x="date_", y="grade_", color='color',
                       xlabel="Date", ylabel="Grade", title="Sends by Date",
                       hovertext=hover_text, hovertemplate=hover_template)

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


def create_grades_histogram(grades_histogram_df):
    """df should look like the following:
    """

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

    return fig


def create_grades_by_year_heatmap(year_table_df, year_df):

    # plot main figure
    hover_text, annotations = hovertext_for_heatmap(year_df)
    fig = plot_heatmap(year_table_df,
                       xlabel="Year", ylabel="Grade", title="Heatmap of Grades by Year",
                       hovertext=hover_text, annotations=annotations)

    return fig


def create_grades_by_wall_heatmap(wall_table_df, wall_df):

    # plot main figure
    columns = ['cave', 'overhang', 'face', 'arete', 'slab', 'corner', 'variable']
    hover_text, annotations = hovertext_for_heatmap(wall_df, columns)
    fig = plot_heatmap(wall_table_df,
                       xlabel="Wall-type", ylabel="Grade", title="Heatmap of Grades by Wall-type",
                       hovertext=hover_text, annotations=annotations)

    return fig


def create_grades_by_hold_heatmap(hold_table_df, hold_df):

    # plot main figure
    columns = ['jug', 'crimp', 'sloper', 'pinch']
    hover_text, annotations = hovertext_for_heatmap(hold_df, columns)
    fig = plot_heatmap(hold_table_df,
                       xlabel="Hold-type", ylabel="Grade", title="Heatmap of Grades by Hold-type",
                       hovertext=hover_text, annotations=annotations)

    return fig


def create_grades_by_style_heatmap(style_table_df, style_df):

    # plot main figure
    columns = ['mantle', 'natural', 'dyno', 'comp']
    hover_text, annotations = hovertext_for_heatmap(style_df, columns)
    fig = plot_heatmap(style_table_df,
                       xlabel="Style", ylabel="Grade", title="Heatmap of Grades by Style",
                       hovertext=hover_text, annotations=annotations)

    return fig
