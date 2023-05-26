import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash

#cargando el dataset
produccionketchupvenado = pd.read_csv('produccionketchupmensual.csv')
produccionmayonesavenado = pd.read_csv('produccionmayonesamensual.csv')
produccionmostazavenado = pd.read_csv('produccionmayonesamensual.csv')
# Grafica comp - graph Salsa kris ketchup
app = DjangoDash('SimpleExample')
app2 = DjangoDash('SimpleExample2')

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': i, 'value': i} for i in produccionketchupvenado['nombre producto'].unique()],
        value=' KRIS KETCHUP'
    ),
    dcc.Graph(id='comparison-graph')
])

@app.callback(
    Output(component_id='comparison-graph', component_property='figure'),
    [Input(component_id='product-dropdown', component_property='value')]
)
def update_graph(selected_product):
    filtered_data = produccionketchupvenado[produccionketchupvenado['nombre producto'] == selected_product]

    fig = px.line(filtered_data, x='Fecha mensual produccion', y=['cantidad producida', 'cantidad distribuida'],
                  title=f'Comparación de Cantidad Producida y Distribuida - {selected_product}')
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Cantidad unidad producto'
    )

    return fig

# Grafica comp - graph Salsa kris mayonesa
app2.layout = html.Div(children=[
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': i, 'value': i} for i in produccionmayonesavenado['nombre producto'].unique()],
        value='KRIS MAYONESA'
    ),
    dcc.Graph(id='comparison-graph')
])

@app2.callback(
    Output(component_id='comparison-graph', component_property='figure'),
    [Input(component_id='product-dropdown', component_property='value')]
)
def update_graph(selected_product):
    filtered_data = produccionmayonesavenado[produccionmayonesavenado['nombre producto'] == selected_product]

    fig = px.line(filtered_data, x='Fecha produccion mensual', y=['cantidad producida', 'cantidad distribuida'],
                  title=f'Comparación de Cantidad Producida y Distribuida - {selected_product}')
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Cantidad unidad producto'
    )
    return fig

# Grafica comp - graph Salsa kris mostaza
app2.layout = html.Div(children=[
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': i, 'value': i} for i in produccionmayonesavenado['nombre producto'].unique()],
        value='KRIS MAYONESA'
    ),
    dcc.Graph(id='comparison-graph')
])

@app2.callback(
    Output(component_id='comparison-graph', component_property='figure'),
    [Input(component_id='product-dropdown', component_property='value')]
)
def update_graph(selected_product):
    filtered_data = produccionmayonesavenado[produccionmayonesavenado['nombre producto'] == selected_product]

    fig = px.line(filtered_data, x='Fecha produccion mensual', y=['cantidad producida', 'cantidad distribuida'],
                  title=f'Comparación de Cantidad Producida y Distribuida - {selected_product}')
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Cantidad unidad producto'
    )
    return fig
