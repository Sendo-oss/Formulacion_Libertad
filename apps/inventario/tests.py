from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.inventario.models import MateriaPrima
from apps.usuarios.models import Usuario


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class InventoryTests(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username="profe_inv",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )

    def test_profesor_puede_crear_materia_prima(self):
        self.client.force_login(self.profesor)
        response = self.client.post(
            reverse("inventario:crear"),
            {
                "nombre": "Glicerina",
                "numero_cas": "",
                "numero_einecs": "",
                "lote": "L-002",
                "fecha_elaboracion": "",
                "fecha_vencimiento": str(timezone.localdate() + timedelta(days=120)),
                "requiere_control_caducidad": "on",
                "dias_alerta_vencimiento": 15,
                "casa_comercial": "",
                "stock_actual": "5.00",
                "stock_minimo": "1.00",
                "unidad_medida": "ml",
                "observaciones": "",
                "estado": MateriaPrima.Estado.ACTIVA,
            },
        )

        self.assertRedirects(response, reverse("inventario:lista"))
        self.assertTrue(MateriaPrima.objects.filter(nombre="Glicerina", registrado_por=self.profesor).exists())
