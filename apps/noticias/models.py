from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=320)
    contenido = models.TextField()
    fuente_url = models.URLField("Enlace de referencia", blank=True)
    publicada_en = models.DateTimeField(default=timezone.now)
    activa = models.BooleanField(default=True)
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="noticias_creadas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publicada_en", "-id"]
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("noticias:detalle", kwargs={"pk": self.pk})
