from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        PROFESOR = "PROFESOR", "Profesor"
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    debe_cambiar_contrasena = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.rol == self.Rol.ADMINISTRADOR:
            administradores = Usuario.objects.filter(rol=self.Rol.ADMINISTRADOR)
            if self.pk:
                administradores = administradores.exclude(pk=self.pk)
            if administradores.count() >= 2:
                raise ValidationError({"rol": "Solo se permiten 2 usuarios con rol de Administrador en el sistema."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"


class SolicitudRecuperacionContrasena(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ATENDIDA = "ATENDIDA", "Atendida"
        RECHAZADA = "RECHAZADA", "Rechazada"

    correo = models.EmailField()
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_recuperacion",
    )
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_atencion = models.DateTimeField(null=True, blank=True)
    atendida_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_atendidas",
    )

    class Meta:
        ordering = ["-fecha_solicitud"]
        verbose_name = "Solicitud de recuperación de contraseña"
        verbose_name_plural = "Solicitudes de recuperación de contraseña"

    def __str__(self):
        return f"{self.correo} - {self.get_estado_display()}"


class HistorialSistema(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acciones_historial",
    )
    modulo = models.CharField(max_length=50)
    accion = models.CharField(max_length=100)
    entidad = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Historial del sistema"
        verbose_name_plural = "Historial del sistema"

    def __str__(self):
        return f"{self.modulo} - {self.accion} - {self.fecha:%d/%m/%Y %H:%M}"
