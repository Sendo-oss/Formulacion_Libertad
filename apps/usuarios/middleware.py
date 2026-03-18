from django.shortcuts import redirect
from django.urls import reverse


class ForzarCambioContrasenaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, "debe_cambiar_contrasena", False):
            ruta_permitida = {
                reverse("usuarios:cambiar_contrasena"),
                reverse("usuarios:cambio_contrasena_completado"),
                reverse("logout"),
            }
            if request.path not in ruta_permitida and not request.path.startswith("/static/") and not request.path.startswith("/media/"):
                return redirect("usuarios:cambiar_contrasena")
        return self.get_response(request)
