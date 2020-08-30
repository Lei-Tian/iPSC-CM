#import chart_studio.plotly as py
import plotly.graph_objs as go
#import plotly.figure_factory as ff
#import plotly.offline as offline
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# read in data from csv file
df = pd.read_csv('ipsccm_fetus_adult_LV.txt.gz',sep="\t")

#df = df.T.iloc[::-1] 		# transform and reverse rows (to get caps in right order for heat map)
#df = df.T 							# and then transform it back again.

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Change the title of the page from the default "Dash"
app.title = "Application heatmap"

left_margin = 100
right_margin = 50

app.layout = html.Div([

	html.H2(
        children='bulk RNA-seq of iPSC-CMs (day 0-90), fetal and adult heart LV',
        style={
            'textAlign': 'center'
        }
    ),
	html.H4("Reference: Churko et al, Nature Communications 2018"),
    html.H4("Article Link: https://www.nature.com/articles/s41467-018-07333-4"),
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df.index],
        multi=True,
        id='Gene name'
    ),
    dcc.Graph(id='heatmap_output')
])

@app.callback(
	Output('heatmap_output', 'figure'),
	[Input('Gene name', 'value')])
def update_figure(value):
    if value is None:
        return {'data': []}
    else:
        dff = df.loc[value,:]
        scaled_size = 100 + 100 + 25*len(value)
        return {
            'data': [{
                'z': dff.values.tolist(),
                'x': dff.columns.tolist(),
                'y': dff.index.tolist(),
                'ygap': 2,
                'reversescale': 'true',
                'colorscale': 'Viridis',
                'type': 'heatmap',
            }],
            'layout': {
                'title': 'VST normalized expression',
                'height': scaled_size,
                'width': 1500,
                'xaxis': {'side':'top'},
                'margin': {
                	'l': left_margin,
                	'r': right_margin,
                	'b': 0,
                	't': 200
                }
            }
        }


if __name__ == '__main__':
    app.run_server(debug=True)
