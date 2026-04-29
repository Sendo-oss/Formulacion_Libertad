from django import forms

from .models import MateriaPrima


class MateriaPrimaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)

    class Meta:
        model = MateriaPrima
        exclude = ("registrado_por",)
        widgets = {
            "fecha_elaboracion": forms.DateInput(attrs={"type": "date"}),
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
            "dias_alerta_vencimiento": forms.NumberInput(attrs={"min": "0"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "requiere_control_caducidad": "Desmarca esta opcion si la materia prima no caduca.",
            "dias_alerta_vencimiento": "Cantidad de dias antes del vencimiento en que debe generarse la alerta.",
        }
