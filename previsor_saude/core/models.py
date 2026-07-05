from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db import models


class RoleUsuario(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    ESTUDANTE = "ESTUDANTE", "Estudante"
    UNIVERSIDADE = "UNIVERSIDADE", "Universidade"


class UsuarioManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not extra_fields.get("role"):
            raise ValueError("A role é obrigatória ao criar um usuário.")
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["role"] = RoleUsuario.ADMIN
        return super().create_superuser(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    role = models.CharField("Role", max_length=15, choices=RoleUsuario.choices)
    objects = UsuarioManager()

    def __str__(self):
        return self.get_full_name() or self.username


class NivelEstresse(models.TextChoices):
    """Categorias de saída do modelo preditivo."""
    BAIXO = "BAIXO", "Baixo"
    MEDIO = "MEDIO", "Médio"
    ALTO = "ALTO", "Alto"


class AvaliacaoEstresse(models.Model):
    """
    Armazena as respostas do questionário preenchido pelo estudante
    e o resultado retornado pelo serviço de predição (IA já treinada).
    """

    # --- Dados de identificação (opcional) ---
    estudante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="avaliacoes", null=True, blank=True,
    )
    nome_estudante = models.CharField(
        "Nome (opcional)", max_length=150, blank=True
    )

    # --- Variáveis usadas pelo modelo preditivo ---
    horas_sono = models.FloatField(
        "Horas de sono por noite",
        help_text="Média de horas dormidas por noite.",
    )
    carga_estudo = models.PositiveSmallIntegerField(
        "Carga diária de estudos (horas)",
        help_text="Quantidade de horas dedicadas aos estudos por dia.",
    )
    frequencia_dor_cabeca = models.PositiveSmallIntegerField(
        "Frequência de dores de cabeça (0 a 5)",
        help_text="0 = nunca, 5 = quase todos os dias.",
    )
    nivel_atividade_fisica = models.PositiveSmallIntegerField(
        "Nível de atividade física (0 a 5)",
        help_text="0 = sedentário, 5 = muito ativo.",
    )
    qualidade_sono = models.PositiveSmallIntegerField(
        "Qualidade percebida do sono (0 a 5)",
        help_text="0 = péssima, 5 = excelente.",
    )
    nivel_ansiedade = models.PositiveSmallIntegerField(
        "Nível de ansiedade percebido (0 a 5)",
        help_text="0 = nenhuma, 5 = extrema.",
    )
    pressao_prazos = models.PositiveSmallIntegerField(
        "Pressão por prazos acadêmicos (0 a 5)",
        help_text="0 = nenhuma, 5 = extrema.",
    )
    frequencia_cansaco = models.PositiveSmallIntegerField(
        "Frequência de cansaço (0 a 5)",
        help_text="0 = nunca, 5 = sempre.",
    )

    # --- Resultado da predição ---
    nivel_estresse_previsto = models.CharField(
        "Nível de estresse previsto",
        max_length=10,
        choices=NivelEstresse.choices,
        blank=True,
    )
    mensagem_explicativa = models.TextField(
        "Mensagem explicativa", blank=True
    )
    score_confianca = models.FloatField(
        "Confiança da predição (0 a 1)", null=True, blank=True
    )

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação de Estresse"
        verbose_name_plural = "Avaliações de Estresse"
        ordering = ["-criado_em"]

    def __str__(self):
        quem = self.nome_estudante or "Anônimo"
        return f"{quem} - {self.get_nivel_estresse_previsto_display() or 'pendente'} ({self.criado_em:%d/%m/%Y %H:%M})"
