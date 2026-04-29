from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.defaults import page_not_found, permission_denied, server_error

from apps.usuarios.forms import LoginForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", include("apps.dashboard.urls")),
    path("calculadora/", include("apps.calculadora.urls")),
    path("documentacion/", include("apps.documentacion.urls")),
    path("noticias/", include("apps.noticias.urls")),
    path("usuarios/", include("apps.usuarios.urls")),
    path("materias-primas/", include("apps.inventario.urls")),
    path("formulaciones/", include("apps.formulaciones.urls")),
    path("alertas/", include("apps.alertas.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
