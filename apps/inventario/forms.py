from django import forms

from .models import MateriaPrima


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        exclude = ("registrado_por",)
        widgets = {
            "fecha_elaboracion": forms.DateInput(attrs={"type": "date"}),
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "requiere_control_caducidad": "Desmarca esta opcion si la materia prima no caduca.",
        }
