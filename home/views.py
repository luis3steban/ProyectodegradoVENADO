from django.shortcuts import render
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect , get_object_or_404
from django.http import FileResponse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse , HttpResponseRedirect
from django_plotly_dash import DjangoDash
import pickle
from django.conf import settings
import csv
from .models import Accesos, Usuarios, Produccion_venado , Distribuciones_venado ,AuditoriaPredicciones
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import pdfkit
import datetime
from sqlalchemy import create_engine
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from django.http import HttpResponse, Http404
from pathlib import Path
from django.template.loader import get_template
from django.contrib.auth.hashers import make_password
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
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
import random
import string
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .AgregarReportesForm import ProduccionDistribucionForm
from datetime import date
# Create your views here.
def home(requests):
    return render(requests, 'home/login.html')
def dash_modal_view(request):
    return render(request, 'modal_template.html')
def pdf(requests):
    return render(requests, 'prediction.html')
def marcas(request):
    error_message = request.session.pop('error_message', None)  # Obtener y eliminar el mensaje de error de la sesión
    return render(request, 'home/Marcas.html', {'error_message': error_message})
def LineaCereales(requests):
    return render(requests, 'home/LineaCerealesKris.html')
def LineaPanificacion(requests):
    return render(requests, 'home/LineaPanificacionKris.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            usuario = Usuarios.objects.get(correo=email)
        except Usuarios.DoesNotExist:
            return render(request, 'home/forgot-password.html', {'error_message': 'El correo electrónico no está registrado.'})

        token = generate_reset_token()

        usuario.reset_token = token
        usuario.save()

        send_password_reset_email(email, token)

        return render(request, 'home/password_reset_email_sent.html')

    return render(request, 'home/forgot-password.html')
def reset_password(request, token):
    try:
        print(token)
        user = Usuarios.objects.get(reset_token=token)
        print(user)
    except Usuarios.DoesNotExist:
        return render(request, 'home/password_reset_invalid.html')
    if user.reset_token == token:
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.reset_token = None
                user.save()
                return render(request, 'home/password_reset_success.html')
            else:
                return render(request, 'home/password_reset.html', {'token': token, 'error_message': 'Las contraseñas no coinciden.'})

        return render(request, 'home/password_reset.html', {'token': token})
    else:
        return render(request, 'home/password_reset_invalid.html')
def generate_reset_token():
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(random.choice(letters_and_digits) for _ in range(16))
    return token

def send_password_reset_email(email, token):
    domain = '127.0.0.1:8000'
    reset_link = reverse('reset_password', args=[token])
    reset_url = f"http://{domain}{reset_link}"

    subject = 'Restablecimiento de contraseña'
    message = f'Hola, has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para continuar: {reset_url}'
    from_email = 'venadopredict@sandboxd00db2adb5d546d2ba28a6a4d3e76ee3.mailgun.org'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def reporteHistorial(requests):
    auditorias = AuditoriaPredicciones.objects.all().order_by('-fechaprediccion', '-horaprediccion')
    return render(requests, 'home/reportehistorialpredicciones.html', {'auditorias': auditorias})
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
            fecha_usuario_pred = fecha_pred + "-01"
            # Crear la conexión a la base de datos
            engine = create_engine('mysql+mysqlconnector://root:8399243Leav_@localhost/venadobdpredict')

            # Obtener los datos de distribucion_venado del producto seleccionado
            query_distribucion = "SELECT d.fecha_distribucion_mensual, d.total_cantidad_distribucion, p.nombre_producto " \
                                 "FROM distribucion_venado d " \
                                 "JOIN productos_venado p ON d.producto_id = p.id " \
                                 "WHERE p.nombre_producto = %s " \
                                "ORDER BY d.fecha_distribucion_mensual"
            distribucion_data = pd.read_sql(query_distribucion, con=engine, params=[nom_prod])
            print("Query distribucion:", query_distribucion % nom_prod)
            distribucion_data['fecha_distribucion_mensual'] = pd.to_datetime(
                distribucion_data['fecha_distribucion_mensual'])

            # Obtener los datos de produccion_venado del producto seleccionado
            query_produccion = "SELECT p.fecha_produccion_mensual, p.cantidad_produccion, pr.nombre_producto " \
                               "FROM produccion_venado p " \
                               "JOIN productos_venado pr ON p.producto_id = pr.id " \
                               "WHERE pr.nombre_producto = %s" \
                               "ORDER BY p.fecha_produccion_mensual"

            produccion_data = pd.read_sql(query_produccion, con=engine, params=[nom_prod])
            print("Query produccion:", query_produccion % nom_prod)
            produccion_data['fecha_produccion_mensual'] = pd.to_datetime(produccion_data['fecha_produccion_mensual'])
            print(distribucion_data.head())
            print(produccion_data.head())

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
            plt.title('Grafica de predicciones - correlacion de Tendencia', fontsize=20)
            plt.xlabel('Fecha mensual producción')
            plt.ylabel('Producción unidades')
            plt.legend()
            plt.savefig('predicciones.png')

            cantidad_produccion = df['cantidad_produccion']
            cantidad_distribucion = df['total_cantidad_distribucion']
            fechas_mensual = produccion_data['fecha_produccion_mensual']


            # Verificar la estacionalidad y tendencia en las series generadas
            decomposition_produccion = seasonal_decompose(cantidad_produccion, model='additive', period=12)
            tendencia_produccion = decomposition_produccion.trend
            estacionalidad_produccion = decomposition_produccion.seasonal

            # Crear el gráfico de comparación
            plt.figure(figsize=(10, 6))
            plt.plot(fechas_mensual, cantidad_produccion , label='Cantidad Producida')
            plt.plot(fechas_mensual, cantidad_distribucion, label='Cantidad Distribuida')
            plt.plot(fechas_mensual, tendencia_produccion, label='Tendencia')
            plt.plot(fechas_mensual, estacionalidad_produccion, label='Estacionalidad')
            plt.xlabel('Fecha')
            plt.ylabel('Cantidad')
            plt.title('Comparación entre Cantidad Producida y Cantidad Distribuida')
            plt.legend()
            plt.savefig('tendencias.png')
            import base64

            # Leer la imagen generada
            with open('predicciones.png', 'rb') as f:
                image_data = f.read()
            # Codificar la imagen en base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            with open('tendencias.png', 'rb') as f:
                image_tendencia = f.read()
            tendencia_img = base64.b64encode(image_tendencia).decode('utf-8')
            # Renderizar la plantilla de resultados con los datos
            contexte = {
                'summary': summary,
                'predicciones': zip(predicciones.index.strftime('%Y-%m-%d'), predicciones),
                'error': error,
                'produccion_adecuada': produccion_adecuada,
                'nombre_producto': nombre_producto,
                'grafica_encoded': encoded_image,
                'tendencia_img': tendencia_img,
                'fecha_usuario_pred': fecha_usuario_pred

            }
            template = get_template('prediction.html')
            html = template.render(contexte)
            pdf = generate_pdf(html)

            # Obtener la tabla de coeficientes
            table_coef = best_model.summary().tables[1]
            # Variables de interés
            variables = ['ar.L1','ma.L1', 'ar.S.L12', 'sigma2']
            # Coeficientes
            coeficientes = {
                'ar.L1': 0.979,  # Valor predeterminado si no se encuentra en la tabla
                'ma.L1': 0.979,  # Valor predeterminado si no se encuentra en la tabla
                'ar.S.L12': 0.979,  # Valor predeterminado si no se encuentra en la tabla
                'sigma2': 0.979# Valor predeterminado si no se encuentra en la tabla
            }
            for row in table_coef.data:
                variable = row[0]
                if variable in variables:
                    coeficiente = row[1]
                    coeficientes[variable] = coeficiente
            # Asignar coeficientes a variables independientes
            ar_L1 = coeficientes['ar.L1']
            ma_L1 = coeficientes['ma.L1']
            ar_S_L12 = coeficientes['ar.S.L12']
            sigma2 = coeficientes['sigma2']
            # AIC, BIC y HQIC
            table_general = best_model.summary().tables[0]
            parametroajustado = table_general.data[1][1]
            Horaprediccion = table_general.data[3][1]
            # Obtener la fecha actual
            from datetime import date
            fecha_actual = date.today()
            usuarioactual = "22"
            nomproductoe = nombre_producto
            Fechaseleccionada = fecha_usuario_pred
            fechaprediccion = fecha_actual
            horaprediccion =Horaprediccion
            cantprediccion = produccion_adecuada
            modelo = parametroajustado
            arL1 = ar_L1
            maL1 = ma_L1
            arSL2 = ar_S_L12
            sigma2 = sigma2
            from django.core.files.base import ContentFile

            pdf_content = pdf.content if isinstance(pdf, HttpResponse) else pdf
            pdf_file = ContentFile(pdf_content)
            auditoria = AuditoriaPredicciones(
                usuario_id=usuarioactual,
                nomproducto=nomproductoe,
                Fechaseleccionada=Fechaseleccionada,
                fechaprediccion=fechaprediccion,
                horaprediccion=horaprediccion,
                cantprediccion=cantprediccion,
                modelo=modelo,
                arL1=arL1,
                maL1=maL1,
                arSL2=arSL2,
                sigma2=sigma2
            )

            auditoria.pdf.save('prediction_results.pdf', pdf_file)
            auditoria.save()
            if pdf is not None:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="prediction_results.pdf"'
                return response
                # Construir el diccionario de datos de respuesta
            response_data = {
                'produccion_adecuada': produccion_adecuada,
                'nombre_producto': nombre_producto,
                'fecha_usuario_pred': fecha_usuario_pred
             }
            print(response_data)
             # Devolver la respuesta JSON
            return JsonResponse(response_data)
        except Exception as e:
            error_message = f"Se produjo un error: {str(e)}"
            context = {'error_message': error_message}
        return render(request, 'prediction_form.html', context)
    else:
        return render(request, 'prediction_form.html')
import os
def descargar_pdf(request, id):
    auditoria = get_object_or_404(AuditoriaPredicciones, id=id)
    file_path = Path(settings.MEDIA_ROOT) / str(auditoria.pdf)
    print(file_path)
    if file_path.exists():
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + file_path.name
            return response
    else:
        print("File Path:", file_path)  # Imprime la ruta del archivo
        raise Http404("El archivo PDF no existe.")
def addReportesMensuales(request):
    if request.method == 'POST':
         form = ProduccionDistribucionForm(request.POST)
         if form.is_valid():
                # Obtener los datos ingresados por el usuario
                producto = form.cleaned_data['producto']
                marca_producto = form.cleaned_data['marca_producto']
                fecha_mensual = form.cleaned_data['fecha_mensual']
                cantidad_produccion = form.cleaned_data['cantidad_produccion']
                canal_horizontal = form.cleaned_data['canal_horizontal']
                canal_tradicional = form.cleaned_data['canal_tradicional']
                canal_moderno = form.cleaned_data['canal_moderno']
                total_cantidad_distribucion = form.cleaned_data['total_cantidad_distribucion']
                # Extraer el año y el mes de la fecha seleccionada
                year = fecha_mensual.year
                month = fecha_mensual.month
                # Crear nuevos objetos en las tablas de Produccion_venado y Distribuciones_venado
                produccion = Produccion_venado(
                    producto=producto,
                    marca_producto=marca_producto,
                    fecha_produccion_mensual=f"{year}-0{month}",
                    cantidad_produccion=cantidad_produccion
                )
                produccion.save()

                distribucion = Distribuciones_venado(
                    producto=producto,
                    fecha_distribucion_mensual=f"{year}-0{month}",
                    canal_horizontal=canal_horizontal,
                    canal_tradicional=canal_tradicional,
                    canal_moderno=canal_moderno,
                    total_cantidad_distribucion=total_cantidad_distribucion
                )
                distribucion.save()


                # Realizar cualquier otra acción necesaria y redirigir al usuario a otra página
                return render(request, 'home/AddReporteMensual.html')
    else:
            form = ProduccionDistribucionForm()

    return render(request, 'home/AddReporteMensual.html', {'form': form})