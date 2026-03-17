from django.contrib import admin

from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("tipo_alerta", "materia_prima", "prioridad", "estado", "fecha_generacion")
    list_filter = ("tipo_alerta", "prioridad", "estado")
    search_fields = ("materia_prima__nombre", "mensaje")
