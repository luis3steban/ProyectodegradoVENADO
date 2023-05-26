from django.shortcuts import render
import pandas as pd
import numpy as np
from django.shortcuts import render
from django_plotly_dash import DjangoDash
import pickle
from django.conf import settings
import csv
import pdfkit
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from io import BytesIO
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import base64
from django.template.loader import render_to_string
from django.conf import settings
from home.dash_apps.finished_apps import simpleexample
# Create your views here.
def home(requests):
    return render(requests, 'home/login.html')
def dash_modal_view(request):
    return render(request, 'modal_template.html')

def marcas(requests):
    return render(requests, 'home/Marcas.html')

def dashboard(requests):
    return render(requests, 'home/dashboard.html')

def prediccion(requests):
    return render(requests, 'home/bienvenido.html')

def contraseñaolvidada(requests):
    return render(requests, 'home/forgot-password.html')

def registrarAcc(requests):
    return render(requests, 'home/register.html')

# Ruta para la vista de formulario de predicción
def prediction_form(request):
    return render(request, 'base.html')
def generate_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def modelo_prediccion(request):
    if request.method == 'POST':
        try:
            # Cargar datos de producción y convertir el índice a fechas mensuales
            df = pd.read_csv('produccionketchupmensual.csv', parse_dates=['Fecha mensual produccion'],
                             index_col='Fecha mensual produccion')
            df.index.freq = 'MS'

            # Dividir los datos en conjunto de entrenamiento y validación
            train_size = int(len(df) * 0.8)
            train_data = df['cantidad producida'][:train_size]
            test_data = df['cantidad producida'][train_size:]

            # Obtener los datos exógenos para el conjunto de prueba
            exog_test_data = df['cantidad distribuida'][train_size:train_size + len(test_data)].values.reshape(-1, 1)

            # Modelar la serie con SARIMAX y optimizar los parámetros
            best_rmse = float('inf')
            best_model = None
            best_end_date = None
            best_product_name = None

            for p in range(3):
                for d in range(2):
                    for q in range(3):
                        for P in range(2):
                            for D in range(2):
                                for Q in range(2):
                                    try:
                                        modelo = SARIMAX(train_data, order=(p, d, q), seasonal_order=(P, D, Q, 12),
                                                         enforce_stationarity=False, enforce_invertibility=False)
                                        modelo_ajustado = modelo.fit()
                                        predicciones = modelo_ajustado.predict(start='2022-06-01',
                                                                               end='2023-05-01',
                                                                               exog=exog_test_data, dynamic=False)
                                        rmse = np.sqrt(np.mean((predicciones - test_data) ** 2))
                                        if rmse < best_rmse:
                                            best_rmse = rmse
                                            best_model = modelo_ajustado
                                            best_end_date = predicciones.index[-1]
                                            best_product_name = df['nombre producto'].iloc[-1]
                                    except:
                                        continue
            # Ver el resumen del mejor modelo
            summary = best_model.summary()

            # Obtener las fechas de inicio y fin para las predicciones
            start_date = '2022-06-01'
            end_date = '2023-06-01'

            # Hacer predicciones en el conjunto de validación usando el mejor modelo
            predicciones = best_model.predict(start=start_date, end=end_date, exog=exog_test_data, dynamic=False)

            # Calcular el error de las predicciones usando el mejor modelo
            error = np.sqrt(np.mean((predicciones - test_data) ** 2))

            # Obtener la última predicción y el nombre del producto
            produccion_adecuada = int(predicciones[-1])
            nombre_producto = best_product_name

            # Graficar los resultados de las predicciones
            plt.figure(figsize=(12, 6))
            # Obtener los índices de los datos de entrenamiento y validación
            train_indices = train_data.index
            test_indices = test_data.index
            # Obtener los valores correspondientes a los índices
            train_values = train_data.values
            test_values = test_data.values
            plt.plot(train_indices, train_values, label='Datos de entrenamiento')
            plt.plot(test_indices, test_values, label='Datos de validación')
            plt.plot(predicciones.index, predicciones, label='Predicciones')
            plt.title('Producción de Salsa Ketchup KRIS - Predicciones', fontsize=20)
            plt.xlabel('Fecha mensual producción')
            plt.ylabel('Producción unidades')
            plt.legend()
            plt.savefig('predicciones.png')

            import base64

            # Leer la imagen generada
            with open('predicciones.png', 'rb') as f:
                image_data = f.read()

            # Codificar la imagen en base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            # Renderizar la plantilla de resultados con los datos
            context = {
                'summary': summary,
                'predicciones': zip(predicciones.index.strftime('%Y-%m-%d'), predicciones),
                'error': error,
                'produccion_adecuada': produccion_adecuada,
                'nombre_producto': nombre_producto,
                'grafica_encoded': encoded_image
            }
            template = get_template('prediction.html')
            html = template.render(context)
            pdf = generate_pdf(html)

            if pdf is not None:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="prediction_results.pdf"'
                return response

            return render(request, 'prediction.html', context)

        except Exception as e:
            error_message = f"Se produjo un error: {str(e)}"
            context = {'error_message': error_message}
        return render(request, 'prediction_form.html', context)
    else:
        return render(request, 'prediction_form.html')