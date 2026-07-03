"""
Serviço de predição de nível de estresse acadêmico.

Este módulo é o ÚNICO ponto do projeto responsável por conversar com o
modelo de IA. Ele NÃO treina nenhum modelo — apenas consome uma predição
já existente.

Duas formas de uso estão previstas:

1) MODO SIMULADO (padrão, ativo agora):
   Uma heurística simples baseada nas respostas do questionário simula
   a saída de um modelo já treinado (ex.: treinado offline com o dataset
   "Student Stress Monitoring Datasets" do Kaggle). Isso permite
   apresentar e testar o fluxo completo do sistema sem depender de uma
   API externa.

2) MODO API EXTERNA (pronto para plugar):
   Basta implementar o método `_prever_via_api()` para fazer uma
   requisição HTTP (requests.post) a um serviço/endpoint que hospeda o
   modelo já treinado (ex.: FastAPI, Flask, SageMaker, etc.) e retornar
   a resposta no mesmo formato do modo simulado. Depois, trocar a flag
   USE_EXTERNAL_API para True nas settings ou aqui embaixo.

A view do Django NUNCA deve conhecer os detalhes de como a predição é
feita — ela apenas chama `prever_nivel_estresse(dados)`.
"""

from dataclasses import dataclass
from django.conf import settings


@dataclass
class ResultadoPredicao:
    nivel: str              # "BAIXO" | "MEDIO" | "ALTO"
    mensagem: str
    confianca: float        # 0.0 a 1.0


# Ative para tentar consumir uma API externa real no futuro.
USE_EXTERNAL_API = getattr(settings, "STRESS_PREDICTOR_USE_API", False)
EXTERNAL_API_URL = getattr(settings, "STRESS_PREDICTOR_API_URL", "")


MENSAGENS = {
    "BAIXO": (
        "Seus hábitos atuais indicam um nível de estresse baixo. "
        "Continue mantendo uma rotina equilibrada entre estudos, sono e "
        "descanso — isso é ótimo para sua saúde mental e desempenho "
        "acadêmico."
    ),
    "MEDIO": (
        "Seus dados indicam um nível de estresse moderado. Fique atento "
        "a sinais como cansaço frequente e dificuldade para dormir. "
        "Pequenos ajustes na rotina, como pausas regulares e mais horas "
        "de sono, podem ajudar bastante."
    ),
    "ALTO": (
        "Seus dados indicam um nível de estresse elevado. É importante "
        "cuidar da sua saúde: procure reduzir a sobrecarga de tarefas, "
        "priorize o sono e considere conversar com o serviço de apoio "
        "psicológico da sua instituição."
    ),
}


def prever_nivel_estresse(dados: dict) -> ResultadoPredicao:
    """
    Ponto único de entrada usado pela view.

    `dados` é um dicionário com as chaves (já validadas pelo ModelForm):
        horas_sono, carga_estudo, frequencia_dor_cabeca,
        nivel_atividade_fisica, qualidade_sono, nivel_ansiedade,
        pressao_prazos, frequencia_cansaco
    """
    if USE_EXTERNAL_API and EXTERNAL_API_URL:
        return _prever_via_api(dados)
    return _prever_simulado(dados)


def _prever_simulado(dados: dict) -> ResultadoPredicao:
    """
    Heurística simples que SIMULA a saída de um modelo já treinado.

    Combina os fatores de risco (ansiedade, pressão de prazos, dor de
    cabeça, cansaço, carga de estudo) e os fatores de proteção (sono,
    qualidade do sono, atividade física) em um score de 0 a 1.
    Substitua esta função por uma chamada real ao modelo quando ele
    estiver disponível — a assinatura da função deve permanecer igual.
    """
    horas_sono = float(dados.get("horas_sono", 0))
    carga_estudo = float(dados.get("carga_estudo", 0))
    dor_cabeca = float(dados.get("frequencia_dor_cabeca", 0))
    atividade_fisica = float(dados.get("nivel_atividade_fisica", 0))
    qualidade_sono = float(dados.get("qualidade_sono", 0))
    ansiedade = float(dados.get("nivel_ansiedade", 0))
    pressao_prazos = float(dados.get("pressao_prazos", 0))
    cansaco = float(dados.get("frequencia_cansaco", 0))

    # Fatores de risco (escala 0-5) normalizados para 0-1
    risco = (
        ansiedade
        + pressao_prazos
        + dor_cabeca
        + cansaco
        + min(carga_estudo, 12) / 12 * 5  # normaliza carga de estudo (h/dia)
    ) / (5 * 5)

    # Fatores de proteção (escala 0-5) normalizados para 0-1
    protecao = (
        qualidade_sono
        + atividade_fisica
        + min(horas_sono, 9) / 9 * 5  # normaliza horas de sono
    ) / (5 * 3)

    # Score final de estresse: quanto maior o risco e menor a proteção,
    # mais alto o estresse.
    score = max(0.0, min(1.0, 0.65 * risco + 0.35 * (1 - protecao)))

    if score < 0.35:
        nivel = "BAIXO"
    elif score < 0.65:
        nivel = "MEDIO"
    else:
        nivel = "ALTO"

    confianca = round(0.75 + 0.20 * abs(score - 0.5) * 2, 2)  # 0.75 - 0.95

    return ResultadoPredicao(
        nivel=nivel,
        mensagem=MENSAGENS[nivel],
        confianca=min(confianca, 0.95),
    )


def _prever_via_api(dados: dict) -> ResultadoPredicao:  # pragma: no cover
    """
    Exemplo de integração com uma API externa que hospeda o modelo já
    treinado. Implementação de referência — ative USE_EXTERNAL_API para
    utilizá-la.
    """
    import requests

    resposta = requests.post(EXTERNAL_API_URL, json=dados, timeout=5)
    resposta.raise_for_status()
    payload = resposta.json()

    nivel = payload["nivel"].upper()
    return ResultadoPredicao(
        nivel=nivel,
        mensagem=payload.get("mensagem") or MENSAGENS.get(nivel, ""),
        confianca=float(payload.get("confianca", 0.8)),
    )
