from django.contrib import admin

from .models import DocumentoTecnico


@admin.register(DocumentoTecnico)
class DocumentoTecnicoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_documento", "formulacion", "materia_prima", "subido_por", "creado_en")
    list_filter = ("tipo_documento", "creado_en")
    search_fields = ("titulo", "descripcion", "formulacion__nombre", "materia_prima__nombre", "materia_prima__lote")
