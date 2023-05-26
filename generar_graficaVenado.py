import pandas as pd
import plotly.graph_objects as go

# Cargar el archivo CSV utilizando Pandas
df = pd.read_csv('produccionketchupmensual.csv')

# Obtener las columnas de cantidad producida y cantidad distribuida
cantidad_producida = df['cantidad producida']
cantidad_distribuida = df['cantidad distribuida']

# Crear la figura de la gráfica comparativa utilizando Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Fecha mensual produccion'], y=cantidad_producida, name='Cantidad Producida'))
fig.add_trace(go.Scatter(x=df['Fecha mensual produccion'], y=cantidad_distribuida, name='Cantidad Distribuida'))

# Personalizar el diseño de la gráfica
fig.update_layout(
    title='Comparativa de Cantidad Producida y Distribuida',
    xaxis_title='Fecha mensual produccion',
    yaxis_title='Cantidad',
    legend=dict(x=0.5, y=1.1)
)

# Guardar la gráfica como archivo HTML
fig.write_html('chart.html')
