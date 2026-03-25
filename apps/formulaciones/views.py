from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView
from openpyxl import Workbook
from utils.exporting import build_pdf_response

from apps.usuarios.models import Usuario

from .forms import FormulacionDetalleFormSet, FormulacionForm
from .models import Formulacion


def puede_editar_formulacion(user, formulacion=None):
    if not user.is_authenticated:
        return False
    if user.rol == Usuario.Rol.ADMINISTRADOR:
        return True
    if user.rol != Usuario.Rol.PROFESOR:
        return False
    if formulacion is None:
        return True
    return formulacion.creado_por_id == user.id


class PuedeEditarFormulacionMixin(UserPassesTestMixin):
    def test_func(self):
        formulacion = None
        if hasattr(self, "get_object"):
            try:
                formulacion = self.get_object()
            except Exception:
                formulacion = None
        return puede_editar_formulacion(self.request.user, formulacion)


class FormulacionListView(LoginRequiredMixin, ListView):
    model = Formulacion
    template_name = "formulaciones/formulacion_list.html"
    context_object_name = "formulaciones"

    def get_queryset(self):
        queryset = super().get_queryset()
        termino = self.request.GET.get("q")
        categoria = self.request.GET.get("categoria")
        if termino:
            queryset = queryset.filter(Q(nombre__icontains=termino) | Q(codigo__icontains=termino))
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        return queryset.select_related("creado_por")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = (
            Formulacion.objects.exclude(categoria__exact="")
            .order_by("categoria")
            .values_list("categoria", flat=True)
            .distinct()
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        queryset = self.get_queryset().prefetch_related("detalles__materia_prima")
        if self.request.GET.get("export") == "excel":
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Formulaciones"
            sheet.append(
                [
                    "Codigo",
                    "Nombre",
                    "Categoria",
                    "Tipo",
                    "Origen",
                    "Estado",
                    "Referencia",
                    "Componentes",
                ]
            )
            for formulacion in queryset:
                componentes = ", ".join(
                    f"{d.orden}. {d.materia_prima.nombre} ({d.cantidad} {d.unidad_medida})"
                    for d in formulacion.detalles.all()
                )
                sheet.append(
                    [
                        formulacion.codigo,
                        formulacion.nombre,
                        formulacion.get_categoria_display(),
                        formulacion.tipo_formulacion,
                        formulacion.get_origen_display(),
                        formulacion.get_estado_display(),
                        formulacion.fuente_referencia,
                        componentes,
                    ]
                )
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="formulaciones.xlsx"'
            workbook.save(response)
            return response
        if self.request.GET.get("export") == "pdf":
            rows = []
            for formulacion in queryset:
                componentes = ", ".join(
                    f"{d.orden}. {d.materia_prima.nombre} ({d.cantidad} {d.unidad_medida})"
                    for d in formulacion.detalles.all()
                )
                rows.append(
                    [
                        formulacion.codigo,
                        formulacion.nombre,
                        formulacion.get_categoria_display(),
                        formulacion.get_estado_display(),
                        componentes,
                    ]
                )
            return build_pdf_response(
                "formulaciones.pdf",
                "Reporte de formulaciones",
                ["Codigo", "Nombre", "Categoria", "Estado", "Componentes"],
                rows,
                subtitle="Listado exportado desde el sistema de formulacion magistral.",
                generated_by=self.request.user.get_full_name() or self.request.user.username,
            )
        return super().render_to_response(context, **response_kwargs)


class FormulacionDetailView(LoginRequiredMixin, DetailView):
    model = Formulacion
    template_name = "formulaciones/formulacion_detail.html"
    context_object_name = "formulacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_editar"] = puede_editar_formulacion(self.request.user, self.object)
        return context

    def render_to_response(self, context, **response_kwargs):
        formulacion = self.get_object()
        if self.request.GET.get("export") == "pdf":
            rows = [
                ["Codigo", formulacion.codigo],
                ["Nombre", formulacion.nombre],
                ["Categoria", formulacion.get_categoria_display()],
                ["Tipo", formulacion.tipo_formulacion],
                ["Origen", formulacion.get_origen_display()],
                ["Referencia", formulacion.fuente_referencia or "-"],
                ["Estado", formulacion.get_estado_display()],
                ["Descripcion", formulacion.descripcion or "-"],
                ["Observaciones", formulacion.observaciones or "-"],
            ]
            for detalle in formulacion.detalles.select_related("materia_prima").all():
                rows.append(
                    [
                        f"Componente {detalle.orden}",
                        f"{detalle.materia_prima.nombre} - {detalle.cantidad} {detalle.unidad_medida}",
                    ]
                )
            return build_pdf_response(
                f"formulacion_{formulacion.pk}.pdf",
                "Ficha de formulacion",
                ["Campo", "Valor"],
                rows,
                subtitle=f"Registro: {formulacion.codigo} - {formulacion.nombre}",
                page_orientation="portrait",
                generated_by=self.request.user.get_full_name() or self.request.user.username,
            )
        return super().render_to_response(context, **response_kwargs)


class FormulacionBaseEditView(LoginRequiredMixin, PuedeEditarFormulacionMixin, View):
    template_name = "formulaciones/formulacion_form.html"
    object = None

    def get_object(self):
        return None

    def get_success_message(self):
        return "Formulacion registrada correctamente."

    def get_success_url(self):
        return redirect("formulaciones:detalle", pk=self.object.pk)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(
            request,
            self.template_name,
            self.get_context_data(),
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormulacionForm(request.POST, instance=self.object)
        formset = FormulacionDetalleFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                formulacion = form.save(commit=False)
                if not formulacion.pk:
                    formulacion.creado_por = request.user
                formulacion.save()
                formset.instance = formulacion
                formset.save()
                self.object = formulacion
            messages.success(request, self.get_success_message())
            return self.get_success_url()
        return render(request, self.template_name, self.get_context_data(form=form, formset=formset))

    def get_context_data(self, form=None, formset=None):
        return {
            "form": form or FormulacionForm(instance=self.object),
            "formset": formset or FormulacionDetalleFormSet(instance=self.object),
            "object": self.object,
        }


class FormulacionCreateView(FormulacionBaseEditView):
    def get_success_message(self):
        return "Formulacion registrada correctamente."


class FormulacionUpdateView(FormulacionBaseEditView):
    def get_object(self):
        return get_object_or_404(Formulacion, pk=self.kwargs["pk"])

    def get_success_message(self):
        return "Formulacion actualizada correctamente."


class FormulacionCambiarEstadoView(LoginRequiredMixin, PuedeEditarFormulacionMixin, View):
    estado_destino = None

    def get_object(self):
        return get_object_or_404(Formulacion, pk=self.kwargs["pk"])

    def post(self, request, pk):
        formulacion = self.get_object()
        formulacion.estado = self.estado_destino
        formulacion.save(update_fields=["estado", "actualizado_en"])
        messages.success(request, f"Estado actualizado a {formulacion.get_estado_display().lower()}.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", formulacion.get_absolute_url() if hasattr(formulacion, "get_absolute_url") else f"/formulaciones/{formulacion.pk}/"))


class FormulacionActivarView(FormulacionCambiarEstadoView):
    estado_destino = Formulacion.Estado.ACTIVA


class FormulacionDesactivarView(FormulacionCambiarEstadoView):
    estado_destino = Formulacion.Estado.INACTIVA
