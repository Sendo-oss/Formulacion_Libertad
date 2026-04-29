from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.alertas.models import Alerta
from apps.inventario.models import MateriaPrima
from apps.usuarios.models import Usuario


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class DashboardTests(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username="profe_dash",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )
        self.estudiante = Usuario.objects.create_user(
            username="estu_dash",
            password="Estudiante123*",
            rol=Usuario.Rol.ESTUDIANTE,
        )
        self.materia = MateriaPrima.objects.create(
            nombre="Ácido bórico",
            lote="L-001",
            fecha_vencimiento=timezone.localdate() + timedelta(days=90),
            requiere_control_caducidad=True,
            dias_alerta_vencimiento=30,
            stock_actual="10.00",
            stock_minimo="2.00",
            unidad_medida="g",
            registrado_por=self.profesor,
        )

    def test_dashboard_del_estudiante_oculta_alertas(self):
        Alerta.objects.create(
            tipo_alerta=Alerta.Tipo.STOCK_BAJO,
            materia_prima=self.materia,
            mensaje="Stock crítico",
            prioridad=Alerta.Prioridad.ALTA,
            estado=Alerta.Estado.ACTIVA,
        )
        self.client.force_login(self.estudiante)

        response = self.client.get(reverse("dashboard:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("alertas_activas", response.context)
