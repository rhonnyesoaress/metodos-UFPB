from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

class Question(ABC):
    def __init__(self, qid: str, enunciado: str, dificuldade: str = "Fácil") -> None:
        self.id = qid
        self.enunciado = enunciado
        self.dificuldade = dificuldade

    @abstractmethod
    def avaliar(self, resposta_usuario: Optional[str]) -> bool:
        ...

class ObjectiveQuestion(Question):
    def __init__(
        self,
        qid: str,
        enunciado: str,
        resposta_correta: str,
        opcoes: Optional[List[str]] = None,
        dificuldade: str = "Fácil",
    ) -> None:
        super().__init__(qid, enunciado, dificuldade=dificuldade)
        self.resposta_correta = (resposta_correta or "").strip().lower()
        self.opcoes = opcoes or []

    def avaliar(self, resposta_usuario: Optional[str]) -> bool:
        norm = (resposta_usuario or "").strip().lower()
        return norm == self.resposta_correta

class PersonalQuestion(Question):
    """Pergunta pessoal cujo gabarito é individualizado por usuário."""
    def __init__(
        self,
        qid: str,
        enunciado: str,
        dificuldade: str = "Fácil",
    ) -> None:
        super().__init__(qid, enunciado, dificuldade=dificuldade)

    def avaliar(self, resposta_usuario: Optional[str], gabarito_usuario: Optional[str] = None) -> bool:
        if gabarito_usuario is None:
            # Na primeira resposta pessoal, tratamos como válida; a persistência do gabarito
            # deve ser feita por um serviço externo (QuestionnaireService).
            return True
        return (resposta_usuario or "").strip().lower() == (gabarito_usuario or "").strip().lower()
