import tempfile
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.documentacion.models import DocumentoTecnico
from apps.formulaciones.models import Formulacion
from apps.inventario.models import MateriaPrima
from apps.usuarios.models import Usuario


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    MEDIA_ROOT=tempfile.gettempdir(),
)
class DocumentationTests(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username="profe_docs",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )
        self.estudiante = Usuario.objects.create_user(
            username="estu_docs",
            password="Estudiante123*",
            rol=Usuario.Rol.ESTUDIANTE,
        )
        self.materia = MateriaPrima.objects.create(
            nombre="Vaselina",
            lote="VAS-01",
            fecha_vencimiento=timezone.localdate() + timedelta(days=180),
            requiere_control_caducidad=True,
            dias_alerta_vencimiento=20,
            stock_actual="20.00",
            stock_minimo="5.00",
            unidad_medida="g",
            registrado_por=self.profesor,
        )
        self.formulacion = Formulacion.objects.create(
            codigo="FM-001",
            nombre="Pomada base",
            descripcion="Base de prueba",
            categoria="Formula magistral tipificada",
            tipo_formulacion="Pomada",
            origen=Formulacion.Origen.DOCENTE,
            estado=Formulacion.Estado.ACTIVA,
            fuente_referencia="Manual",
            observaciones="",
            creado_por=self.profesor,
        )

    def test_profesor_puede_subir_documento_pdf(self):
        self.client.force_login(self.profesor)
        archivo = SimpleUploadedFile("ficha.pdf", b"%PDF-1.4 archivo de prueba", content_type="application/pdf")

        response = self.client.post(
            reverse("documentacion:crear"),
            {
                "titulo": "Ficha de vaselina",
                "tipo_documento": DocumentoTecnico.TipoDocumento.FICHA_TECNICA,
                "formulacion": "",
                "materia_prima": self.materia.pk,
                "descripcion": "Documento técnico",
                "archivo": archivo,
            },
        )

        self.assertRedirects(response, reverse("documentacion:lista"))
        self.assertTrue(DocumentoTecnico.objects.filter(titulo="Ficha de vaselina").exists())

    def test_estudiante_no_puede_subir_documento(self):
        self.client.force_login(self.estudiante)
        response = self.client.get(reverse("documentacion:crear"))

        self.assertEqual(response.status_code, 403)
