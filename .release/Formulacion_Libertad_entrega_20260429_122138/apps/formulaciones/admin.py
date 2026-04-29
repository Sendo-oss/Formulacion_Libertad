from django.contrib import admin

from .forms import BaseFormulacionDetalleFormSet
from .models import Formulacion, FormulacionDetalle


class FormulacionDetalleInline(admin.TabularInline):
    model = FormulacionDetalle
    extra = 1
    formset = BaseFormulacionDetalleFormSet


@admin.register(Formulacion)
class FormulacionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "tipo_formulacion", "origen", "estado", "creado_por")
    list_filter = ("categoria", "estado", "origen", "tipo_formulacion")
    search_fields = ("codigo", "nombre")
    inlines = [FormulacionDetalleInline]
