from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class MateriaPrima(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        INACTIVA = "INACTIVA", "Inactiva"
        VENCIDA = "VENCIDA", "Vencida"

    nombre = models.CharField(max_length=150)
    numero_cas = models.CharField("Numero CAS", max_length=50, blank=True)
    numero_einecs = models.CharField("Numero EINECS", max_length=50, blank=True)
    lote = models.CharField(max_length=80)
    fecha_elaboracion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    requiere_control_caducidad = models.BooleanField(default=True)
    dias_alerta_vencimiento = models.PositiveIntegerField(default=30)
    casa_comercial = models.CharField(max_length=150, blank=True)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="materias_primas_registradas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre", "lote"]
        verbose_name = "Materia prima"
        verbose_name_plural = "Materias primas"

    def __str__(self):
        return f"{self.nombre} - Lote {self.lote}"

    @property
    def dias_para_vencer(self):
        if not self.requiere_control_caducidad or not self.fecha_vencimiento:
            return None
        return (self.fecha_vencimiento - timezone.localdate()).days

    @property
    def vencimiento_texto(self):
        if not self.requiere_control_caducidad or not self.fecha_vencimiento:
            return "No caduca"
        return self.fecha_vencimiento

    @property
    def nivel_stock(self):
        if self.stock_actual == 0:
            return "SIN_STOCK"
        if self.stock_actual <= self.stock_minimo:
            return "STOCK_BAJO"
        return "NORMAL"

    def actualizar_estado_por_vencimiento(self):
        if not self.requiere_control_caducidad or not self.fecha_vencimiento:
            if self.estado == self.Estado.VENCIDA:
                self.estado = self.Estado.ACTIVA
            return
        if self.fecha_vencimiento < timezone.localdate():
            self.estado = self.Estado.VENCIDA
        elif self.estado == self.Estado.VENCIDA:
            self.estado = self.Estado.ACTIVA

    def clean(self):
        if self.requiere_control_caducidad and not self.fecha_vencimiento:
            raise ValidationError(
                {"fecha_vencimiento": "Debes ingresar fecha de vencimiento o desactivar el control de caducidad."}
            )
        if self.fecha_elaboracion and self.fecha_vencimiento and self.fecha_elaboracion > self.fecha_vencimiento:
            raise ValidationError(
                {"fecha_elaboracion": "La fecha de elaboracion no puede ser posterior al vencimiento."}
            )
        if self.stock_actual < 0:
            raise ValidationError({"stock_actual": "El stock actual no puede ser negativo."})
        if self.stock_minimo < 0:
            raise ValidationError({"stock_minimo": "El stock minimo no puede ser negativo."})
        if self.dias_alerta_vencimiento < 0:
            raise ValidationError({"dias_alerta_vencimiento": "Los dias de anticipacion no pueden ser negativos."})

    def save(self, *args, **kwargs):
        self.actualizar_estado_por_vencimiento()
        self.full_clean()
        return super().save(*args, **kwargs)
