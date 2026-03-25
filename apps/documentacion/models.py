from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.formulaciones.models import Formulacion


class DocumentoTecnico(models.Model):
    class TipoDocumento(models.TextChoices):
        FICHA_TECNICA = "FICHA_TECNICA", "Ficha tecnica"
        PROCEDIMIENTO = "PROCEDIMIENTO", "Procedimiento de elaboracion"

    titulo = models.CharField(max_length=200)
    tipo_documento = models.CharField(max_length=30, choices=TipoDocumento.choices)
    formulacion = models.ForeignKey(
        Formulacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_tecnicos",
    )
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to="documentacion/")
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="documentos_subidos",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en", "titulo"]
        verbose_name = "Documento tecnico"
        verbose_name_plural = "Documentacion tecnica"

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.archivo and not self.archivo.name.lower().endswith(".pdf"):
            raise ValidationError({"archivo": "Solo se permiten archivos PDF."})
