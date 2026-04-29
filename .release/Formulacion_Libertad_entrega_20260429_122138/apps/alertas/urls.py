from django.urls import path

from .views import (
    AlertaCerrarView,
    AlertaDetailView,
    AlertaListView,
    AlertaMarcarRevisadaView,
)

app_name = "alertas"

urlpatterns = [
    path("", AlertaListView.as_view(), name="lista"),
    path("<int:pk>/", AlertaDetailView.as_view(), name="detalle"),
    path("<int:pk>/revisar/", AlertaMarcarRevisadaView.as_view(), name="revisar"),
    path("<int:pk>/cerrar/", AlertaCerrarView.as_view(), name="cerrar"),
]
