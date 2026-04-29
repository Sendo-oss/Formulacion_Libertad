from django.conf import settings
from django.db import models

from apps.inventario.models import MateriaPrima


class Alerta(models.Model):
    class Tipo(models.TextChoices):
        PROXIMA_CADUCIDAD = "PROXIMA_CADUCIDAD", "Proxima caducidad"
        CADUCADA = "CADUCADA", "Caducada"
        STOCK_BAJO = "STOCK_BAJO", "Stock bajo"
        SIN_STOCK = "SIN_STOCK", "Sin stock"

    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Critica"

    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        REVISADA = "REVISADA", "Revisada"
        CERRADA = "CERRADA", "Cerrada"

    tipo_alerta = models.CharField(max_length=30, choices=Tipo.choices)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name="alertas")
    mensaje = models.TextField()
    prioridad = models.CharField(max_length=20, choices=Prioridad.choices)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    atendida_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="alertas_atendidas",
    )
    fecha_atencion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_generacion"]

    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.materia_prima.nombre}"
