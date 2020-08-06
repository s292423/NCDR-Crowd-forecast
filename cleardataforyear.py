import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': '台北市', 'value': 'A'},
            {'label': '新北市', 'value': 'B'},
            {'label': '桃園市', 'value': 'C'},
            {'label': '宜蘭市', 'value': 'D'},
            {'label': '基隆市', 'value': 'E'},
        ],
    ),
    html.Label('Slider'),
    dcc.Slider(
        min=1,
        max=12,
        marks={i: '{}'.format(i) for i in range(1, 13)},
    ),
], style={'columnCount': 1})

if __name__ == '__main__':
    app.run_server(debug=True)