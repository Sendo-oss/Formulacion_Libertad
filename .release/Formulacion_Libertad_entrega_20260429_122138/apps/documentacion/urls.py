from django.urls import path

from .views import (
    DocumentoTecnicoCreateView,
    DocumentoTecnicoDeleteView,
    DocumentoTecnicoDetailView,
    DocumentoTecnicoListView,
    DocumentoTecnicoUpdateView,
)

app_name = "documentacion"

urlpatterns = [
    path("", DocumentoTecnicoListView.as_view(), name="lista"),
    path("nuevo/", DocumentoTecnicoCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", DocumentoTecnicoUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", DocumentoTecnicoDeleteView.as_view(), name="eliminar"),
    path("<int:pk>/", DocumentoTecnicoDetailView.as_view(), name="detalle"),
]
