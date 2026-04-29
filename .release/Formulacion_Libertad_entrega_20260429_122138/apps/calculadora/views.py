from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import EscaladoFormulacionForm


def redondear(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class CalculadoraView(LoginRequiredMixin, View):
    template_name = "calculadora/inicio.html"

    def get(self, request):
        formulacion_id = request.GET.get("formulacion")
        escalado_initial = {"formulacion": formulacion_id} if formulacion_id else None
        return render(
            request,
            self.template_name,
            {
                "escalado_form": EscaladoFormulacionForm(initial=escalado_initial),
            },
        )

    def post(self, request):
        context = {
            "escalado_form": EscaladoFormulacionForm(),
        }

        form = EscaladoFormulacionForm(request.POST)
        context["escalado_form"] = form
        if form.is_valid():
            formulacion = form.cleaned_data["formulacion"]
            cantidad_objetivo = form.cleaned_data["cantidad_objetivo"]
            unidad_objetivo = form.cleaned_data["unidad_objetivo"]
            detalles = list(formulacion.detalles.select_related("materia_prima").all())
            total_base = sum((detalle.cantidad for detalle in detalles), Decimal("0.00"))
            usa_base_100 = any(detalle.unidad_medida == "%" for detalle in detalles)
            componentes = []
            total_ajustado = Decimal("0.00")
            if total_base > 0:
                for detalle in detalles:
                    cantidad_ajustada = redondear((detalle.cantidad / total_base) * cantidad_objetivo)
                    unidad_resultado = unidad_objetivo if detalle.unidad_medida == "%" else detalle.unidad_medida
                    total_ajustado += cantidad_ajustada
                    componentes.append(
                        {
                            "orden": detalle.orden,
                            "materia_prima": detalle.materia_prima.nombre,
                            "cantidad_base": detalle.cantidad,
                            "unidad_base": detalle.unidad_medida,
                            "cantidad_ajustada": cantidad_ajustada,
                            "unidad_resultado": unidad_resultado,
                        }
                    )
            context["resultado_escalado"] = {
                "formulacion": formulacion,
                "cantidad_objetivo": cantidad_objetivo,
                "unidad_objetivo": unidad_objetivo,
                "total_base": total_base,
                "total_ajustado": total_ajustado,
                "usa_base_100": usa_base_100,
                "componentes": componentes,
            }

        return render(request, self.template_name, context)
