from decimal import Decimal

from django import forms

from apps.formulaciones.models import Formulacion


class StyledFormMixin:
    def _apply_styles(self):
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)


class EscaladoFormulacionForm(StyledFormMixin, forms.Form):
    formulacion = forms.ModelChoiceField(
        queryset=Formulacion.objects.filter(estado=Formulacion.Estado.ACTIVA).order_by("codigo"),
        label="Formulación",
    )
    cantidad_objetivo = forms.DecimalField(label="Cantidad final deseada", min_value=Decimal("0.01"))
    unidad_objetivo = forms.CharField(label="Unidad final", initial="g", max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_styles()
