import dash
from SimpleExample import views
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash

#cargando el dataset
produccionvenaddo = pd.read_csv('produccionketchupmensual.csv')
#creamos dashapp
app = DjangoDash('SimpleExample')
app2 = DjangoDash('SimpleExample2')
app3 = DjangoDash('SimpleExample3')
app4 = DjangoDash('SimpleExample4')
app5 = DjangoDash('SimpleExample5')
app6 = DjangoDash('SimpleExample6')
app7 = DjangoDash('SimpleExample7')


app.layout = html.Div(children=[
    dcc.Dropdown(
        id='geo-dropdown',
        options=[{'label': i, 'value': i} for i in produccionvenaddo['nombre producto'].unique()],
        value='SALSAS KETCHUP'
    ),
    dcc.Graph(id='price-graph')
])

@app.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filtered_data = produccionvenaddo[produccionvenaddo['nombre producto'] == selected_geography]
    fig = px.line(filtered_data, x='Fecha produccion', y=['cantidad producida', 'cantidad distribuida'],
                  title=f'Comparación de Cantidad Producida y Distribuida - {selected_geography}')

    return fig

app2.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='AVENA INSTANTANEA'),
   dcc.Graph(id='price-graph')
   ])

@app2.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig
app3.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='GELATINA SIN SABOR'),
   dcc.Graph(id='price-graph')
   ])

@app3.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig
app4.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='DURAZNOS ENLATADOS'),
   dcc.Graph(id='price-graph')
   ])

@app4.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig
app5.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='SALSAS MAYONESA'),
   dcc.Graph(id='price-graph')
   ])

@app5.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig
app6.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='POLVO DE HORNEAR'),
   dcc.Graph(id='price-graph')
   ])

@app6.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig
app7.layout = html.Div(children=[
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i,'value': i}
                          for i in produccionvenaddo ['producto'].unique()],
                value='CEREAL AZUCARADITAS'),
   dcc.Graph(id='price-graph')
   ])

@app7.callback(
               Output(component_id='price-graph', component_property= 'figure'),
              [Input(component_id='geo-dropdown', component_property='value')])
def update_graph(selected_geography):
    filterd_avocado = produccionvenaddo[produccionvenaddo['producto']== selected_geography]
    line_fig=px.line(filterd_avocado,
                     x='Fecha produccion',y='cantidad produccion - miles',
                     color='Tipo',
                     title=f'Grafica produccion - {selected_geography}')
    return line_fig

