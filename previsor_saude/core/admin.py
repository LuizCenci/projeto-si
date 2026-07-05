from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AvaliacaoEstresse, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role",)
    fieldsets = UserAdmin.fieldsets + (("Acesso ao sistema", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Acesso ao sistema", {"fields": ("role",)}),)


@admin.register(AvaliacaoEstresse)
class AvaliacaoEstresseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "estudante",
        "nome_estudante",
        "nivel_estresse_previsto",
        "score_confianca",
        "criado_em",
    )
    list_filter = ("nivel_estresse_previsto", "criado_em")
    search_fields = ("nome_estudante", "estudante__username")
    readonly_fields = (
        "nivel_estresse_previsto",
        "mensagem_explicativa",
        "score_confianca",
        "criado_em",
    )
    ordering = ("-criado_em",)

    fieldsets = (
        ("Identificação", {"fields": ("nome_estudante", "criado_em")}),
        (
            "Respostas do questionário",
            {
                "fields": (
                    "horas_sono",
                    "carga_estudo",
                    "frequencia_dor_cabeca",
                    "nivel_atividade_fisica",
                    "qualidade_sono",
                    "nivel_ansiedade",
                    "pressao_prazos",
                    "frequencia_cansaco",
                )
            },
        ),
        (
            "Resultado da predição",
            {
                "fields": (
                    "nivel_estresse_previsto",
                    "mensagem_explicativa",
                    "score_confianca",
                )
            },
        ),
    )
