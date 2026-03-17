from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import UsuarioCreationForm, UsuarioUpdateForm
from .models import Usuario


class SoloAdministradorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == Usuario.Rol.ADMINISTRADOR


class UsuarioListView(LoginRequiredMixin, SoloAdministradorMixin, ListView):
    model = Usuario
    template_name = "usuarios/usuario_list.html"
    context_object_name = "usuarios"


class UsuarioCreateView(LoginRequiredMixin, SoloAdministradorMixin, CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = "usuarios/usuario_form.html"
    success_url = reverse_lazy("usuarios:lista")


class UsuarioUpdateView(LoginRequiredMixin, SoloAdministradorMixin, UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = "usuarios/usuario_form.html"
    success_url = reverse_lazy("usuarios:lista")
