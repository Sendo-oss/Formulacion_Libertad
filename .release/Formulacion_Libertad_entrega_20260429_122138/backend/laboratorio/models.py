from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MateriaPrima(TimeStampedModel):
    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        INACTIVA = "inactiva", "Inactiva"

    nombre = models.CharField(max_length=150)
    numero_cas = models.CharField(max_length=50, db_index=True)
    numero_einecs = models.CharField(max_length=50, blank=True)
    lote = models.CharField(max_length=80, db_index=True)
    fecha_elaboracion = models.DateField()
    fecha_vencimiento = models.DateField(db_index=True)
    casa_comercial = models.CharField(max_length=150)
    stock_actual = models.DecimalField(max_digits=12, decimal_places=3)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=3)
    unidad_medida = models.CharField(max_length=30)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA, db_index=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="materias_primas")

    class Meta:
        ordering = ["nombre", "lote"]

    def __str__(self):
        return f"{self.nombre} ({self.lote})"


class Formulacion(TimeStampedModel):
    class Origen(models.TextChoices):
        INSTITUCIONAL = "institucional", "Institucional"
        DOCENTE = "docente", "Creada por docente"

    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        INACTIVA = "inactiva", "Inactiva"

    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=180)
    descripcion = models.TextField(blank=True)
    tipo_formulacion = models.CharField(max_length=80)
    origen = models.CharField(max_length=20, choices=Origen.choices)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="formulaciones")
    materias_primas = models.ManyToManyField(MateriaPrima, through="FormulacionDetalle", related_name="formulaciones")

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class FormulacionDetalle(TimeStampedModel):
    formulacion = models.ForeignKey(Formulacion, on_delete=models.CASCADE, related_name="detalles")
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT, related_name="detalles_formulacion")
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad_medida = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["formulacion", "materia_prima"], name="uq_formulacion_materia"),
        ]

    def __str__(self):
        return f"{self.formulacion.codigo} -> {self.materia_prima.nombre}"


class Alerta(TimeStampedModel):
    class Tipo(models.TextChoices):
        PROXIMA_CADUCIDAD = "proxima_caducidad", "Próxima a caducar"
        CADUCADA = "caducada", "Caducada"
        STOCK_BAJO = "stock_bajo", "Stock bajo"
        SIN_STOCK = "sin_stock", "Sin stock"

    class Prioridad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
        CRITICA = "critica", "Crítica"

    class Estado(models.TextChoices):
        NUEVA = "nueva", "Nueva"
        EN_REVISION = "en_revision", "En revisión"
        RESUELTA = "resuelta", "Resuelta"

    tipo_alerta = models.CharField(max_length=30, choices=Tipo.choices, db_index=True)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name="alertas")
    mensaje = models.CharField(max_length=255)
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, db_index=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVA, db_index=True)
    fecha_generacion = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-fecha_generacion"]

    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.materia_prima.nombre}"
