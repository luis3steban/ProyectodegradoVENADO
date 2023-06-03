from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marcas&productos/', views.prediccion, name='prediccion'),
    path('contraseñaOlvidada?/', views.contraseñaolvidada, name='contraolvidada'),
    path('MarcasVenado/', views.marcas, name='marcas'),
    path('ReporteVenadoProduccion/', views.reporteProduccion, name='reporteproduccion'),
    path('ReporteVenadoDistribucion/', views.reporteDistribucion, name='reportedistribucion'),
    path('prediction/', views.modelo_prediccion, name='prediction'),
    path('login/', views.login_view, name='login'),
    path('form/', views.prediction_form, name='form'),
    path('ModuloUsuarios/', views.UsuariosMod, name='Usuarios'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('modificar-usuario/', views.modificar_usuario, name='ModificarUsuario'),
    path('obtener_opciones_acceso/', views.obtener_opciones_acceso, name='obtener_opciones_acceso'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('agregar-acceso/', views.agregar_acceso, name='agregar_acceso'),
    path('modificar-acceso/', views.modificar_acceso, name='modificar_acceso'),
    path('eliminar-acceso/', views.eliminar_acceso, name='eliminar_acceso'),
]


