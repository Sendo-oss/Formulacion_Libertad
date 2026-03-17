from datetime import timedelta

from django.utils import timezone

from apps.inventario.models import MateriaPrima

from .models import Alerta


DIAS_ALERTA_CADUCIDAD = 30


def generar_alertas_materia_prima(materia_prima):
    hoy = timezone.localdate()
    alertas = []
    tipos_activos = set()

    if materia_prima.requiere_control_caducidad and materia_prima.fecha_vencimiento:
        if materia_prima.fecha_vencimiento < hoy:
            alertas.append(
                {
                    "tipo_alerta": Alerta.Tipo.CADUCADA,
                    "prioridad": Alerta.Prioridad.CRITICA,
                    "mensaje": f"La materia prima {materia_prima.nombre} esta caducada.",
                }
            )
        elif materia_prima.fecha_vencimiento <= hoy + timedelta(days=DIAS_ALERTA_CADUCIDAD):
            alertas.append(
                {
                    "tipo_alerta": Alerta.Tipo.PROXIMA_CADUCIDAD,
                    "prioridad": Alerta.Prioridad.ALTA,
                    "mensaje": f"La materia prima {materia_prima.nombre} vencera pronto.",
                }
            )

    if materia_prima.stock_actual == 0:
        alertas.append(
            {
                "tipo_alerta": Alerta.Tipo.SIN_STOCK,
                "prioridad": Alerta.Prioridad.CRITICA,
                "mensaje": f"La materia prima {materia_prima.nombre} no tiene stock disponible.",
            }
        )
    elif materia_prima.stock_actual <= materia_prima.stock_minimo:
        alertas.append(
            {
                "tipo_alerta": Alerta.Tipo.STOCK_BAJO,
                "prioridad": Alerta.Prioridad.MEDIA,
                "mensaje": f"La materia prima {materia_prima.nombre} tiene stock bajo.",
            }
        )

    for alerta in alertas:
        tipos_activos.add(alerta["tipo_alerta"])

    for alerta in alertas:
        Alerta.objects.get_or_create(
            tipo_alerta=alerta["tipo_alerta"],
            materia_prima=materia_prima,
            estado=Alerta.Estado.ACTIVA,
            defaults={
                "mensaje": alerta["mensaje"],
                "prioridad": alerta["prioridad"],
            },
        )

    Alerta.objects.filter(materia_prima=materia_prima, estado=Alerta.Estado.ACTIVA).exclude(
        tipo_alerta__in=tipos_activos
    ).update(estado=Alerta.Estado.CERRADA)


def generar_alertas_automaticas():
    for materia_prima in MateriaPrima.objects.all():
        generar_alertas_materia_prima(materia_prima)
