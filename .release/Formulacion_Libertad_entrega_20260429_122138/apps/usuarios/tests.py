from django.test import TestCase, override_settings
from django.urls import reverse
from apps.usuarios.models import Usuario


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class LoginFlowTests(TestCase):
    def setUp(self):
        self.password = "ClaveSegura123*"
        self.user = Usuario.objects.create_user(
            username="michael",
            password=self.password,
            rol=Usuario.Rol.ADMINISTRADOR,
        )

    def test_login_invalido_muestra_mensaje_claro(self):
        response = self.client.post(
            reverse("login"),
            {"username": "usuario_inexistente", "password": "incorrecta"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario no existe o la contraseña es incorrecta.")

    def test_login_valido_redirige_al_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )

        self.assertRedirects(response, reverse("dashboard:inicio"))


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class RoleAccessTests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username="admin_test",
            password="Admin123*",
            rol=Usuario.Rol.ADMINISTRADOR,
        )
        self.profesor = Usuario.objects.create_user(
            username="profesor_test",
            password="Profesor123*",
            rol=Usuario.Rol.PROFESOR,
        )
        self.estudiante = Usuario.objects.create_user(
            username="estudiante_test",
            password="Estudiante123*",
            rol=Usuario.Rol.ESTUDIANTE,
        )

    def test_usuario_anonimo_es_redirigido_al_login(self):
        response = self.client.get(reverse("inventario:lista"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('inventario:lista')}")

    def test_administrador_puede_entrar_a_usuarios_y_alertas(self):
        self.client.force_login(self.admin)

        response_usuarios = self.client.get(reverse("usuarios:lista"))
        response_alertas = self.client.get(reverse("alertas:lista"))

        self.assertEqual(response_usuarios.status_code, 200)
        self.assertEqual(response_alertas.status_code, 200)

    def test_profesor_no_puede_entrar_a_usuarios_pero_si_a_alertas(self):
        self.client.force_login(self.profesor)

        response_usuarios = self.client.get(reverse("usuarios:lista"))
        response_alertas = self.client.get(reverse("alertas:lista"))
        response_formulaciones = self.client.get(reverse("formulaciones:crear"))

        self.assertEqual(response_usuarios.status_code, 403)
        self.assertEqual(response_alertas.status_code, 200)
        self.assertEqual(response_formulaciones.status_code, 200)

    def test_estudiante_no_puede_entrar_a_alertas_ni_a_crear_formulaciones(self):
        self.client.force_login(self.estudiante)

        response_alertas = self.client.get(reverse("alertas:lista"))
        response_formulaciones = self.client.get(reverse("formulaciones:crear"))
        response_documentacion = self.client.get(reverse("documentacion:lista"))

        self.assertEqual(response_alertas.status_code, 403)
        self.assertEqual(response_formulaciones.status_code, 403)
        self.assertEqual(response_documentacion.status_code, 200)

    def test_usuario_con_cambio_obligatorio_es_redirigido(self):
        self.estudiante.debe_cambiar_contrasena = True
        self.estudiante.save(update_fields=["debe_cambiar_contrasena"])
        self.client.force_login(self.estudiante)

        response = self.client.get(reverse("dashboard:inicio"))

        self.assertRedirects(response, reverse("usuarios:cambiar_contrasena"))


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class RecoveryFlowTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="recuperable",
            password="Recuperable123*",
            email="recuperable@itslibertad.edu.ec",
            rol=Usuario.Rol.ESTUDIANTE,
        )

    def test_crear_solicitud_de_recuperacion_asocia_usuario(self):
        response = self.client.post(
            reverse("usuarios:recuperacion_solicitar"),
            {"correo_usuario": "recuperable", "observaciones": "Perdí mi clave"},
        )

        self.assertRedirects(response, reverse("usuarios:recuperacion_enviada"))
        self.assertEqual(self.user.solicitudes_recuperacion.count(), 1)
        solicitud = self.user.solicitudes_recuperacion.first()
        self.assertEqual(solicitud.correo, "recuperable@itslibertad.edu.ec")
