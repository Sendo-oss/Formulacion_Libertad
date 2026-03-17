from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import DosisPesoForm, EscaladoFormulacionForm, ReglaTresDosisForm


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
                "regla_tres_form": ReglaTresDosisForm(),
                "dosis_peso_form": DosisPesoForm(),
                "escalado_form": EscaladoFormulacionForm(initial=escalado_initial),
                "active_tab": request.GET.get("tab", "regla_tres"),
            },
        )

    def post(self, request):
        action = request.POST.get("action", "regla_tres")
        context = {
            "regla_tres_form": ReglaTresDosisForm(),
            "dosis_peso_form": DosisPesoForm(),
            "escalado_form": EscaladoFormulacionForm(),
            "active_tab": action,
        }

        if action == "regla_tres":
            form = ReglaTresDosisForm(request.POST)
            context["regla_tres_form"] = form
            if form.is_valid():
                dosis = form.cleaned_data["dosis_requerida_mg"]
                mg_disponible = form.cleaned_data["concentracion_disponible_mg"]
                ml_disponible = form.cleaned_data["volumen_disponible_ml"]
                ml_resultado = redondear((dosis * ml_disponible) / mg_disponible)
                context["resultado_regla_tres"] = {
                    "dosis_mg": dosis,
                    "mg_disponible": mg_disponible,
                    "ml_disponible": ml_disponible,
                    "ml_resultado": ml_resultado,
                }

        elif action == "dosis_peso":
            form = DosisPesoForm(request.POST)
            context["dosis_peso_form"] = form
            if form.is_valid():
                peso = form.cleaned_data["peso_kg"]
                dosis_mg_kg = form.cleaned_data["dosis_mg_kg"]
                mg_disponible = form.cleaned_data["concentracion_disponible_mg"]
                ml_disponible = form.cleaned_data["volumen_disponible_ml"]
                dosis_total = redondear(peso * dosis_mg_kg)
                ml_resultado = redondear((dosis_total * ml_disponible) / mg_disponible)
                context["resultado_dosis_peso"] = {
                    "peso": peso,
                    "dosis_mg_kg": dosis_mg_kg,
                    "dosis_total": dosis_total,
                    "ml_resultado": ml_resultado,
                }

        elif action == "escalado":
            form = EscaladoFormulacionForm(request.POST)
            context["escalado_form"] = form
            if form.is_valid():
                formulacion = form.cleaned_data["formulacion"]
                cantidad_objetivo = form.cleaned_data["cantidad_objetivo"]
                unidad_objetivo = form.cleaned_data["unidad_objetivo"]
                detalles = list(formulacion.detalles.select_related("materia_prima").all())
                total_base = sum((detalle.cantidad for detalle in detalles), Decimal("0.00"))
                componentes = []
                if total_base > 0:
                    for detalle in detalles:
                        cantidad_ajustada = redondear((detalle.cantidad / total_base) * cantidad_objetivo)
                        unidad_resultado = unidad_objetivo if detalle.unidad_medida == "%" else detalle.unidad_medida
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
                    "componentes": componentes,
                }

        return render(request, self.template_name, context)
