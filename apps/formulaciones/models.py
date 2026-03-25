from django.conf import settings
from django.db import models

from apps.inventario.models import MateriaPrima


class Formulacion(models.Model):
    CATEGORIAS_BASE = (
        "Excipiente",
        "Formula magistral tipificada",
        "Preparado oficial",
    )

    class Origen(models.TextChoices):
        INSTITUCIONAL = "INSTITUCIONAL", "Institucional"
        DOCENTE = "DOCENTE", "Creada por docente"

    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        INACTIVA = "INACTIVA", "Inactiva"
        EN_REVISION = "EN_REVISION", "En revision"

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, default="Formula magistral tipificada")
    tipo_formulacion = models.CharField(max_length=100)
    origen = models.CharField(max_length=20, choices=Origen.choices)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    fuente_referencia = models.CharField(max_length=300, blank=True)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="formulaciones_creadas",
    )
    materias_primas = models.ManyToManyField(
        MateriaPrima,
        through="FormulacionDetalle",
        related_name="formulaciones",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["codigo", "nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_categoria_display(self):
        return self.categoria

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("formulaciones:detalle", kwargs={"pk": self.pk})


class FormulacionDetalle(models.Model):
    class UnidadMedida(models.TextChoices):
        PORCENTAJE = "%", "%"
        MILILITRO = "ml", "ml"

    formulacion = models.ForeignKey(Formulacion, on_delete=models.CASCADE, related_name="detalles")
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT, related_name="detalles_formulacion")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=10, choices=UnidadMedida.choices, default=UnidadMedida.PORCENTAJE)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("formulacion", "materia_prima")
        verbose_name = "Detalle de formulacion"
        verbose_name_plural = "Detalles de formulacion"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.formulacion.codigo} - {self.materia_prima.nombre}"
