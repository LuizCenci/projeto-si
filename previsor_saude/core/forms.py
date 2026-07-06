from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AvaliacaoEstresse, RespostaEstudante


ESCALA_0_5 = [(i, str(i)) for i in range(0, 6)]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário", widget=forms.TextInput(attrs={"placeholder": "Nome de usuário"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"placeholder": "Sua senha"}))


class AvaliacaoEstresseForm(forms.ModelForm):
    frequencia_dor_cabeca = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("frequencia_dor_cabeca").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )
    nivel_atividade_fisica = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("nivel_atividade_fisica").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )
    qualidade_sono = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("qualidade_sono").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )
    nivel_ansiedade = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("nivel_ansiedade").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )
    pressao_prazos = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("pressao_prazos").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )
    frequencia_cansaco = forms.TypedChoiceField(
        label=AvaliacaoEstresse._meta.get_field("frequencia_cansaco").verbose_name,
        choices=ESCALA_0_5, coerce=int, widget=forms.Select,
    )

    class Meta:
        model = AvaliacaoEstresse
        fields = [
            "nome_estudante", "horas_sono", "carga_estudo",
            "frequencia_dor_cabeca", "nivel_atividade_fisica",
            "qualidade_sono", "nivel_ansiedade", "pressao_prazos",
            "frequencia_cansaco",
        ]
        widgets = {
            "nome_estudante": forms.TextInput(attrs={"placeholder": "Como podemos te chamar? (opcional)"}),
            "horas_sono": forms.NumberInput(attrs={"step": "0.5", "min": "0", "max": "14"}),
            "carga_estudo": forms.NumberInput(attrs={"min": "0", "max": "16"}),
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


FEATURE_FIELDS = [
    "anxiety_level", "self_esteem", "mental_health_history",
    "depression", "headache", "blood_pressure",
    "sleep_quality", "breathing_problem", "noise_level",
    "living_conditions", "safety", "basic_needs",
    "academic_performance", "study_load", "teacher_student_relationship",
    "future_career_concerns", "social_support", "peer_pressure",
    "extracurricular_activities", "bullying",
]

HELP_TEXTS = {
    "anxiety_level": "Nivel de preocupacao, nervosismo ou tensao no dia a dia.",
    "self_esteem": "O quanto voce se valoriza e confia em si mesmo.",
    "mental_health_history": "Ja teve ou tem acompanhamento psicologico/psiquiatrico.",
    "depression": "Frequencia de sentimentos de tristeza, desânimo ou falta de interesse.",
    "headache": "Frequencia de dores de cabeca no seu cotidiano.",
    "blood_pressure": "Se souber, informe. Caso nao saiba, deixe em branco.",
    "sleep_quality": "Como voce avalia a qualidade do seu sono de forma geral.",
    "breathing_problem": "Sente falta de ar, desconforto ao respirar ou problemas respiratorios.",
    "noise_level": "Nivel de ruido no ambiente onde voce estuda ou mora.",
    "living_conditions": "Condicoes gerais da sua moradia (espaco, conforto, infraestrutura).",
    "safety": "Sensacao de seguranca no seu bairro ou regiao onde mora.",
    "basic_needs": "Acesso a alimentacao, agua, energia e itens basicos.",
    "academic_performance": "Como voce avalia seu desempenho nas disciplinas.",
    "study_load": "Carga de estudos e tarefas academicas que voce precisa cumprir.",
    "teacher_student_relationship": "Qualidade da relacao e comunicacao com seus professores.",
    "future_career_concerns": "Nivel de preocupacao com seu futuro profissional e carreira.",
    "social_support": "Apoio que voce recebe de familia, amigos ou colegas.",
    "peer_pressure": "Pressao que voce sente por parte dos colegas ou grupo social.",
    "extracurricular_activities": "Participacao em atividades alem dos estudos (esportes, arte, etc).",
    "bullying": "Frequencia com que voce sofre ou sofreu situacoes de bullying.",
}


class RespostaEstudanteForm(forms.ModelForm):
    class Meta:
        model = RespostaEstudante
        fields = [
            "nome_aluno", "ra", "turma",
        ] + FEATURE_FIELDS
        widgets = {
            "nome_aluno": forms.TextInput(attrs={"placeholder": "Nome completo"}),
            "ra": forms.TextInput(attrs={"placeholder": "Ex: 2554704"}),
            "turma": forms.TextInput(attrs={"placeholder": "Ex: 3 Ano ADS"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in FEATURE_FIELDS:
            self.fields[f].widget = forms.NumberInput(attrs={
                "min": "0", "max": "5", "class": "scale-input",
                "placeholder": "0 a 5",
            })
            self.fields[f].min_value = 0
            self.fields[f].max_value = 5
            self.fields[f].required = False
            self.fields[f].help_text = HELP_TEXTS.get(f, "")

    def clean(self):
        cleaned = super().clean()
        for f in FEATURE_FIELDS:
            v = cleaned.get(f)
            if v is not None and (v < 0 or v > 5):
                self.add_error(f, "Valor deve estar entre 0 e 5.")
        return cleaned
