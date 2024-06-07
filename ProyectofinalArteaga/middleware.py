from django.shortcuts import redirect
from django.urls import reverse

class TokenCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la ruta de la solicitud
        current_path = request.path

        # Obtener la ruta de la página de inicio de sesión
        login_url = reverse('login')

        # Verificar si la sesión está cerrada y la solicitud no es para la página de inicio de sesión
        if 'access_token' not in request.session and current_path != login_url:
            # Redirigir al usuario a la página de inicio de sesión
            return redirect(login_url)

        # Continuar con la solicitud si todo está bien
        return self.get_response(request)
