from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.noticias.models import Noticia
from apps.usuarios.models import Usuario


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class NewsTests(TestCase):
    def setUp(self):
        self.profesor = Usuario.objects.create_user(
            username="profe_news",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )
        self.estudiante = Usuario.objects.create_user(
            username="estu_news",
            password="Estudiante123*",
            rol=Usuario.Rol.ESTUDIANTE,
        )
        self.noticia_oculta = Noticia.objects.create(
            titulo="Noticia interna",
            resumen="Resumen interno",
            contenido="Contenido interno",
            activa=False,
            creada_por=self.profesor,
        )
        self.noticia_publica = Noticia.objects.create(
            titulo="Noticia pública",
            resumen="Resumen visible",
            contenido="Contenido visible",
            activa=True,
            creada_por=self.profesor,
        )

    def test_estudiante_solo_ve_noticias_activas(self):
        self.client.force_login(self.estudiante)
        response = self.client.get(reverse("noticias:lista"))

        self.assertEqual(response.status_code, 200)
        noticias = list(response.context["noticias"])
        self.assertIn(self.noticia_publica, noticias)
        self.assertNotIn(self.noticia_oculta, noticias)

    def test_profesor_puede_crear_noticia(self):
        self.client.force_login(self.profesor)
        response = self.client.post(
            reverse("noticias:crear"),
            {
                "titulo": "Nueva noticia",
                "resumen": "Resumen de prueba",
                "contenido": "Contenido de prueba",
                "fuente_url": "",
                "publicada_en": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                "activa": "on",
            },
        )

        self.assertRedirects(response, reverse("noticias:lista"))
        self.assertTrue(Noticia.objects.filter(titulo="Nueva noticia", creada_por=self.profesor).exists())
