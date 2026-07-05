import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def duas_semanas():
    return timezone.now() + timedelta(weeks=2)


class NivelEstresse(models.TextChoices):
    BAIXO = "BAIXO", "Baixo"
    MEDIO = "MEDIO", "Médio"
    ALTO = "ALTO", "Alto"


class NivelRisco(models.TextChoices):
    BAIXO = "Baixo", "Baixo"
    MEDIO = "Médio", "Médio"
    ALTO = "Alto", "Alto"


class AvaliacaoEstresse(models.Model):
    nome_estudante = models.CharField("Nome (opcional)", max_length=150, blank=True)
    horas_sono = models.FloatField("Horas de sono por noite")
    carga_estudo = models.PositiveSmallIntegerField("Carga diária de estudos (horas)")
    frequencia_dor_cabeca = models.PositiveSmallIntegerField("Frequência de dores de cabeça (0 a 5)")
    nivel_atividade_fisica = models.PositiveSmallIntegerField("Nível de atividade física (0 a 5)")
    qualidade_sono = models.PositiveSmallIntegerField("Qualidade percebida do sono (0 a 5)")
    nivel_ansiedade = models.PositiveSmallIntegerField("Nível de ansiedade percebido (0 a 5)")
    pressao_prazos = models.PositiveSmallIntegerField("Pressão por prazos acadêmicos (0 a 5)")
    frequencia_cansaco = models.PositiveSmallIntegerField("Frequência de cansaço (0 a 5)")
    nivel_estresse_previsto = models.CharField(max_length=10, choices=NivelEstresse.choices, blank=True)
    mensagem_explicativa = models.TextField(blank=True)
    score_confianca = models.FloatField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação de Estresse"
        verbose_name_plural = "Avaliações de Estresse"
        ordering = ["-criado_em"]

    def __str__(self):
        quem = self.nome_estudante or "Anônimo"
        return f"{quem} - {self.get_nivel_estresse_previsto_display() or 'pendente'} ({self.criado_em:%d/%m/%Y %H:%M})"


class FormularioGerado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios_gerados')
    ativo = models.BooleanField(default=True)
    validade = models.DateTimeField("Válido até", default=duas_semanas)

    class Meta:
        verbose_name = "Formulário Gerado"
        verbose_name_plural = "Formulários Gerados"
        ordering = ["-criado_em"]

    def esta_valido(self):
        return self.ativo and timezone.now() <= self.validade

    def __str__(self):
        return f"Formulário {self.id} - {self.criado_por.username} ({self.criado_em:%d/%m/%Y})"


class RespostaEstudante(models.Model):
    formulario = models.ForeignKey(FormularioGerado, on_delete=models.CASCADE, related_name='respostas')
    nome_aluno = models.CharField("Nome completo", max_length=255)
    ra = models.CharField("RA (Registro Acadêmico)", max_length=20, default="")
    turma = models.CharField("Turma/Ano escolar", max_length=100)

    anxiety_level = models.PositiveSmallIntegerField("Nível de ansiedade")
    self_esteem = models.PositiveSmallIntegerField("Autoestima")
    mental_health_history = models.PositiveSmallIntegerField("Histórico de saúde mental")
    depression = models.PositiveSmallIntegerField("Depressão")
    headache = models.PositiveSmallIntegerField("Dor de cabeça")
    blood_pressure = models.PositiveSmallIntegerField("Pressão arterial")
    sleep_quality = models.PositiveSmallIntegerField("Qualidade do sono")
    breathing_problem = models.PositiveSmallIntegerField("Problemas respiratórios")
    noise_level = models.PositiveSmallIntegerField("Nível de ruído")
    living_conditions = models.PositiveSmallIntegerField("Condições de moradia")
    safety = models.PositiveSmallIntegerField("Segurança")
    basic_needs = models.PositiveSmallIntegerField("Necessidades básicas")
    academic_performance = models.PositiveSmallIntegerField("Desempenho acadêmico")
    study_load = models.PositiveSmallIntegerField("Carga de estudos")
    teacher_student_relationship = models.PositiveSmallIntegerField("Relação professor-aluno")
    future_career_concerns = models.PositiveSmallIntegerField("Preocupações com carreira")
    social_support = models.PositiveSmallIntegerField("Suporte social")
    peer_pressure = models.PositiveSmallIntegerField("Pressão dos colegas")
    extracurricular_activities = models.PositiveSmallIntegerField("Atividades extracurriculares")
    bullying = models.PositiveSmallIntegerField("Bullying")

    nivel_estresse_predito = models.IntegerField("Nível de estresse predito (0-2)", null=True, blank=True)
    nivel_risco = models.CharField("Nível de risco", max_length=50, choices=NivelRisco.choices, blank=True)
    data_submissao = models.DateTimeField("Data de submissão", auto_now_add=True)

    class Meta:
        verbose_name = "Resposta de Estudante"
        verbose_name_plural = "Respostas de Estudantes"
        ordering = ["-data_submissao"]

    def __str__(self):
        return f"{self.nome_aluno} - {self.turma} ({self.get_nivel_risco_display() or 'pendente'})"
