from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView
from openpyxl import Workbook
from utils.exporting import build_pdf_response

from apps.usuarios.models import Usuario

from .models import Alerta


class PuedeVerAlertasMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.rol in {Usuario.Rol.ADMINISTRADOR, Usuario.Rol.PROFESOR}
        )


class AlertaListView(LoginRequiredMixin, PuedeVerAlertasMixin, ListView):
    model = Alerta
    template_name = "alertas/alerta_list.html"
    context_object_name = "alertas"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        prioridad = self.request.GET.get("prioridad")
        estado = self.request.GET.get("estado")
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset.select_related("materia_prima")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prioridades"] = Alerta.Prioridad.choices
        context["estados"] = Alerta.Estado.choices
        return context

    def render_to_response(self, context, **response_kwargs):
        queryset = self.get_queryset()
        if self.request.GET.get("export") == "excel":
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Alertas"
            sheet.append(
                [
                    "Tipo",
                    "Materia prima",
                    "Mensaje",
                    "Prioridad",
                    "Estado",
                    "Fecha generacion",
                    "Atendida por",
                    "Fecha atencion",
                ]
            )
            for alerta in queryset:
                sheet.append(
                    [
                        alerta.get_tipo_alerta_display(),
                        alerta.materia_prima.nombre,
                        alerta.mensaje,
                        alerta.get_prioridad_display(),
                        alerta.get_estado_display(),
                        str(alerta.fecha_generacion),
                        str(alerta.atendida_por or ""),
                        str(alerta.fecha_atencion or ""),
                    ]
                )
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="alertas.xlsx"'
            workbook.save(response)
            return response
        if self.request.GET.get("export") == "pdf":
            rows = [
                [
                    alerta.get_tipo_alerta_display(),
                    alerta.materia_prima.nombre,
                    alerta.get_prioridad_display(),
                    alerta.get_estado_display(),
                    alerta.fecha_generacion,
                ]
                for alerta in queryset
            ]
            return build_pdf_response(
                "alertas.pdf",
                "Reporte de alertas",
                ["Tipo", "Materia prima", "Prioridad", "Estado", "Fecha"],
                rows,
                subtitle="Listado exportado desde el sistema de formulacion magistral.",
                generated_by=self.request.user.get_full_name() or self.request.user.username,
            )
        return super().render_to_response(context, **response_kwargs)


class AlertaDetailView(LoginRequiredMixin, PuedeVerAlertasMixin, DetailView):
    model = Alerta
    template_name = "alertas/alerta_detail.html"
    context_object_name = "alerta"


class AlertaCambiarEstadoView(LoginRequiredMixin, PuedeVerAlertasMixin, View):
    estado_destino = None

    def post(self, request, pk):
        alerta = get_object_or_404(Alerta, pk=pk)
        alerta.estado = self.estado_destino
        alerta.atendida_por = request.user
        alerta.fecha_atencion = timezone.now()
        alerta.save(update_fields=["estado", "atendida_por", "fecha_atencion"])
        messages.success(request, f"Alerta actualizada a {alerta.get_estado_display().lower()}.")
        return redirect("alertas:detalle", pk=alerta.pk)


class AlertaMarcarRevisadaView(AlertaCambiarEstadoView):
    estado_destino = Alerta.Estado.REVISADA


class AlertaCerrarView(AlertaCambiarEstadoView):
    estado_destino = Alerta.Estado.CERRADA
