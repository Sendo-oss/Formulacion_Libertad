from django.urls import path

from .views import (
    NoticiaCreateView,
    NoticiaDeleteView,
    NoticiaDetailView,
    NoticiaListView,
    NoticiaUpdateView,
)

app_name = "noticias"

urlpatterns = [
    path("", NoticiaListView.as_view(), name="lista"),
    path("nueva/", NoticiaCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", NoticiaUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", NoticiaDeleteView.as_view(), name="eliminar"),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="detalle"),
]
