import pandas as pd
from sqlalchemy import create_engine

# Crear la conexión a la base de datos
engine = create_engine('mysql+mysqlconnector://root:8399243Leav_@localhost/venadobdpredict')

# Obtener los datos de distribucion_venado de la base de datos
distribucion_data = pd.read_sql("SELECT d.fecha_distribucion_mensual, d.total_cantidad_distribucion, p.nombre_producto FROM distribucion_venado d JOIN productos_venado p ON d.producto_id = p.id", con=engine)
distribucion_data['fecha_distribucion_mensual'] = pd.to_datetime(distribucion_data['fecha_distribucion_mensual'])

# Obtener los datos de produccion_venado de la base de datos
produccion_data = pd.read_sql("SELECT p.fecha_produccion_mensual, p.cantidad_produccion, pr.nombre_producto FROM produccion_venado p JOIN productos_venado pr ON p.producto_id = pr.id", con=engine)
produccion_data['fecha_produccion_mensual'] = pd.to_datetime(produccion_data['fecha_produccion_mensual'])

# Fusionar las columnas de fecha en una sola columna
df = pd.DataFrame()
df['fecha'] = distribucion_data['fecha_distribucion_mensual'].combine_first(produccion_data['fecha_produccion_mensual'])
df['total_cantidad_distribucion'] = distribucion_data['total_cantidad_distribucion']
df['cantidad_produccion'] = produccion_data['cantidad_produccion']
df['nombre_producto'] = distribucion_data['nombre_producto'].combine_first(produccion_data['nombre_producto'])

# Establecer la frecuencia a 'MS'
df = df.set_index('fecha')
df = df.asfreq('MS')

# Verificar el DataFrame resultante
print(df.to_string())
