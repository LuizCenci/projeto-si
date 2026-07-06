from django.contrib import admin
from .models import AvaliacaoEstresse, FormularioGerado, RespostaEstudante


@admin.register(AvaliacaoEstresse)
class AvaliacaoEstresseAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_estudante", "nivel_estresse_previsto", "score_confianca", "criado_em")
    list_filter = ("nivel_estresse_previsto", "criado_em")
    search_fields = ("nome_estudante",)
    readonly_fields = ("nivel_estresse_previsto", "mensagem_explicativa", "score_confianca", "criado_em")
    ordering = ("-criado_em",)
    fieldsets = (
        ("Identificação", {"fields": ("nome_estudante", "criado_em")}),
        ("Respostas do questionário", {"fields": (
            "horas_sono", "carga_estudo", "frequencia_dor_cabeca",
            "nivel_atividade_fisica", "qualidade_sono", "nivel_ansiedade",
            "pressao_prazos", "frequencia_cansaco",
        )}),
        ("Resultado da predição", {"fields": ("nivel_estresse_previsto", "mensagem_explicativa", "score_confianca")}),
    )


@admin.register(FormularioGerado)
class FormularioGeradoAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_por", "ativo", "validade", "criado_em")
    list_filter = ("ativo", "criado_em")
    search_fields = ("criado_por__username",)
    readonly_fields = ("id", "criado_em")


@admin.register(RespostaEstudante)
class RespostaEstudanteAdmin(admin.ModelAdmin):
    list_display = ("nome_aluno", "ra", "turma", "nivel_risco", "nivel_estresse_predito", "data_submissao")
    list_filter = ("nivel_risco", "turma", "data_submissao")
    search_fields = ("nome_aluno", "ra", "turma")
    readonly_fields = ("nivel_estresse_predito", "nivel_risco", "data_submissao")
