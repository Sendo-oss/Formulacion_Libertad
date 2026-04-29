from django.urls import path

from .views import (
    MateriaPrimaCreateView,
    MateriaPrimaDetailView,
    MateriaPrimaListView,
    MateriaPrimaUpdateView,
)

app_name = "inventario"

urlpatterns = [
    path("", MateriaPrimaListView.as_view(), name="lista"),
    path("nueva/", MateriaPrimaCreateView.as_view(), name="crear"),
    path("<int:pk>/", MateriaPrimaDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", MateriaPrimaUpdateView.as_view(), name="editar"),
]
