from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import SolicitudRecuperacionContrasena, Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")


class UsuarioUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol", "is_active")


class SolicitudRecuperacionForm(forms.ModelForm):
    def clean_correo(self):
        return self.cleaned_data["correo"].strip().lower()

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        if correo:
            solicitudes_activas = SolicitudRecuperacionContrasena.objects.filter(
                correo__iexact=correo,
                estado=SolicitudRecuperacionContrasena.Estado.PENDIENTE,
            ).count()
            if solicitudes_activas >= 2:
                raise ValidationError(
                    "Este correo ya tiene 2 solicitudes pendientes. Espera a que el administrador revise alguna antes de enviar otra."
                )
        return cleaned_data

    class Meta:
        model = SolicitudRecuperacionContrasena
        fields = ("correo", "observaciones")
        widgets = {
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "correo@institucion.edu.ec",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Si deseas, indica tu nombre o alguna referencia para que el administrador te identifique.",
                }
            ),
        }


class SolicitudRecuperacionGestionForm(forms.ModelForm):
    nueva_contrasena = forms.CharField(
        required=False,
        label="Nueva contrasena temporal",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa la nueva contrasena temporal",
            }
        ),
    )
    confirmar_contrasena = forms.CharField(
        required=False,
        label="Confirmar nueva contrasena",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repite la nueva contrasena temporal",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        nueva_contrasena = cleaned_data.get("nueva_contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
        usuario = self.instance.usuario

        if nueva_contrasena or confirmar_contrasena:
            if nueva_contrasena != confirmar_contrasena:
                raise ValidationError("La nueva contrasena y su confirmacion no coinciden.")
            if len(nueva_contrasena) < 8:
                raise ValidationError("La nueva contrasena debe tener al menos 8 caracteres.")

        if estado == SolicitudRecuperacionContrasena.Estado.ATENDIDA:
            if not usuario:
                raise ValidationError("No se puede marcar como atendida sin un usuario relacionado.")
            if not nueva_contrasena:
                raise ValidationError("Para marcar la solicitud como atendida debes asignar una nueva contrasena temporal.")

        return cleaned_data

    class Meta:
        model = SolicitudRecuperacionContrasena
        fields = ("estado", "observaciones")
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class CambioContrasenaObligatorioForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "autocapitalize": "none",
                "spellcheck": "false",
                "placeholder": "Ingresa tu usuario",
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Contraseña",
            }
        ),
    )
