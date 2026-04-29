from django.urls import path

from .views import CalculadoraView

app_name = "calculadora"

urlpatterns = [
    path("", CalculadoraView.as_view(), name="inicio"),
]
