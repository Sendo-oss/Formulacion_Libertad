from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import SolicitudRecuperacionContrasena, Usuario

DOMINIO_INSTITUCIONAL = "itslibertad.edu.ec"


class CorreoInstitucionalMixin:
    def clean_correo_usuario(self):
        local = (self.cleaned_data.get("correo_usuario") or "").strip().lower()
        if not local:
            raise ValidationError("Debes ingresar el identificador del correo institucional.")
        if "@" in local or " " in local:
            raise ValidationError(f"Ingresa solo la parte anterior a @{DOMINIO_INSTITUCIONAL}.")
        return local

    def _construir_correo(self):
        return f"{self.cleaned_data['correo_usuario']}@{DOMINIO_INSTITUCIONAL}"

    def _configurar_correo_usuario(self):
        if "correo_usuario" in self.fields:
            self.fields["correo_usuario"].help_text = (
                f"El sistema agregará automáticamente @{DOMINIO_INSTITUCIONAL}."
            )
            self.fields["correo_usuario"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "usuario",
                }
            )


class UsuarioCreationForm(CorreoInstitucionalMixin, forms.ModelForm):
    correo_usuario = forms.CharField(label="Correo institucional")
    password_temporal = forms.CharField(
        label="Contraseña temporal",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa una contraseña temporal",
            }
        ),
        help_text="Esta contraseña será temporal. El usuario deberá cambiarla al iniciar sesión.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_correo_usuario()
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self._construir_correo()
        usuario.set_password(self.cleaned_data["password_temporal"])
        usuario.debe_cambiar_contrasena = True
        if commit:
            usuario.save()
        return usuario

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "rol")


class UsuarioUpdateForm(CorreoInstitucionalMixin, UserChangeForm):
    correo_usuario = forms.CharField(label="Correo institucional")
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_correo_usuario()
        if self.instance and self.instance.email:
            self.fields["correo_usuario"].initial = self.instance.email.split("@", 1)[0]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self._construir_correo()
        if commit:
            usuario.save()
        return usuario

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "rol", "is_active")


class SolicitudRecuperacionForm(forms.ModelForm):
    correo_usuario = forms.CharField(label="Correo institucional")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["correo_usuario"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "usuario",
            }
        )
        self.fields["correo_usuario"].help_text = (
            f"El sistema agregará automáticamente @{DOMINIO_INSTITUCIONAL}."
        )

    def clean_correo_usuario(self):
        local = (self.cleaned_data.get("correo_usuario") or "").strip().lower()
        if not local:
            raise ValidationError("Debes ingresar el identificador del correo institucional.")
        if "@" in local or " " in local:
            raise ValidationError(f"Ingresa solo la parte anterior a @{DOMINIO_INSTITUCIONAL}.")
        return local

    def clean(self):
        cleaned_data = super().clean()
        local = cleaned_data.get("correo_usuario")
        correo = f"{local}@{DOMINIO_INSTITUCIONAL}" if local else None
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

    def save(self, commit=True):
        self.instance.correo = f"{self.cleaned_data['correo_usuario']}@{DOMINIO_INSTITUCIONAL}"
        return super().save(commit=commit)

    class Meta:
        model = SolicitudRecuperacionContrasena
        fields = ()


class SolicitudRecuperacionGestionForm(forms.ModelForm):
    nueva_contrasena = forms.CharField(
        required=False,
        label="Nueva contraseña temporal",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa la nueva contraseña temporal",
            }
        ),
    )
    confirmar_contrasena = forms.CharField(
        required=False,
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repite la nueva contraseña temporal",
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
                raise ValidationError("La nueva contraseña y su confirmación no coinciden.")

        if estado == SolicitudRecuperacionContrasena.Estado.ATENDIDA:
            if not usuario:
                raise ValidationError("No se puede marcar como atendida sin un usuario relacionado.")
            if not nueva_contrasena:
                raise ValidationError("Para marcar la solicitud como atendida debes asignar una nueva contraseña temporal.")

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
        label="Contraseña temporal actual",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("La contraseña temporal actual no es correcta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        nueva = cleaned_data.get("new_password1")
        confirmacion = cleaned_data.get("new_password2")
        if nueva and confirmacion and nueva != confirmacion:
            raise ValidationError("La nueva contraseña y la confirmación no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save(update_fields=["password"])
        return self.user


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Usuario no existe o la contraseña es incorrecta.",
        "inactive": "Esta cuenta está inactiva. Contacta al administrador.",
    }

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
