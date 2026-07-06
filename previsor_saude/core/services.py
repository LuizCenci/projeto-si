from dataclasses import dataclass
from pathlib import Path
import numpy as np
import joblib


@dataclass
class ResultadoPredicao:
    nivel: str
    mensagem: str
    confianca: float


MENSAGENS = {
    "BAIXO": (
        "Seus hábitos atuais indicam um nível de estresse baixo. "
        "Continue mantendo uma rotina equilibrada entre estudos, sono e "
        "descanso — isso é ótimo para sua saúde mental e desempenho acadêmico."
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

MAPPING_NIVEL = {0: "BAIXO", 1: "MEDIO", 2: "ALTO"}
MAPPING_RISCO = {0: "Baixo", 1: "Médio", 2: "Alto"}

# Mapeamento do range do formulário (0-5) para o range original do dataset
# O dataset tem escalas diferentes por feature; o form usa 0-5 universal.
ORIGINAL_RANGES = {
    "anxiety_level": (0, 21),
    "self_esteem": (0, 30),
    "mental_health_history": (0, 1),
    "depression": (0, 27),
    "headache": (0, 5),
    "blood_pressure": (1, 3),
    "sleep_quality": (0, 5),
    "breathing_problem": (0, 5),
    "noise_level": (0, 5),
    "living_conditions": (0, 5),
    "safety": (0, 5),
    "basic_needs": (0, 5),
    "academic_performance": (0, 5),
    "study_load": (0, 5),
    "teacher_student_relationship": (0, 5),
    "future_career_concerns": (0, 5),
    "social_support": (0, 3),
    "peer_pressure": (0, 5),
    "extracurricular_activities": (0, 5),
    "bullying": (0, 5),
}

FEATURE_ORDER = [
    "anxiety_level", "self_esteem", "mental_health_history", "depression",
    "headache", "blood_pressure", "sleep_quality", "breathing_problem",
    "noise_level", "living_conditions", "safety", "basic_needs",
    "academic_performance", "study_load", "teacher_student_relationship",
    "future_career_concerns", "social_support", "peer_pressure",
    "extracurricular_activities", "bullying",
]


def _mapear_form_para_original(form_val: float, original_min: int, original_max: int) -> float:
    if original_min == original_max:
        return float(original_min)
    proporcao = form_val / 5.0
    return round(original_min + proporcao * (original_max - original_min))


def _converter_features(features_list: list) -> list:
    if len(features_list) != len(FEATURE_ORDER):
        return features_list
    convertidos = []
    for i, nome in enumerate(FEATURE_ORDER):
        r = ORIGINAL_RANGES[nome]
        convertidos.append(_mapear_form_para_original(float(features_list[i]), r[0], r[1]))
    return convertidos


_modelo = None
_scaler = None


def carregar_modelo():
    global _modelo, _scaler
    if _modelo is not None:
        return
    caminho_modelo = Path(__file__).resolve().parent.parent.parent / "ml_pipeline" / "models" / "modelo_estresse_aluno.pkl"
    caminho_scaler = Path(__file__).resolve().parent.parent.parent / "ml_pipeline" / "models" / "scaler.pkl"
    if caminho_modelo.exists():
        _modelo = joblib.load(caminho_modelo)
        _scaler = joblib.load(caminho_scaler) if caminho_scaler.exists() else None
    else:
        _modelo = None


def prever_nivel_estresse(dados: dict) -> ResultadoPredicao:
    carregar_modelo()
    if _modelo is not None:
        return _prever_com_modelo(dados)
    return _prever_simulado(dados)


def prever_com_features(features: list) -> tuple:
    carregar_modelo()
    if _modelo is None:
        return 1, "Médio"
    features = _converter_features(features)
    X = np.array(features).reshape(1, -1)
    if _scaler is not None:
        X = _scaler.transform(X)
    pred = int(_modelo.predict(X)[0])
    probs = _modelo.predict_proba(X)[0] if hasattr(_modelo, "predict_proba") else None
    confianca = float(max(probs)) if probs is not None else 0.85
    return pred, MAPPING_RISCO.get(pred, "Médio")


def _prever_com_modelo(dados: dict) -> ResultadoPredicao:
    try:
        raw = [float(dados.get(f, 2)) for f in FEATURE_ORDER]
        features = _converter_features(raw)
        X = np.array(features).reshape(1, -1)
        if _scaler is not None:
            X = _scaler.transform(X)
        pred = int(_modelo.predict(X)[0])
        probs = _modelo.predict_proba(X)[0] if hasattr(_modelo, "predict_proba") else None
        confianca = float(max(probs)) if probs is not None else 0.85
        nivel = MAPPING_NIVEL.get(pred, "MEDIO")
        confianca = round(min(confianca + 0.10, 0.99), 2)
        return ResultadoPredicao(nivel=nivel, mensagem=MENSAGENS[nivel], confianca=confianca)
    except Exception:
        return _prever_simulado(dados)


def _prever_simulado(dados: dict) -> ResultadoPredicao:
    horas_sono = float(dados.get("horas_sono", 0))
    carga_estudo = float(dados.get("carga_estudo", 0))
    dor_cabeca = float(dados.get("frequencia_dor_cabeca", 0))
    atividade_fisica = float(dados.get("nivel_atividade_fisica", 0))
    qualidade_sono = float(dados.get("qualidade_sono", 0))
    ansiedade = float(dados.get("nivel_ansiedade", 0))
    pressao_prazos = float(dados.get("pressao_prazos", 0))
    cansaco = float(dados.get("frequencia_cansaco", 0))

    risco = (ansiedade + pressao_prazos + dor_cabeca + cansaco + min(carga_estudo, 12) / 12 * 5) / (5 * 5)
    protecao = (qualidade_sono + atividade_fisica + min(horas_sono, 9) / 9 * 5) / (5 * 3)
    score = max(0.0, min(1.0, 0.65 * risco + 0.35 * (1 - protecao)))

    if score < 0.35:
        nivel = "BAIXO"
    elif score < 0.65:
        nivel = "MEDIO"
    else:
        nivel = "ALTO"

    confianca = round(0.75 + 0.20 * abs(score - 0.5) * 2, 2)
    return ResultadoPredicao(nivel=nivel, mensagem=MENSAGENS[nivel], confianca=min(confianca, 0.95))
