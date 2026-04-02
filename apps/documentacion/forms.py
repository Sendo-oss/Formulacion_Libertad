from django import forms

from .models import DocumentoTecnico


class DocumentoTecnicoForm(forms.ModelForm):
    class Meta:
        model = DocumentoTecnico
        fields = ("titulo", "tipo_documento", "formulacion", "materia_prima", "descripcion", "archivo")
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "formulacion": "Usa este campo para procedimientos o fichas técnicas relacionadas con una formulación.",
            "materia_prima": "Usa este campo para procedimientos o fichas técnicas relacionadas con una materia prima.",
            "archivo": "Sube un archivo PDF.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)
