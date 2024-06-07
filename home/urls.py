from django.urls import path
from . import views 
from .Scripts import prediction_model , autenticacion , ModuloUsuarios
from home.dash_apps.finished_apps import simpleexample
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marcas&productos/', views.prediccion, name='prediccion'),
    path('contraseñaOlvidada?/', views.contraseñaolvidada, name='contraolvidada'),
    path('MarcasVenado/', views.marcas, name='marcas'),
    path('CerealesKris/', views.LineaCereales, name='cerealeskris'),
    path('pdf/', views.pdf, name='pdf'),
    path('PanificacionKris/', views.LineaPanificacion, name='panificacionkris'),
    path('ReporteHistorialPredicciones/', views.reporteHistorial, name='reporteauditoria'),
    path('ReporteVenadoProduccion/', views.reporteProduccion, name='reporteproduccion'),
    path('ReporteVenadoDistribucion/', views.reporteDistribucion, name='reportedistribucion'),
    path('prediction/', prediction_model.modelo_prediccion, name='prediction'),
    path('login/', autenticacion.login_view, name='login'),
    path('logout/', autenticacion.logout_view, name='logout'),
    path('forgot-password/', autenticacion.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', autenticacion.reset_password, name='reset_password'),
    path('form/', views.prediction_form, name='form'),
    path('ModuloUsuarios/', ModuloUsuarios.UsuariosMod, name='Usuarios'),
    path('agregar-usuario/', ModuloUsuarios.agregar_usuario, name='agregar_usuario'),
    path('modificar-usuario/', ModuloUsuarios.modificar_usuario, name='ModificarUsuario'),
    path('obtener_opciones_acceso/', ModuloUsuarios.obtener_opciones_acceso, name='obtener_opciones_acceso'),
    path('eliminar-usuario/<int:usuario_id>/', ModuloUsuarios.eliminar_usuario, name='eliminar_usuario'),
    path('agregar-acceso/', ModuloUsuarios.agregar_acceso, name='agregar_acceso'),
    path('modificar-acceso/', ModuloUsuarios.modificar_acceso, name='modificar_acceso'),
    path('eliminar-acceso/', ModuloUsuarios.eliminar_acceso, name='eliminar_acceso'),
    path('descargar_pdf/<int:id>/', views.descargar_pdf, name='descargar_pdf'),
    path('Add-reportes/', views.addReportesMensuales, name='addReportes'),
]


