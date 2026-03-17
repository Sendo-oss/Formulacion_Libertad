from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Formulacion, FormulacionDetalle


class FormulacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)

    class Meta:
        model = Formulacion
        exclude = ("creado_por",)
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "codigo": "Usa el codigo institucional o uno interno unico.",
            "fuente_referencia": "Ejemplo: Formulario Nacional 2003 o referencia docente.",
        }


class BaseFormulacionDetalleFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        detalles_validos = 0
        materias = set()

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            materia = form.cleaned_data.get("materia_prima")
            cantidad = form.cleaned_data.get("cantidad")
            unidad = form.cleaned_data.get("unidad_medida")

            if materia or cantidad or unidad:
                if not (materia and cantidad and unidad):
                    raise ValidationError("Cada componente debe tener materia prima, cantidad y unidad de medida.")
                if materia.pk in materias:
                    raise ValidationError("No puedes repetir la misma materia prima dentro de una formulacion.")
                materias.add(materia.pk)
                detalles_validos += 1

        if detalles_validos == 0:
            raise ValidationError("Debes registrar al menos un componente en la formulacion.")


FormulacionDetalleFormSet = inlineformset_factory(
    Formulacion,
    FormulacionDetalle,
    fields=("materia_prima", "cantidad", "unidad_medida", "orden"),
    extra=1,
    can_delete=True,
    formset=BaseFormulacionDetalleFormSet,
    widgets={
        "materia_prima": forms.Select(attrs={"class": "form-select"}),
        "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "unidad_medida": forms.TextInput(attrs={"class": "form-control"}),
        "orden": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    },
)
