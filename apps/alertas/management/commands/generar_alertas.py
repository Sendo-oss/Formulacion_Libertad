from django.core.management.base import BaseCommand

from apps.alertas.services import generar_alertas_automaticas


class Command(BaseCommand):
    help = "Genera o actualiza alertas automáticas para materias primas."

    def handle(self, *args, **options):
        generar_alertas_automaticas()
        self.stdout.write(self.style.SUCCESS("Alertas generadas o actualizadas correctamente."))
