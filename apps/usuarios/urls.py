from django.urls import path

from .views import (
    CambioContrasenaCompletadoView,
    CambioContrasenaObligatorioView,
    HistorialSistemaListView,
    SolicitudRecuperacionCreateView,
    SolicitudRecuperacionDeleteView,
    SolicitudRecuperacionDoneView,
    SolicitudRecuperacionListView,
    SolicitudRecuperacionUpdateView,
    UsuarioCreateView,
    UsuarioListView,
    UsuarioUpdateView,
)

app_name = "usuarios"

urlpatterns = [
    path("", UsuarioListView.as_view(), name="lista"),
    path("nuevo/", UsuarioCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", UsuarioUpdateView.as_view(), name="editar"),
    path("recuperacion/", SolicitudRecuperacionCreateView.as_view(), name="recuperacion_solicitar"),
    path("recuperacion/enviada/", SolicitudRecuperacionDoneView.as_view(), name="recuperacion_enviada"),
    path("recuperaciones/", SolicitudRecuperacionListView.as_view(), name="recuperaciones"),
    path("historial/", HistorialSistemaListView.as_view(), name="historial"),
    path("recuperaciones/<int:pk>/gestionar/", SolicitudRecuperacionUpdateView.as_view(), name="recuperacion_gestionar"),
    path("recuperaciones/<int:pk>/eliminar/", SolicitudRecuperacionDeleteView.as_view(), name="recuperacion_eliminar"),
    path("cambiar-contrasena/", CambioContrasenaObligatorioView.as_view(), name="cambiar_contrasena"),
    path("cambiar-contrasena/completado/", CambioContrasenaCompletadoView.as_view(), name="cambio_contrasena_completado"),
]
