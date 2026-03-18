from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.usuarios.forms import LoginForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", include("apps.dashboard.urls")),
    path("calculadora/", include("apps.calculadora.urls")),
    path("usuarios/", include("apps.usuarios.urls")),
    path("materias-primas/", include("apps.inventario.urls")),
    path("formulaciones/", include("apps.formulaciones.urls")),
    path("alertas/", include("apps.alertas.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
