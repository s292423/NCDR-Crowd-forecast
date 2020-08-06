import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from scipy import signal

app = dash.Dash()

df1 = pd.read_csv("A_area.csv", encoding='utf-8')
df1 = df1[['Total', 'Longitude', 'Latitude', 'TownID']]
df1 = df1.groupby(['TownID', 'Latitude', 'Longitude'])['Total'].sum()
df1 = df1.values.tolist()
df2 = pd.read_csv("H_area.csv", encoding='utf-8')
df2 = df2[['Total', 'Longitude', 'Latitude', 'TownID']]
df2 = df2.groupby(['TownID', 'Latitude', 'Longitude'])['Total'].sum()
df2 = df2.values.tolist()
df3 = pd.read_csv("G_area.csv", encoding='utf-8')
df3 = df3[['Total', 'Longitude', 'Latitude', 'TownID']]
df3 = df3.groupby(['TownID', 'Latitude', 'Longitude'])['Total'].sum()
df3 = df3.values.tolist()
df4 = pd.read_csv("F_area.csv", encoding='utf-8')
df4 = df4[['Total', 'Longitude', 'Latitude', 'TownID']]
df4 = df4.groupby(['TownID', 'Latitude', 'Longitude'])['Total'].sum()
df4 = df4.values.tolist()
df5 = pd.read_csv("C_area.csv", encoding='utf-8')
df5 = df5[['Total', 'Longitude', 'Latitude', 'TownID']]
df5 = df5.groupby(['TownID', 'Latitude', 'Longitude'])['Total'].sum()
df5 = df5.values.tolist()


app.layout = html.Div([
    dcc.Dropdown(
        id='choose',
        options=[
            {'label': '平均數', 'value': 'M'},
            {'label': '標準化', 'value': 'S'},
        ],
        value='M',
        # style={"width": "50vh", "padding-left": "150px"},
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': '台北市', 'value': 'A'},
            {'label': '新北市', 'value': 'F'},
            {'label': '桃園市', 'value': 'H'},
            {'label': '宜蘭市', 'value': 'G'},
            {'label': '基隆市', 'value': 'C'},
        ],
        value='A',
        # style={"width": "50vh", "padding-left": "150px"},
    ),
    html.Div(style={"height": "5vh"}),
    dcc.Slider(
        id='slider',
        min=1,
        max=12,
        value=1,
        marks={
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
        },
    ),
    html.Div(style={"height": "10vh"}),
    html.H1('city heatmaps'),
    dcc.Graph(
        id='gapminder',
        style={"height": "80vh", "width": "50%"},
    ),
    html.H1('city convolution'),
    dcc.Graph(
        id='cnn',
        style={"height": "80vh", "width": "50%"},
    ),
    html.H1('city box'),
    dcc.Graph(
        id='box',
        style={"height": "80vh", "width": "100%"},
        figure={
            'data': [
                go.Box(
                    y=df1,
                    name="台北市",
                    boxpoints='outliers',
                    marker=dict(
                        color='rgba(93, 164, 214, 0.5)',
                    ),
                    line=dict(
                        width=1,
                        color='rgba(93, 164, 214, 0.5)',
                    ),
                ),
                go.Box(
                    y=df2,
                    name="桃園市",
                    boxpoints='outliers',
                    marker=dict(
                        color='rgba(255, 144, 14, 0.5)',
                    ),
                    line=dict(
                        width=1,
                        color='rgba(255, 144, 14, 0.5)',
                    ),
                ),
                go.Box(
                    y=df3,
                    name="宜蘭市",
                    boxpoints='outliers',
                    marker=dict(
                        color='rgba(44, 160, 101, 0.5)',
                    ),
                    line=dict(
                        width=1,
                        color='rgba(44, 160, 101, 0.5)',
                    ),
                ),
                go.Box(
                    y=df4,
                    name="新北市",
                    boxpoints='outliers',
                    marker=dict(
                        color='rgba(255, 65, 54, 0.5)',
                    ),
                    line=dict(
                        width=1,
                        color='rgba(255, 65, 54, 0.5)',
                    ),
                ),
                go.Box(
                    y=df5,
                    name="基隆市",
                    boxpoints='outliers',
                    marker=dict(
                        color='rgba(207, 114, 255, 0.5)'),
                    line=dict(
                        width=1,
                        color='rgba(207, 114, 255, 0.5)'),
                ),
            ]
        }
    ),
])

