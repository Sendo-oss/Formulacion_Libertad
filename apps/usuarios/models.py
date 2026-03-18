from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        PROFESOR = "PROFESOR", "Profesor"
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    debe_cambiar_contrasena = models.BooleanField(default=False)

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
        verbose_name = "Solicitud de recuperacion de contrasena"
        verbose_name_plural = "Solicitudes de recuperacion de contrasena"

    def __str__(self):
        return f"{self.correo} - {self.get_estado_display()}"
