from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marcas&productos/', views.prediccion, name='prediccion'),
    path('contraseñaOlvidada?/', views.contraseñaolvidada, name='contraolvidada'),
    path('registrarCuenta/', views.registrarAcc, name='registrar'),
    path('MarcasVenado/', views.marcas, name='marcas')

]