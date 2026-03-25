from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.usuarios.models import Usuario
from apps.usuarios.services import registrar_historial

from .forms import DocumentoTecnicoForm
from .models import DocumentoTecnico


class PuedeGestionarDocumentacionMixin(UserPassesTestMixin):
    def test_func(self):
        documento = None
        if hasattr(self, "get_object"):
            try:
                documento = self.get_object()
            except Exception:
                documento = None
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.rol == Usuario.Rol.ADMINISTRADOR:
            return True
        if self.request.user.rol != Usuario.Rol.PROFESOR:
            return False
        if documento is None:
            return True
        return documento.subido_por_id == self.request.user.id


class DocumentoTecnicoListView(LoginRequiredMixin, ListView):
    model = DocumentoTecnico
    template_name = "documentacion/documento_list.html"
    context_object_name = "documentos"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("subido_por", "formulacion")
        termino = self.request.GET.get("q")
        tipo = self.request.GET.get("tipo")
        formulacion = self.request.GET.get("formulacion")
        if termino:
            queryset = queryset.filter(
                Q(titulo__icontains=termino)
                | Q(descripcion__icontains=termino)
                | Q(formulacion__nombre__icontains=termino)
            )
        if tipo:
            queryset = queryset.filter(tipo_documento=tipo)
        if formulacion:
            queryset = queryset.filter(formulacion_id=formulacion)
        return queryset

    def get_context_data(self, **kwargs):
        from apps.formulaciones.models import Formulacion

        context = super().get_context_data(**kwargs)
        context["tipos_documento"] = DocumentoTecnico.TipoDocumento.choices
        context["puede_subir"] = self.request.user.rol in {Usuario.Rol.ADMINISTRADOR, Usuario.Rol.PROFESOR}
        context["formulaciones"] = Formulacion.objects.order_by("codigo", "nombre")
        documentos = context["documentos"]
        context["documentos_ficha_tecnica"] = [
            documento
            for documento in documentos
            if documento.tipo_documento == DocumentoTecnico.TipoDocumento.FICHA_TECNICA
        ]
        context["documentos_procedimiento"] = [
            documento
            for documento in documentos
            if documento.tipo_documento == DocumentoTecnico.TipoDocumento.PROCEDIMIENTO
        ]
        return context


class DocumentoTecnicoDetailView(LoginRequiredMixin, DetailView):
    model = DocumentoTecnico
    template_name = "documentacion/documento_detail.html"
    context_object_name = "documento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_gestionar"] = (
            self.request.user.rol == Usuario.Rol.ADMINISTRADOR
            or self.object.subido_por_id == self.request.user.id
        )
        return context


class DocumentoTecnicoCreateView(LoginRequiredMixin, PuedeGestionarDocumentacionMixin, CreateView):
    model = DocumentoTecnico
    form_class = DocumentoTecnicoForm
    template_name = "documentacion/documento_form.html"
    success_url = reverse_lazy("documentacion:lista")

    def form_valid(self, form):
        form.instance.subido_por = self.request.user
        response = super().form_valid(form)
        registrar_historial(
            self.request.user,
            "Documentacion tecnica",
            "Carga de documento",
            f"Se subio el documento '{self.object.titulo}'.",
            entidad=self.object.titulo,
        )
        return response


class DocumentoTecnicoUpdateView(LoginRequiredMixin, PuedeGestionarDocumentacionMixin, UpdateView):
    model = DocumentoTecnico
    form_class = DocumentoTecnicoForm
    template_name = "documentacion/documento_form.html"
    success_url = reverse_lazy("documentacion:lista")

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_historial(
            self.request.user,
            "Documentacion tecnica",
            "Actualizacion de documento",
            f"Se actualizo el documento '{self.object.titulo}'.",
            entidad=self.object.titulo,
        )
        return response


class DocumentoTecnicoDeleteView(LoginRequiredMixin, PuedeGestionarDocumentacionMixin, View):
    def get_object(self):
        return get_object_or_404(DocumentoTecnico, pk=self.kwargs["pk"])

    def post(self, request, pk, *args, **kwargs):
        documento = self.get_object()
        titulo = documento.titulo
        documento.delete()
        registrar_historial(
            request.user,
            "Documentacion tecnica",
            "Eliminacion de documento",
            f"Se elimino el documento '{titulo}'.",
            entidad=titulo,
        )
        messages.success(request, "El documento fue eliminado correctamente.")
        return redirect("documentacion:lista")
