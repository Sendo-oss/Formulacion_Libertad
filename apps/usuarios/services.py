from .models import HistorialSistema


def registrar_historial(usuario, modulo, accion, descripcion, entidad=""):
    HistorialSistema.objects.create(
        usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
        modulo=modulo,
        accion=accion,
        entidad=entidad,
        descripcion=descripcion,
    )
