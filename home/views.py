from django.shortcuts import render
from django.conf import settings
# Create your views here.
def home (requests):
    return render(requests,'home/login.html')
def marcas (requests):
    return render(requests,'home/Marcas.html')

def dashboard (requests):
    return render(requests,'home/dashboard.html')

def prediccion (requests):
    return render(requests,'home/bienvenido.html')

def contraseñaolvidada (requests):
    return render(requests,'home/forgot-password.html')

def registrarAcc (requests):
    return render(requests,'home/register.html')