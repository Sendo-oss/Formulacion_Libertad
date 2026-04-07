from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.formulaciones.models import Formulacion, FormulacionDetalle
from apps.inventario.models import MateriaPrima
from apps.usuarios.models import Usuario


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class FormulacionTests(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username="profe_form",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )
        self.estudiante = Usuario.objects.create_user(
            username="estu_form",
            password="Estudiante123*",
            rol=Usuario.Rol.ESTUDIANTE,
        )
        self.materia_1 = MateriaPrima.objects.create(
            nombre="Lanolina",
            lote="LAN-01",
            fecha_vencimiento=timezone.localdate() + timedelta(days=120),
            requiere_control_caducidad=True,
            dias_alerta_vencimiento=20,
            stock_actual="15.00",
            stock_minimo="3.00",
            unidad_medida="g",
            registrado_por=self.profesor,
        )
        self.materia_2 = MateriaPrima.objects.create(
            nombre="Vaselina sólida",
            lote="VAS-02",
            fecha_vencimiento=timezone.localdate() + timedelta(days=120),
            requiere_control_caducidad=True,
            dias_alerta_vencimiento=20,
            stock_actual="25.00",
            stock_minimo="4.00",
            unidad_medida="g",
            registrado_por=self.profesor,
        )

    def test_profesor_puede_crear_formulacion_valida(self):
        self.client.force_login(self.profesor)
        response = self.client.post(
            reverse("formulaciones:crear"),
            {
                "codigo": "FM-100",
                "nombre": "Pomada de prueba",
                "descripcion": "Descripción",
                "categoria": "Formula magistral tipificada",
                "nueva_categoria": "",
                "tipo_formulacion": "Pomada",
                "origen": Formulacion.Origen.DOCENTE,
                "estado": Formulacion.Estado.ACTIVA,
                "fuente_referencia": "Manual",
                "observaciones": "",
                "detalles-TOTAL_FORMS": "2",
                "detalles-INITIAL_FORMS": "0",
                "detalles-MIN_NUM_FORMS": "0",
                "detalles-MAX_NUM_FORMS": "1000",
                "detalles-0-materia_prima": str(self.materia_1.pk),
                "detalles-0-cantidad": "50.00",
                "detalles-0-unidad_medida": FormulacionDetalle.UnidadMedida.PORCENTAJE,
                "detalles-0-orden": "1",
                "detalles-1-materia_prima": str(self.materia_2.pk),
                "detalles-1-cantidad": "50.00",
                "detalles-1-unidad_medida": FormulacionDetalle.UnidadMedida.PORCENTAJE,
                "detalles-1-orden": "2",
            },
        )

        formulacion = Formulacion.objects.get(codigo="FM-100")
        self.assertRedirects(response, reverse("formulaciones:detalle", kwargs={"pk": formulacion.pk}))
        self.assertEqual(formulacion.detalles.count(), 2)

    def test_estudiante_no_puede_crear_formulacion(self):
        self.client.force_login(self.estudiante)
        response = self.client.get(reverse("formulaciones:crear"))

        self.assertEqual(response.status_code, 403)
