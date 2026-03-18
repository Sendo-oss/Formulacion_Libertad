from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import (
    CambioContrasenaObligatorioForm,
    SolicitudRecuperacionForm,
    SolicitudRecuperacionGestionForm,
    UsuarioCreationForm,
    UsuarioUpdateForm,
)
from .models import SolicitudRecuperacionContrasena, Usuario


class SoloAdministradorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == Usuario.Rol.ADMINISTRADOR


class UsuarioListView(LoginRequiredMixin, SoloAdministradorMixin, ListView):
    model = Usuario
    template_name = "usuarios/usuario_list.html"
    context_object_name = "usuarios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solicitudes_pendientes"] = SolicitudRecuperacionContrasena.objects.filter(
            estado=SolicitudRecuperacionContrasena.Estado.PENDIENTE
        ).count()
        context["usuarios_con_cambio_pendiente"] = Usuario.objects.filter(debe_cambiar_contrasena=True).count()
        return context


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


class SolicitudRecuperacionCreateView(CreateView):
    model = SolicitudRecuperacionContrasena
    form_class = SolicitudRecuperacionForm
    template_name = "auth/password_reset_form.html"
    success_url = reverse_lazy("usuarios:recuperacion_enviada")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        correo = form.cleaned_data["correo"]
        usuario = Usuario.objects.filter(email__iexact=correo).order_by("id").first()
        form.instance.correo = correo
        form.instance.usuario = usuario
        messages.success(
            self.request,
            "Tu solicitud fue registrada. Un administrador revisara el caso y te ayudara a restablecer el acceso.",
        )
        return super().form_valid(form)


class SolicitudRecuperacionDoneView(TemplateView):
    template_name = "auth/password_reset_done.html"


class SolicitudRecuperacionListView(LoginRequiredMixin, SoloAdministradorMixin, ListView):
    model = SolicitudRecuperacionContrasena
    template_name = "usuarios/solicitud_recuperacion_list.html"
    context_object_name = "solicitudes"


class SolicitudRecuperacionUpdateView(LoginRequiredMixin, SoloAdministradorMixin, UpdateView):
    model = SolicitudRecuperacionContrasena
    form_class = SolicitudRecuperacionGestionForm
    template_name = "usuarios/solicitud_recuperacion_form.html"
    success_url = reverse_lazy("usuarios:recuperaciones")

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        nueva_contrasena = form.cleaned_data.get("nueva_contrasena")

        if nueva_contrasena and solicitud.usuario:
            solicitud.usuario.set_password(nueva_contrasena)
            solicitud.usuario.debe_cambiar_contrasena = True
            solicitud.usuario.save(update_fields=["password", "debe_cambiar_contrasena"])

        if solicitud.estado in {
            SolicitudRecuperacionContrasena.Estado.ATENDIDA,
            SolicitudRecuperacionContrasena.Estado.RECHAZADA,
        }:
            solicitud.fecha_atencion = timezone.now()
            solicitud.atendida_por = self.request.user
        else:
            solicitud.fecha_atencion = None
            solicitud.atendida_por = None
        solicitud.save()
        messages.success(self.request, "La solicitud fue actualizada correctamente.")
        return redirect(self.success_url)


class SolicitudRecuperacionDeleteView(LoginRequiredMixin, SoloAdministradorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        solicitud = get_object_or_404(SolicitudRecuperacionContrasena, pk=pk)
        solicitud.delete()
        messages.success(request, "La solicitud fue eliminada correctamente.")
        return redirect("usuarios:recuperaciones")


class CambioContrasenaObligatorioView(LoginRequiredMixin, PasswordChangeView):
    form_class = CambioContrasenaObligatorioForm
    template_name = "usuarios/cambiar_contrasena.html"
    success_url = reverse_lazy("usuarios:cambio_contrasena_completado")

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, "debe_cambiar_contrasena", False):
            return redirect("dashboard:inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.debe_cambiar_contrasena = False
        self.request.user.save(update_fields=["debe_cambiar_contrasena"])
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, "Tu contrasena fue actualizada correctamente.")
        return response


class CambioContrasenaCompletadoView(TemplateView):
    template_name = "usuarios/cambiar_contrasena_ok.html"
