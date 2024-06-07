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
from ..models import Accesos, Usuarios, Produccion_venado , Distribuciones_venado ,AuditoriaPredicciones
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
from ..AgregarReportesForm import ProduccionDistribucionForm
from datetime import date

def UsuariosMod(requests):
    accesos = Accesos.objects.all()
    usuarios = Usuarios.objects.all()
    return render(requests, 'home/ModuloUsuarios/moduloUsuarios.html', {'accesos': accesos, 'usuarios': usuarios})

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

from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import connection

def obtener_usuario_predictor(correo):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", [correo])
            row = cursor.fetchone() 
            if row:
                usuario_id = row[0]
                return usuario_id  
            else:
                return None  
    except Exception as e:
        print("Error:", e)
        return None 
