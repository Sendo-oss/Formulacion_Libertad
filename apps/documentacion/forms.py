from django import forms

from .models import DocumentoTecnico


class DocumentoTecnicoForm(forms.ModelForm):
    class Meta:
        model = DocumentoTecnico
        fields = ("titulo", "tipo_documento", "formulacion", "descripcion", "archivo")
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "formulacion": "Opcional. Asocia el documento a una formulacion si corresponde.",
            "archivo": "Sube un archivo PDF.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)
