from django.contrib import admin

from .models import MateriaPrima


@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "lote",
        "fecha_vencimiento",
        "requiere_control_caducidad",
        "dias_alerta_vencimiento",
        "stock_actual",
        "stock_minimo",
        "unidad_medida",
        "estado",
    )
    list_filter = ("estado", "unidad_medida", "fecha_vencimiento")
    search_fields = ("nombre", "numero_cas", "numero_einecs", "lote", "casa_comercial")
