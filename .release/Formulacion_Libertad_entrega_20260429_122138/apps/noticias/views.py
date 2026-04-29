from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.usuarios.models import Usuario
from apps.usuarios.services import registrar_historial

from .forms import NoticiaForm
from .models import Noticia


class PuedeGestionarNoticiasMixin(UserPassesTestMixin):
    def test_func(self):
        noticia = None
        if hasattr(self, "get_object"):
            try:
                noticia = self.get_object()
            except Exception:
                noticia = None
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.rol == Usuario.Rol.ADMINISTRADOR:
            return True
        if self.request.user.rol != Usuario.Rol.PROFESOR:
            return False
        if noticia is None:
            return True
        return noticia.creada_por_id == self.request.user.id


class NoticiaListView(LoginRequiredMixin, ListView):
    model = Noticia
    template_name = "noticias/noticia_list.html"
    context_object_name = "noticias"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().select_related("creada_por")
        if self.request.user.rol == Usuario.Rol.ESTUDIANTE:
            queryset = queryset.filter(activa=True)
        termino = self.request.GET.get("q")
        if termino:
            queryset = queryset.filter(
                Q(titulo__icontains=termino)
                | Q(resumen__icontains=termino)
                | Q(contenido__icontains=termino)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_gestionar"] = self.request.user.rol in {Usuario.Rol.ADMINISTRADOR, Usuario.Rol.PROFESOR}
        return context


class NoticiaDetailView(LoginRequiredMixin, DetailView):
    model = Noticia
    template_name = "noticias/noticia_detail.html"
    context_object_name = "noticia"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("creada_por")
        if self.request.user.rol == Usuario.Rol.ESTUDIANTE:
            queryset = queryset.filter(activa=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_editar"] = (
            self.request.user.rol == Usuario.Rol.ADMINISTRADOR
            or self.object.creada_por_id == self.request.user.id
        )
        return context


class NoticiaCreateView(LoginRequiredMixin, PuedeGestionarNoticiasMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = "noticias/noticia_form.html"
    success_url = reverse_lazy("noticias:lista")

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        response = super().form_valid(form)
        registrar_historial(
            self.request.user,
            "Noticias",
            "Creación de noticia",
            f"Se publicó la noticia '{self.object.titulo}'.",
            entidad=self.object.titulo,
        )
        return response


class NoticiaUpdateView(LoginRequiredMixin, PuedeGestionarNoticiasMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = "noticias/noticia_form.html"
    success_url = reverse_lazy("noticias:lista")

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_historial(
            self.request.user,
            "Noticias",
            "Actualización de noticia",
            f"Se actualizó la noticia '{self.object.titulo}'.",
            entidad=self.object.titulo,
        )
        return response


class NoticiaDeleteView(LoginRequiredMixin, PuedeGestionarNoticiasMixin, View):
    def get_object(self):
        return get_object_or_404(Noticia, pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        noticia = self.get_object()
        titulo = noticia.titulo
        noticia.delete()
        registrar_historial(
            request.user,
            "Noticias",
            "Eliminación de noticia",
            f"Se eliminó la noticia '{titulo}'.",
            entidad=titulo,
        )
        messages.success(request, "La noticia fue eliminada correctamente.")
        return redirect("noticias:lista")
