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
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            usuario = Usuarios.objects.get(correo=email)
        except Usuarios.DoesNotExist:
            return render(request, 'home/ModuloAutenticacion/forgot-password.html', {'error_message': 'El correo electrónico no está registrado.'})

        token = generate_reset_token()

        usuario.reset_token = token
        usuario.save()

        send_password_reset_email(email, token)

        return render(request, 'home/ModuloAutenticacion/password_reset_email_sent.html')

    return render(request, 'home/ModuloAutenticacionforgot-password.html')

def reset_password(request, token):
    try:
        print(token)
        user = Usuarios.objects.get(reset_token=token)
        print(user)
    except Usuarios.DoesNotExist:
        return render(request, 'home/ModuloAutenticacion/password_reset_invalid.html')
    if user.reset_token == token:
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.reset_token = None
                user.save()
                return render(request, 'home/ModuloAutenticacion/password_reset_success.html')
            else:
                return render(request, 'home/ModuloAutenticacion/password_reset.html', {'token': token, 'error_message': 'Las contraseñas no coinciden.'})

        return render(request, 'home/ModuloAutenticacion/password_reset.html', {'token': token})
    else:
        return render(request, 'home/ModuloAutenticacion/password_reset_invalid.html')
    
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

from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

@never_cache
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            user = Usuarios.objects.get(correo=correo)

            if user.verificar_password(password):
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)

                request.session['access_token'] = token
                request.session['user_id'] = user.id

                id_acceso = user.acceso_id

                response = redirect('dashboard')
                response.set_cookie('id_acceso', id_acceso)
                response.set_cookie('correo', correo)

                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Expires'] = '0'
                response['Pragma'] = 'no-cache'

                return response
            else:
                error_message = 'Credenciales inválidas. Inténtalo nuevamente.'
                return render(request, 'home/ModuloAutenticacion/login.html', {'error_message': error_message})
        except Usuarios.DoesNotExist:
            error_message = 'Su usuario o contraseña son incorrectas, por favor intente nuevamente.'
            return render(request, 'home/ModuloAutenticacion/login.html', {'error_message': error_message})

    return render(request, 'home/ModuloAutenticacion/login.html')


from django.urls import reverse

def logout_view(request):
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'user_id' in request.session:
        del request.session['user_id']

    return redirect(reverse('login'))
