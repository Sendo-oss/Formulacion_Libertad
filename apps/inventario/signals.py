from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.alertas.services import generar_alertas_materia_prima

from .models import MateriaPrima


@receiver(post_save, sender=MateriaPrima)
def generar_alertas_al_guardar(sender, instance, **kwargs):
    generar_alertas_materia_prima(instance)
