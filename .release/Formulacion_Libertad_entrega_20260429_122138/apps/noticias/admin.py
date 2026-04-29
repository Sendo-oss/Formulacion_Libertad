from django.contrib import admin

from .models import Noticia


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "publicada_en", "activa", "creada_por")
    list_filter = ("activa", "publicada_en")
    search_fields = ("titulo", "resumen", "contenido", "creada_por__username")
