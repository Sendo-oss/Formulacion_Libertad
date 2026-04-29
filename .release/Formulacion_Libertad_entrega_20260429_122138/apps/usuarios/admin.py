from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import HistorialSistema, SolicitudRecuperacionContrasena, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "rol", "is_active")
    list_filter = ("rol", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Información institucional", {"fields": ("rol", "debe_cambiar_contrasena")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información institucional", {"fields": ("rol", "debe_cambiar_contrasena")}),
    )


@admin.register(SolicitudRecuperacionContrasena)
class SolicitudRecuperacionContrasenaAdmin(admin.ModelAdmin):
    list_display = ("correo", "usuario", "estado", "fecha_solicitud", "fecha_atencion", "atendida_por")
    list_filter = ("estado", "fecha_solicitud")
    search_fields = ("correo", "usuario__username", "usuario__first_name", "usuario__last_name")


@admin.register(HistorialSistema)
class HistorialSistemaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "modulo", "accion", "entidad")
    list_filter = ("modulo", "accion", "fecha")
    search_fields = ("descripcion", "entidad", "usuario__username", "usuario__first_name", "usuario__last_name")
