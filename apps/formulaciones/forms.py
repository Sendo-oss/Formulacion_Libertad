from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Formulacion, FormulacionDetalle


class FormulacionForm(forms.ModelForm):
    categoria = forms.ChoiceField(label="Categoria", required=False)
    nueva_categoria = forms.CharField(
        label="Nueva categoria",
        required=False,
        help_text="Si no aparece en la lista, escribela aqui para agregarla.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias_existentes = list(
            Formulacion.objects.exclude(categoria__exact="")
            .order_by("categoria")
            .values_list("categoria", flat=True)
            .distinct()
        )
        categorias = list(Formulacion.CATEGORIAS_BASE)
        for categoria in categorias_existentes:
            if categoria not in categorias:
                categorias.append(categoria)
        if self.instance and self.instance.pk and self.instance.categoria and self.instance.categoria not in categorias:
            categorias.append(self.instance.categoria)
        self.fields["categoria"].choices = [("", "Selecciona una categoria")] + [
            (categoria, categoria) for categoria in categorias
        ]
        if self.instance and self.instance.pk:
            self.fields["categoria"].initial = self.instance.categoria
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css_class)
        self.fields["fuente_referencia"].widget.attrs.setdefault(
            "placeholder",
            "Ejemplo: https://... o autor, A. A. (2023). Titulo del libro. Editorial.",
        )

    def clean(self):
        cleaned_data = super().clean()
        categoria = (cleaned_data.get("categoria") or "").strip()
        nueva_categoria = (cleaned_data.get("nueva_categoria") or "").strip()
        categorias_existentes = {
            item.lower(): item
            for item in Formulacion.objects.exclude(categoria__exact="")
            .values_list("categoria", flat=True)
            .distinct()
        }

        if nueva_categoria:
            cleaned_data["categoria"] = categorias_existentes.get(nueva_categoria.lower(), nueva_categoria)
        elif categoria:
            cleaned_data["categoria"] = categoria
        else:
            self.add_error("categoria", "Debes seleccionar una categoria o registrar una nueva.")

        return cleaned_data

    class Meta:
        model = Formulacion
        exclude = ("creado_por", "materias_primas")
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "codigo": "Usa el codigo institucional o uno interno unico.",
            "fuente_referencia": "Ingresa la fuente de donde se obtuvo la formulacion. Puede ser enlace web, libro, articulo o documento tecnico. En tu documento Word cita esta fuente en formato APA 7.",
        }


class BaseFormulacionDetalleFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        detalles_validos = 0
        materias = set()
        total_porcentaje = Decimal("0.00")
        hay_porcentajes = False
        hay_otras_unidades = False

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
                if unidad == FormulacionDetalle.UnidadMedida.PORCENTAJE:
                    hay_porcentajes = True
                    if cantidad > Decimal("100.00"):
                        raise ValidationError(
                            f"El componente '{materia.nombre}' no puede superar 100%."
                        )
                    total_porcentaje += cantidad
                else:
                    hay_otras_unidades = True
                materias.add(materia.pk)
                detalles_validos += 1

        if detalles_validos == 0:
            raise ValidationError("Debes registrar al menos un componente en la formulacion.")
        if hay_porcentajes and hay_otras_unidades:
            raise ValidationError(
                "Si una formulacion usa porcentaje (%), todos sus componentes deben registrarse en porcentaje."
            )
        if hay_porcentajes and total_porcentaje != Decimal("100.00"):
            raise ValidationError(
                f"La formulacion en porcentaje debe sumar exactamente 100%. Total actual: {total_porcentaje}."
            )


FormulacionDetalleFormSet = inlineformset_factory(
    Formulacion,
    FormulacionDetalle,
    fields=("materia_prima", "cantidad", "unidad_medida", "orden"),
    extra=1,
    can_delete=True,
    formset=BaseFormulacionDetalleFormSet,
    widgets={
        "materia_prima": forms.Select(attrs={"class": "form-select"}),
        "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
        "unidad_medida": forms.Select(
            attrs={"class": "form-select"},
            choices=FormulacionDetalle.UnidadMedida.choices,
        ),
        "orden": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    },
)
