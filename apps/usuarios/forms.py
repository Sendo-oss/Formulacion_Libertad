from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from .models import SolicitudRecuperacionContrasena, Usuario

DOMINIO_INSTITUCIONAL = "itslibertad.edu.ec"


class CorreoInstitucionalMixin:
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if email and not email.endswith(f"@{DOMINIO_INSTITUCIONAL}"):
            raise ValidationError(f"Solo se permite correo institucional @{DOMINIO_INSTITUCIONAL}.")
        return email

    def _configurar_email(self):
        if "email" in self.fields:
            self.fields["email"].help_text = f"Usa un correo institucional con dominio @{DOMINIO_INSTITUCIONAL}."
            self.fields["email"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"usuario@{DOMINIO_INSTITUCIONAL}",
                }
            )


class UsuarioCreationForm(CorreoInstitucionalMixin, forms.ModelForm):
    password_temporal = forms.CharField(
        label="Contrasena temporal",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa una contrasena temporal",
            }
        ),
        help_text="Esta contrasena sera temporal. El usuario debera cambiarla al iniciar sesion.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_email()
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password_temporal"])
        usuario.debe_cambiar_contrasena = True
        if commit:
            usuario.save()
        return usuario

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")


class UsuarioUpdateForm(CorreoInstitucionalMixin, UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_email()

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol", "is_active")


class SolicitudRecuperacionForm(forms.ModelForm):
    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        if not correo.endswith(f"@{DOMINIO_INSTITUCIONAL}"):
            raise ValidationError(f"Solo se permite correo institucional @{DOMINIO_INSTITUCIONAL}.")
        return correo

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
        fields = ("correo",)
        widgets = {
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": f"usuario@{DOMINIO_INSTITUCIONAL}",
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


class CambioContrasenaObligatorioForm(forms.Form):
    old_password = forms.CharField(
        label="Contrasena temporal actual",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="Nueva contrasena",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contrasena",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("La contrasena temporal actual no es correcta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        nueva = cleaned_data.get("new_password1")
        confirmacion = cleaned_data.get("new_password2")
        if nueva and confirmacion and nueva != confirmacion:
            raise ValidationError("La nueva contrasena y la confirmacion no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save(update_fields=["password"])
        return self.user


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
