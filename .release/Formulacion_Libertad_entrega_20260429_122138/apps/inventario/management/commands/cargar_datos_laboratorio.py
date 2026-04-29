from datetime import date, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from apps.alertas.services import generar_alertas_automaticas
from apps.formulaciones.data import FORMULACIONES_BASE
from apps.formulaciones.models import Formulacion, FormulacionDetalle
from apps.inventario.data import MATERIAS_PRIMAS_BASE
from apps.inventario.models import MateriaPrima
from apps.usuarios.models import Usuario

CATALOGO_CATEGORIAS = {
    "EXCIPIENTE": "Excipiente",
    "MAGISTRAL_TIPIFICADA": "Formula magistral tipificada",
    "PREPARADO_OFICIAL": "Preparado oficial",
}


def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    value = str(value).strip()
    if not value or value.lower() == "no caduca":
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%m/%d/%y", "%d-%m-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    if len(value) == 7 and "/" in value:
        month, year = value.split("/")
        if month.isdigit() and year.isdigit():
            return date(int(year), int(month), 1)

    return None


class Command(BaseCommand):
    help = "Carga materias primas y formulaciones base a partir de los formatos institucionales."

    def add_arguments(self, parser):
        parser.add_argument("--usuario", required=True, help="Username del usuario que quedara como creador.")

    def handle(self, *args, **options):
        username = options["usuario"]
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist as exc:
            raise CommandError(f"No existe el usuario '{username}'.") from exc

        materias_por_nombre = {}
        for item in MATERIAS_PRIMAS_BASE:
            materia, _ = MateriaPrima.objects.update_or_create(
                nombre=item["nombre"],
                lote=item["lote"],
                defaults={
                    "numero_cas": item["numero_cas"],
                    "numero_einecs": item["numero_einecs"],
                    "fecha_elaboracion": parse_date(item["fecha_elaboracion"]),
                    "fecha_vencimiento": parse_date(item["fecha_vencimiento"]),
                    "requiere_control_caducidad": item["requiere_control_caducidad"],
                    "casa_comercial": item["casa_comercial"],
                    "stock_actual": Decimal(item["stock_actual"]),
                    "stock_minimo": Decimal(item["stock_minimo"]),
                    "unidad_medida": item["unidad_medida"],
                    "observaciones": item["observaciones"],
                    "registrado_por": usuario,
                },
            )
            materias_por_nombre[materia.nombre.lower()] = materia

        for item in FORMULACIONES_BASE:
            formulacion, _ = Formulacion.objects.update_or_create(
                codigo=item["codigo"],
                defaults={
                    "nombre": item["nombre"],
                    "descripcion": item["descripcion"],
                    "categoria": CATALOGO_CATEGORIAS.get(item["categoria"], item["categoria"]),
                    "tipo_formulacion": item["tipo_formulacion"],
                    "origen": item["origen"],
                    "fuente_referencia": item["fuente_referencia"],
                    "estado": Formulacion.Estado.ACTIVA,
                    "observaciones": "Registro base cargado desde formato institucional.",
                    "creado_por": usuario,
                },
            )
            formulacion.detalles.all().delete()
            for detalle in item["detalles"]:
                materia = materias_por_nombre.get(detalle["nombre"].lower())
                if not materia:
                    materia, _ = MateriaPrima.objects.get_or_create(
                        nombre=detalle["nombre"],
                        lote=f"BASE-{formulacion.codigo}",
                        defaults={
                            "numero_cas": "",
                            "numero_einecs": "",
                            "fecha_elaboracion": None,
                            "fecha_vencimiento": None,
                            "requiere_control_caducidad": False,
                            "casa_comercial": "",
                            "stock_actual": Decimal("0.00"),
                            "stock_minimo": Decimal("0.00"),
                            "unidad_medida": detalle["unidad_medida"],
                            "observaciones": "Materia prima creada automaticamente desde formulacion base.",
                            "registrado_por": usuario,
                        },
                    )
                    materias_por_nombre[materia.nombre.lower()] = materia
                FormulacionDetalle.objects.create(
                    formulacion=formulacion,
                    materia_prima=materia,
                    cantidad=Decimal(detalle["cantidad"]),
                    unidad_medida=detalle["unidad_medida"],
                    orden=detalle["orden"],
                )

        generar_alertas_automaticas()
        self.stdout.write(self.style.SUCCESS("Datos base del laboratorio cargados correctamente."))
