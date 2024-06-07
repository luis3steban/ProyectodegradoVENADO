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
from .Scripts.Dashboard import obtener_producto_incremento , obtener_producto_max_produccion_mes , obtener_producto_max_produccion_anio , obtener_producto_disminucion
from datetime import date
import os

# Create your views here.
def home(requests):
    return render(requests, 'home/ModuloAutenticacion/login.html')
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

def reporteHistorial(request):
    auditorias = AuditoriaPredicciones.objects.order_by('-fechaprediccion', '-horaprediccion')
    return render(request, 'home/reportehistorialpredicciones.html', {'auditorias': auditorias})
def reporteProduccion(requests):
    producciones = Produccion_venado.objects.all().order_by('fecha_produccion_mensual', 'cantidad_produccion')
    return render(requests, 'home/reporteproduccionVenado.html', {'producciones': producciones})
def reporteDistribucion(requests):
    distribuciones = Distribuciones_venado.objects.all().order_by('fecha_distribucion_mensual', 'total_cantidad_distribucion')
    return render(requests, 'home/reportedistribuicionVenado.html', {'distribuciones': distribuciones})

def dashboard(request):
    resultado_max_produccion = obtener_producto_max_produccion_mes()
    resultado_max_produccion_anio = obtener_producto_max_produccion_anio()
    resutaldo_porcetaje_incremento = obtener_producto_incremento()
    resutaldo_disminucion_produccion = obtener_producto_disminucion()
    return render(request, 'home/dashboard.html', {
        'resultado_max_produccion': resultado_max_produccion,'resultado_max_produccion_anio': resultado_max_produccion_anio,'resutaldo_porcetaje_incremento': resutaldo_porcetaje_incremento,'resutaldo_disminucion_produccion': resutaldo_disminucion_produccion
    })

def prediccion(requests):
    return render(requests, 'home/bienvenido.html')

def contraseñaolvidada(requests):
    return render(requests, 'home/ModuloAutenticacion/forgot-password.html')


# Ruta para la vista de formulario de predicción
def prediction_form(request):
    return render(request, 'base.html')
def generate_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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