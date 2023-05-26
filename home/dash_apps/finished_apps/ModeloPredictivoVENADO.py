import pandas as pd
import numpy as np
import pickle

# Cargar el modelo
with open('modelopredictivocantidadprodvenado.pkl', 'rb') as f:
    model = pickle.load(f)


# Función para hacer predicciones
def hacer_prediccion(datos):
    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(datos, index=[0])

    # Hacer la predicción
    prediccion = model.predict(df)[0]

    # Redondear la predicción y convertirla a entero
    prediccion = round(prediccion)
    prediccion = int(prediccion)

    # Devolver la predicción
    return prediccion
