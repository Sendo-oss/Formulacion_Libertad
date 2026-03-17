from django.urls import path

from .views import (
    FormulacionActivarView,
    FormulacionCreateView,
    FormulacionDesactivarView,
    FormulacionDetailView,
    FormulacionListView,
    FormulacionUpdateView,
)

app_name = "formulaciones"

urlpatterns = [
    path("", FormulacionListView.as_view(), name="lista"),
    path("nueva/", FormulacionCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", FormulacionUpdateView.as_view(), name="editar"),
    path("<int:pk>/activar/", FormulacionActivarView.as_view(), name="activar"),
    path("<int:pk>/desactivar/", FormulacionDesactivarView.as_view(), name="desactivar"),
    path("<int:pk>/", FormulacionDetailView.as_view(), name="detalle"),
]
