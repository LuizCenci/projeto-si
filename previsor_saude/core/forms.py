from django import forms
from .models import AvaliacaoEstresse


ESCALA_0_5 = [(i, str(i)) for i in range(0, 6)]


class AvaliacaoEstresseForm(forms.ModelForm):
    """Formulário/questionário respondido pelo estudante."""

    frequencia_dor_cabeca = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("frequencia_dor_cabeca").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )
    nivel_atividade_fisica = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("nivel_atividade_fisica").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )
    qualidade_sono = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("qualidade_sono").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )
    nivel_ansiedade = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("nivel_ansiedade").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )
    pressao_prazos = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("pressao_prazos").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )
    frequencia_cansaco = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("frequencia_cansaco").verbose_name,
        choices=ESCALA_0_5,
        coerce=int,
        widget=forms.Select,
    )

    class Meta:
        model = AvaliacaoEstresse
        fields = [
            "horas_sono",
            "carga_estudo",
            "frequencia_dor_cabeca",
            "nivel_atividade_fisica",
            "qualidade_sono",
            "nivel_ansiedade",
            "pressao_prazos",
            "frequencia_cansaco",
        ]
        widgets = {
            "nome_estudante": forms.TextInput(
                attrs={"placeholder": "Como podemos te chamar? (opcional)"}
            ),
            "horas_sono": forms.NumberInput(
                attrs={"step": "0.5", "min": "0", "max": "14"}
            ),
            "carga_estudo": forms.NumberInput(
                attrs={"min": "0", "max": "16"}
            ),
        }

    def clean_horas_sono(self):
        valor = self.cleaned_data["horas_sono"]
        if valor < 0 or valor > 14:
            raise forms.ValidationError("Informe um valor entre 0 e 14 horas.")
        return valor

    def clean_carga_estudo(self):
        valor = self.cleaned_data["carga_estudo"]
        if valor < 0 or valor > 16:
            raise forms.ValidationError("Informe um valor entre 0 e 16 horas.")
        return valor
