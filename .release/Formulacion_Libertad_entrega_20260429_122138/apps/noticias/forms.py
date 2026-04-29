from django import forms

from .models import Noticia


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ("titulo", "resumen", "contenido", "fuente_url", "publicada_en", "activa")
        widgets = {
            "resumen": forms.Textarea(attrs={"rows": 3}),
            "contenido": forms.Textarea(attrs={"rows": 8}),
            "publicada_en": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "fuente_url": "Opcional. Puedes enlazar una fuente confiable sobre formulación magistral.",
            "publicada_en": "Fecha y hora en la que la noticia quedará visible en el sistema.",
            "activa": "Si está marcada, la noticia será visible para los usuarios. Si la desmarcas, quedará oculta.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)
