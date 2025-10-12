from __future__ import annotations
from typing import Any

try:
    from Entidades.atividade import Atividade  # estilo PascalCase
except Exception:
    try:
        from Entidades.atividade import Atividade  # estilo snake_case
    except Exception:
        Atividade = Any  # fallback para não quebrar import durante lint/tests

from .question import ObjectiveQuestion, PersonalQuestion

def question_from_atividade(a: Atividade):
    categoria = getattr(a, "categoria", None) or getattr(a, "tipo", "objetiva")
    descricao = getattr(a, "descricao", None) or getattr(a, "texto", "Pergunta sem enunciado")
    resposta = getattr(a, "resposta", None) or getattr(a, "gabarito", "")
    opcoes = getattr(a, "opcoes", None) or getattr(a, "alternativas", None)
    dificuldade = getattr(a, "dificuldade", "Fácil")
    qid = getattr(a, "id", None) or getattr(a, "codigo", None) or str(id(a))

    if str(categoria).lower() in {"objetiva", "multipla_escolha", "alternativa"}:
        return ObjectiveQuestion(
            qid=qid,
            enunciado=descricao,
            resposta_correta=str(resposta or ""),
            opcoes=list(opcoes) if opcoes else None,
            dificuldade=str(dificuldade),
        )
    else:
        return PersonalQuestion(
            qid=qid,
            enunciado=descricao,
            dificuldade=str(dificuldade),
        )
