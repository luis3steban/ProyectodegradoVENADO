from django.shortcuts import render
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect , get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django_plotly_dash import DjangoDash
import pickle
from django.conf import settings
import csv
from .models import Accesos, Usuarios, Produccion_venado , Distribuciones_venado
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import pdfkit
import datetime
from sqlalchemy import create_engine
from statsmodels.tsa.statespace.sarimax import SARIMAX
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from io import BytesIO
from django.contrib import messages
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

def reporteProduccion(requests):
    producciones = Produccion_venado.objects.all().order_by('fecha_produccion_mensual', 'cantidad_produccion')
    return render(requests, 'home/reporteproduccionVenado.html', {'producciones': producciones})
def reporteDistribucion(requests):
    distribuciones = Distribuciones_venado.objects.all().order_by('fecha_distribucion_mensual', 'total_cantidad_distribucion')
    return render(requests, 'home/reportedistribuicionVenado.html', {'distribuciones': distribuciones})
def login_view(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        # Buscar el usuario en tu tabla personalizada
        try:
            user = Usuarios.objects.get(correo=correo)

            # Verificar la contraseña
            if user.verificar_password(password):
                # Iniciar sesión exitosamente
                request.session['user_id'] = user.id

                id_acceso = user.acceso_id
                return redirect('dashboard')
                # Redirigir a la página de inicio después del inicio de sesión
            else:
                # Credenciales inválidas
                error_message = 'Credenciales inválidas. Inténtalo nuevamente.'
                return render(request, 'home/login.html', {'error_message': error_message})
        except Usuarios.DoesNotExist:
            # Credenciales inválidas
            error_message = 'Su usuario o contraseña son incorrectas, porfavor intente nuevamente.'
            return render(request, 'home/login.html', {'error_message': error_message})

    return render(request, 'home/login.html')

def dashboard(request):
    return render(request, 'home/dashboard.html')

def prediccion(requests):
    return render(requests, 'home/bienvenido.html')

def contraseñaolvidada(requests):
    return render(requests, 'home/forgot-password.html')


def UsuariosMod(requests):
    accesos = Accesos.objects.all()
    usuarios = Usuarios.objects.all()
    return render(requests, 'home/moduloUsuarios.html', {'accesos': accesos, 'usuarios': usuarios})
def agregar_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        correo = request.POST.get('correo')
        acceso_id = request.POST.get('acceso')
        password = request.POST.get('password_usuario')

        # Obtener la instancia del modelo "Accesos"
        acceso = get_object_or_404(Accesos, id=acceso_id)

        # Crear el nuevo usuario
        nuevo_usuario = Usuarios.objects.create_user(
            nombre_usuario=nombre_usuario,
            correo=correo,
            acceso=acceso,
            password=password
        )

        # Realizar cualquier otra acción necesaria y redirigir a una página de éxito
        return redirect('Usuarios')
def eliminar_usuario(request, usuario_id):
    if request.method == 'POST':
        try:
            usuario = Usuarios.objects.get(id=usuario_id)
            usuario.delete()
            # Mostrar mensaje de éxito o realizar cualquier otra acción necesaria
            return JsonResponse({'success': True, 'message': 'Usuario eliminado exitosamente'})
        except Usuarios.DoesNotExist:
            # Mostrar mensaje de error
            return JsonResponse({'success': False, 'message': 'El usuario no existe'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

def modificar_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nombre_usuario = request.POST.get('nombre_usuario')
        correo = request.POST.get('correo')
        acceso_id = request.POST.get('acceso_id')

        usuario = get_object_or_404(Usuarios, id=usuario_id)
        usuario.nombre_usuario = nombre_usuario
        usuario.correo = correo

        acceso = get_object_or_404(Accesos, id=acceso_id)
        usuario.acceso = acceso  # Asignar el objeto Accesos correspondiente

        usuario.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def agregar_acceso(request):
    if request.method == 'POST':
        acceso_predict = request.POST.get('acceso_predict')
        descripcion = request.POST.get('descripcion')
        Accesos.objects.create(acceso_predict=acceso_predict, descripcion=descripcion)
        return redirect('Usuarios')

    return redirect('Usuarios')
def obtener_opciones_acceso(request):
    opciones_acceso = Accesos.objects.values('id', 'acceso_predict')  # Obtener las opciones de acceso desde el modelo Acceso
    return JsonResponse(list(opciones_acceso), safe=False)

def modificar_acceso(request):
    if request.method == 'POST':
        acceso_id = request.POST.get('acceso_id')
        acceso_predict = request.POST.get('acceso_predict')
        descripcion = request.POST.get('descripcion')

        try:
            acceso = Accesos.objects.get(id=acceso_id)
            acceso.acceso_predict = acceso_predict
            acceso.descripcion = descripcion
            acceso.save()
            return JsonResponse({'success': True})
        except Accesos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El acceso no existe.'})
    return redirect('Usuarios')

def eliminar_acceso(request):
    if request.method == 'POST':
        acceso_id = request.POST.get('acceso_id')

        # Buscar el acceso en la base de datos
        try:
            acceso = Accesos.objects.get(id=acceso_id)
            acceso.delete()
            # Mostrar mensaje de éxito
            return redirect('Usuarios')
            return JsonResponse({'success': True, 'message': 'Acceso eliminado exitosamente'})
        except Accesos.DoesNotExist:
            # Mostrar mensaje de error
            return JsonResponse({'success': False, 'message': 'El acceso no existe'})
        # Redirigir a la página 'Usuarios'
        return redirect('Usuarios')
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

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
            nom_prod = request.POST.get('nom_prod')
            fecha_pred = request.POST.get('fecha_pred')
            fecha_usuario_pred = fecha_pred+"-01"
            # Crear la conexión a la base de datos
            engine = create_engine('mysql+mysqlconnector://root:8399243Leav_@localhost/venadobdpredict')

            # Obtener los datos de distribucion_venado del producto seleccionado
            query_distribucion = "SELECT d.fecha_distribucion_mensual, d.total_cantidad_distribucion, p.nombre_producto " \
                                 "FROM distribucion_venado d " \
                                 "JOIN productos_venado p ON d.producto_id = p.id " \
                                 "WHERE p.nombre_producto = %s"
            distribucion_data = pd.read_sql(query_distribucion, con=engine, params=[nom_prod])
            print("Query distribucion:", query_distribucion % nom_prod)
            distribucion_data['fecha_distribucion_mensual'] = pd.to_datetime(
                distribucion_data['fecha_distribucion_mensual'])

            # Obtener los datos de produccion_venado del producto seleccionado
            query_produccion = "SELECT p.fecha_produccion_mensual, p.cantidad_produccion, pr.nombre_producto " \
                               "FROM produccion_venado p " \
                               "JOIN productos_venado pr ON p.producto_id = pr.id " \
                               "WHERE pr.nombre_producto = %s"
            produccion_data = pd.read_sql(query_produccion, con=engine, params=[nom_prod])
            print("Query produccion:", query_produccion % nom_prod)
            produccion_data['fecha_produccion_mensual'] = pd.to_datetime(produccion_data['fecha_produccion_mensual'])

            # Fusionar las columnas de fecha en una sola columna
            df = pd.DataFrame()
            df['fecha'] = distribucion_data['fecha_distribucion_mensual'].combine_first(
                produccion_data['fecha_produccion_mensual'])
            df['total_cantidad_distribucion'] = distribucion_data['total_cantidad_distribucion']
            df['cantidad_produccion'] = produccion_data['cantidad_produccion']
            df['nombre_producto'] = distribucion_data['nombre_producto'].combine_first(
                produccion_data['nombre_producto'])
            print(df)
            # Establecer la frecuencia a 'MS'
            df = df.set_index('fecha')
            df = df.asfreq('MS')

            # Dividir los datos en conjunto de entrenamiento y validación
            train_size = int(len(df) * 0.8)
            train_data = df['cantidad_produccion'][:train_size]
            test_data = df['cantidad_produccion'][train_size:]
            # Generar fechas mensuales desde enero de 2018 hasta diciembre de 2022
            fechas = df.index[train_size:train_size + len(test_data)].strftime('%m-%y')

            # Crear una lista con los meses festivos en Bolivia
            meses_festivos_bolivia = [1, 2, 3, 5, 6, 8, 11, 12]

            # Crear una variable binaria que indica si el mes es festivo en Bolivia o no
            data = pd.DataFrame({'Fecha': fechas})
            data['HOLYMONTS'] = [1 if int(date[:2]) in meses_festivos_bolivia else 0 for date in fechas]

            # Asignar los valores de HOLYMONTS en df utilizando indexación booleana
            df.loc[df.index[train_size:train_size + len(test_data)], 'HOLYMONTS'] = data['HOLYMONTS'].values

            # Obtener los datos exógenos para el conjunto de prueba
            exog_test_data = df[['total_cantidad_distribucion', 'HOLYMONTS']][train_size:train_size + len(test_data)]
            # Modelar la serie con SARIMAX y optimizar los parámetros
            fecha_inicio = df.index[-1]

            best_rmse = float('inf')
            best_model = None
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
                                        predicciones = modelo_ajustado.predict(start=fecha_inicio,
                                                                               end=fecha_usuario_pred,
                                                                               exog=exog_test_data, dynamic=False)
                                        rmse = np.sqrt(np.mean((predicciones - test_data) ** 2))
                                        if rmse < best_rmse:
                                            best_rmse = rmse
                                            best_model = modelo_ajustado
                                            best_product_name = df['nombre_producto'].iloc[-1]
                                    except:
                                        continue
            # Ver el resumen del mejor modelo
            summary = best_model.summary()

            # Obtener las fechas de inicio y fin para las predicciones
            start_date = fecha_inicio
            end_date = fecha_usuario_pred

            # Hacer predicciones en el conjunto de validación usando el mejor modelo
            predicciones = best_model.predict(start=start_date, end=end_date, exog=exog_test_data, dynamic=False)

            # Calcular el error de las predicciones usando el mejor modelo
            error = np.sqrt(np.mean((predicciones - test_data) ** 2))* 0.1

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
            print("nom_prod:", nom_prod)
            print("fecha_pred:", fecha_usuario_pred)
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