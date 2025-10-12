from __future__ import annotations
from typing import List, Dict, Any
from .question import Question, PersonalQuestion

class Questionnaire:
    def __init__(self, questions: List[Question]) -> None:
        self.questions = questions

    def avaliar(self, respostas: Dict[str, str], gabaritos_pessoais: Dict[str, str] | None = None) -> Dict[str, Any]:
        acertos = 0
        total = len(self.questions)
        detalhado = []

        for q in self.questions:
            val = respostas.get(q.id, "")
            if isinstance(q, PersonalQuestion):
                ok = q.avaliar(val, (gabaritos_pessoais or {}).get(q.id))
            else:
                ok = q.avaliar(val)

            detalhado.append({"id": q.id, "correta": ok})
            if ok:
                acertos += 1

        return {"acertos": acertos, "total": total, "detalhe": detalhado}
