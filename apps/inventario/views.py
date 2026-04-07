from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from openpyxl import Workbook
from utils.exporting import build_pdf_response

from apps.usuarios.models import Usuario

from .forms import MateriaPrimaForm
from .models import MateriaPrima


def puede_editar_materia(user, materia_prima=None):
    if not user.is_authenticated:
        return False
    if user.rol == Usuario.Rol.ADMINISTRADOR:
        return True
    if user.rol != Usuario.Rol.PROFESOR:
        return False
    if materia_prima is None:
        return True
    return materia_prima.registrado_por_id == user.id


class PuedeEditarInventarioMixin(UserPassesTestMixin):
    def test_func(self):
        materia_prima = None
        if hasattr(self, "get_object"):
            try:
                materia_prima = self.get_object()
            except Exception:
                materia_prima = None
        return puede_editar_materia(self.request.user, materia_prima)


class MateriaPrimaListView(LoginRequiredMixin, ListView):
    model = MateriaPrima
    template_name = "inventario/materiaprima_list.html"
    context_object_name = "materias_primas"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        termino = self.request.GET.get("q")
        estado = self.request.GET.get("estado")
        nivel_stock = self.request.GET.get("nivel_stock")
        if termino:
            queryset = queryset.filter(
                Q(nombre__icontains=termino)
                | Q(lote__icontains=termino)
                | Q(numero_cas__icontains=termino)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
        if nivel_stock == "sin_stock":
            queryset = queryset.filter(stock_actual=0)
        elif nivel_stock == "stock_bajo":
            queryset = queryset.filter(stock_actual__gt=0, stock_actual__lte=F("stock_minimo"))
        return queryset.select_related("registrado_por")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = MateriaPrima.Estado.choices
        return context

    def render_to_response(self, context, **response_kwargs):
        queryset = self.get_queryset()
        if self.request.GET.get("export") == "excel":
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Materias primas"
            sheet.append(
                [
                    "Nombre",
                    "CAS",
                    "EINECS",
                    "Lote",
                    "Fecha elaboracion",
                    "Fecha vencimiento",
                    "Control caducidad",
                    "Dias alerta vencimiento",
                    "Casa comercial",
                    "Stock actual",
                    "Stock minimo",
                    "Unidad",
                    "Estado",
                ]
            )
            for item in queryset:
                sheet.append(
                    [
                        item.nombre,
                        item.numero_cas,
                        item.numero_einecs,
                        item.lote,
                        str(item.fecha_elaboracion or ""),
                        str(item.fecha_vencimiento or "No caduca"),
                        "Si" if item.requiere_control_caducidad else "No",
                        item.dias_alerta_vencimiento,
                        item.casa_comercial,
                        float(item.stock_actual),
                        float(item.stock_minimo),
                        item.unidad_medida,
                        item.get_estado_display(),
                    ]
                )
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="materias_primas.xlsx"'
            workbook.save(response)
            return response
        if self.request.GET.get("export") == "pdf":
            rows = [
                [
                    item.nombre,
                    item.numero_cas or "-",
                    item.lote,
                    item.vencimiento_texto,
                    item.stock_actual,
                    item.unidad_medida,
                    item.get_estado_display(),
                ]
                for item in queryset
            ]
            return build_pdf_response(
                "materias_primas.pdf",
                "Reporte de materias primas",
                ["Nombre", "CAS", "Lote", "Vencimiento", "Stock", "Unidad", "Estado"],
                rows,
                subtitle="Listado exportado desde el sistema de formulacion magistral.",
                generated_by=self.request.user.get_full_name() or self.request.user.username,
            )
        return super().render_to_response(context, **response_kwargs)


class MateriaPrimaDetailView(LoginRequiredMixin, DetailView):
    model = MateriaPrima
    template_name = "inventario/materiaprima_detail.html"
    context_object_name = "materia_prima"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_editar"] = puede_editar_materia(self.request.user, self.object)
        return context

    def render_to_response(self, context, **response_kwargs):
        materia = self.get_object()
        if self.request.GET.get("export") == "pdf":
            rows = [
                ["Nombre", materia.nombre],
                ["CAS", materia.numero_cas or "-"],
                ["EINECS", materia.numero_einecs or "-"],
                ["Lote", materia.lote],
                ["Fecha elaboracion", materia.fecha_elaboracion or "-"],
                ["Fecha vencimiento", materia.vencimiento_texto],
                ["Control de caducidad", "Si" if materia.requiere_control_caducidad else "No"],
                ["Dias de anticipacion para alerta", materia.dias_alerta_vencimiento],
                ["Casa comercial", materia.casa_comercial or "-"],
                ["Stock actual", f"{materia.stock_actual} {materia.unidad_medida}"],
                ["Stock minimo", f"{materia.stock_minimo} {materia.unidad_medida}"],
                ["Estado", materia.get_estado_display()],
                ["Observaciones", materia.observaciones or "-"],
            ]
            return build_pdf_response(
                f"materia_prima_{materia.pk}.pdf",
                "Ficha de materia prima",
                ["Campo", "Valor"],
                rows,
                subtitle=f"Registro: {materia.nombre}",
                page_orientation="portrait",
                generated_by=self.request.user.get_full_name() or self.request.user.username,
            )
        return super().render_to_response(context, **response_kwargs)


class MateriaPrimaCreateView(LoginRequiredMixin, PuedeEditarInventarioMixin, CreateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    template_name = "inventario/materiaprima_form.html"
    success_url = reverse_lazy("inventario:lista")

    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        return super().form_valid(form)


class MateriaPrimaUpdateView(LoginRequiredMixin, PuedeEditarInventarioMixin, UpdateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    template_name = "inventario/materiaprima_form.html"
    success_url = reverse_lazy("inventario:lista")
