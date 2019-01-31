import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go

df = pd.read_excel('/home/pushkar/Documents/Projects/mosp_national_accounts/Datasets/S1_5r.xlsx')

df = df.iloc[4:,:]

economic_activities = list()

i=2
try:
    while not df.iloc[i,-1] is np.nan:
        activity = df.iloc[i,-1].strip(' ')
        economic_activities.append(activity)
        i=i+12
except:
    pass  

listofDict = [] 

for i in economic_activities:
    ecodict = {
        'label':str(i),
        'value':str(i)
    }
    listofDict.append(ecodict)

# Columns for values at current prices
column1 = df.iloc[0,2:7].values
column1 = np.insert(column1, 0, 'Parameters')
column_1 = [column1[0]]
i=1
while i<len(column1):
    temp1 = column1[i]
    temp2 = temp1[:2]+temp1[-2:]
    i=i+1
    column_1.append(temp2)
    
# Columns for values at constant prices
column2 = df.iloc[0,8:13].values
column2 = np.insert(column2, 0, 'Parameters')
column_2 = [column1[0]]
i=1
while i<len(column2):
    temp1 = column1[i]
    temp2 = temp1[:2]+temp1[-2:]
    i=i+1
    column_2.append(temp2)

dataframes_collection_at_current_price = {}

loop = len(economic_activities)
k=3
e=0
while loop:
    temp_df = pd.DataFrame()
    for i in range(11):
        row = np.insert(df.iloc[i+k,2:7].values, 0, df.iloc[i+k,-1])
        temp_df = temp_df.append(pd.Series(row), ignore_index=True)
    k = k+12
    temp_df.columns = column_1
    dataframes_collection_at_current_price[economic_activities[e]]=temp_df
    e=e+1
    loop = loop-1

dataframes_collection_at_constant_price = {}

loop = len(economic_activities)
k=3
e=0
while loop:
    temp_df = pd.DataFrame()
    for i in range(11):
        row = np.insert(df.iloc[i+k,8:13].values, 0, df.iloc[i+k,-1])
        temp_df = temp_df.append(pd.Series(row), ignore_index=True)
    k = k+12
    temp_df.columns = column_1
    dataframes_collection_at_constant_price[economic_activities[e]]=temp_df
    e=e+1
    loop = loop-1

external_stylesheets = ['stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(style = {'backgroundColor':'#111111', 'color':'#7FDBFF', }, children = [
        html.H1(children='National Accounts Dashboard',
        style = {
            'textAlign':'center',
        }
        ),

        html.Div(children='''
            Dashboard for analyzing National Accounts data
        ''',
        style = {
            'textAlign':'center',
            'padding':20
        }
        )
    ]),

    dcc.Dropdown(
        id = 'economic_activity',
        options=listofDict,
        multi=False,
        placeholder = economic_activities[0]
    ),

    dcc.Graph(id='graphs_at_current_price'),
    
    dcc.Graph(id='graphs_at_constant_price')

])

@app.callback(
    dash.dependencies.Output('graphs_at_current_price', 'figure'),
    [dash.dependencies.Input('economic_activity', 'value')])
def plot_graphs_current(act):
    current_df = dataframes_collection_at_current_price[act]
    traces = []
    for i in range(11):
        traces.append(go.Scatter(
              y=current_df.iloc[i,1:].values,
              x=current_df.columns[1:],
              name = current_df['Parameters'][i]))

    return {
        'data': traces
    }

@app.callback(
    dash.dependencies.Output('graphs_at_constant_price', 'figure'),
    [dash.dependencies.Input('economic_activity', 'value')])
def plot_graphs_constant(act):
    current_df = dataframes_collection_at_constant_price[act]
    traces = []
    for i in range(11):
        traces.append(go.Scatter(
              y=current_df.iloc[i,1:].values,
              x=current_df.columns[1:],
              name = current_df['Parameters'][i]))

    return {
        'data': traces
    }

if __name__ == '__main__':
    app.run_server(debug=True)