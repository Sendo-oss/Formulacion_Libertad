from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")


class UsuarioUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol", "is_active")
