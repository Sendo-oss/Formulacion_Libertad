from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.formulaciones.models import Formulacion
from apps.inventario.models import MateriaPrima


class DocumentoTecnico(models.Model):
    class TipoDocumento(models.TextChoices):
        FICHA_TECNICA = "FICHA_TECNICA", "Ficha técnica"
        PROCEDIMIENTO = "PROCEDIMIENTO", "Procedimiento normalizado / procedimiento operativo estándar"

    titulo = models.CharField(max_length=200)
    tipo_documento = models.CharField(max_length=30, choices=TipoDocumento.choices)
    formulacion = models.ForeignKey(
        Formulacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_tecnicos",
    )
    materia_prima = models.ForeignKey(
        MateriaPrima,
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
        verbose_name = "Documento técnico"
        verbose_name_plural = "Documentación técnica"

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        if self.archivo and not self.archivo.name.lower().endswith(".pdf"):
            raise ValidationError({"archivo": "Solo se permiten archivos PDF."})
        if self.tipo_documento == self.TipoDocumento.PROCEDIMIENTO:
            if not self.formulacion and not self.materia_prima:
                raise ValidationError(
                    {"formulacion": "El procedimiento debe asociarse a una formulación o a una materia prima."}
                )
            if self.formulacion and self.materia_prima:
                raise ValidationError(
                    {"materia_prima": "Asocia el procedimiento solo a una formulación o a una materia prima."}
                )
        if self.tipo_documento == self.TipoDocumento.FICHA_TECNICA:
            if not self.formulacion and not self.materia_prima:
                raise ValidationError(
                    {"formulacion": "La ficha técnica debe asociarse a una formulación o a una materia prima."}
                )
            if self.formulacion and self.materia_prima:
                raise ValidationError(
                    {"materia_prima": "Asocia la ficha técnica solo a una formulación o a una materia prima."}
                )
