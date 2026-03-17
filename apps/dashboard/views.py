from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView
from datetime import timedelta

from apps.alertas.models import Alerta
from apps.formulaciones.models import Formulacion
from apps.inventario.models import MateriaPrima


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        context["total_materias_primas"] = MateriaPrima.objects.count()
        context["total_formulaciones"] = Formulacion.objects.count()
        context["materias_por_vencer"] = MateriaPrima.objects.filter(
            requiere_control_caducidad=True,
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=hoy + timedelta(days=30),
        ).count()
        context["materias_sin_stock"] = MateriaPrima.objects.filter(stock_actual=0).count()
        context["alertas_activas"] = Alerta.objects.filter(estado=Alerta.Estado.ACTIVA)[:10]
        return context