@app.callback(
    [dash.dependencies.Output('gapminder', 'figure'), dash.dependencies.Output('cnn', 'figure')],
    [dash.dependencies.Input('choose', 'value'), dash.dependencies.Input('slider', 'value'), dash.dependencies.Input('dropdown', 'value')])

def update_figure(selected_choose, selected_year, selected_continent):
    if selected_choose == 'M':
        if selected_year < 10:
            df = pd.read_csv('./output/20180' + str(selected_year) + '.csv')
            A_area = df.loc[df['TownID'].str.contains(selected_continent)].reset_index(drop=True)
            A_area = A_area[['Time', 'TownID', 'Longitude', 'Latitude', 'Total']]
            lats = sorted(A_area['Latitude'].unique().tolist())
            lngs = sorted(A_area['Longitude'].unique().tolist())
            z = []
            for i in lats:
                z_inside = []
                for j in lngs:
                    con1 = A_area['Latitude'] == i
                    con2 = A_area['Longitude'] == j
                    if A_area[con1 & con2].empty:
                        z_inside.append(0)
                    else:
                        z_inside.append(A_area[con1 & con2]['Total'].mean())
                z.append(z_inside)
        else:
            df = pd.read_csv('./output/2018' + str(selected_year) + '.csv')
            A_area = df.loc[df['TownID'].str.contains(selected_continent)].reset_index(drop=True)
            A_area = A_area[['Time', 'TownID', 'Longitude', 'Latitude', 'Total']]
            lats = sorted(A_area['Latitude'].unique().tolist())
            lngs = sorted(A_area['Longitude'].unique().tolist())
            z = []
            for i in lats:
                z_inside = []
                for j in lngs:
                    con1 = A_area['Latitude'] == i
                    con2 = A_area['Longitude'] == j
                    if A_area[con1 & con2].empty:
                        z_inside.append(0)
                    else:
                        z_inside.append(A_area[con1 & con2]['Total'].mean())
                z.append(z_inside)
        nn = np.array(z)
        w_k = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1], ],
                       dtype='float')
        f = signal.convolve2d(nn, w_k, 'valid')
        n = f.tolist()
    else:
        if selected_year < 10:
            df = pd.read_csv('./output/20180' + str(selected_year) + '.csv')
            A_area = df.loc[df['TownID'].str.contains(selected_continent)].reset_index(drop=True)
            A_area = A_area[['Time', 'TownID', 'Longitude', 'Latitude', 'Total']]
            lats = sorted(A_area['Latitude'].unique().tolist())
            lngs = sorted(A_area['Longitude'].unique().tolist())
            z = []
            for i in lats:
                z_inside = []
                for j in lngs:
                    con1 = A_area['Latitude'] == i
                    con2 = A_area['Longitude'] == j
                    if A_area[con1 & con2].empty:
                        z_inside.append(0)
                    else:
                        z_inside.append(A_area[con1 & con2]['Total'].std())
                z.append(z_inside)
        else:
            df = pd.read_csv('./output/2018' + str(selected_year) + '.csv')
            A_area = df.loc[df['TownID'].str.contains(selected_continent)].reset_index(drop=True)
            A_area = A_area[['Time', 'TownID', 'Longitude', 'Latitude', 'Total']]
            lats = sorted(A_area['Latitude'].unique().tolist())
            lngs = sorted(A_area['Longitude'].unique().tolist())
            z = []
            for i in lats:
                z_inside = []
                for j in lngs:
                    con1 = A_area['Latitude'] == i
                    con2 = A_area['Longitude'] == j
                    if A_area[con1 & con2].empty:
                        z_inside.append(0)
                    else:
                        z_inside.append(A_area[con1 & con2]['Total'].std())
                z.append(z_inside)
        nn = np.array(z)
        w_k = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1], ],
                       dtype='float')
        f = signal.convolve2d(nn, w_k, 'valid')
        n = f.tolist()

    return {
        'data': [
            go.Heatmap(
                z=z,
                x=lngs,
                y=lats,
                colorscale='Viridis',
            )
        ]
    }, {
        'data': [
            go.Heatmap(
                z=n,
                x=[i for i in range(f.shape[0])],
                y=[i for i in range(f.shape[1])],
                colorscale='Viridis',
            )
        ]
    }

if __name__ == '__main__':
    app.run_server(debug=True)