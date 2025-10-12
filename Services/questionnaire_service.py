from __future__ import annotations
from typing import Dict, Any

from Domain.questionnaire import Questionnaire
from Domain.factories import question_from_atividade
from Repositories.interfaces import IUserRepository, IAtividadeRepository

class QuestionnaireService:
    def __init__(self, atividades_repo: IAtividadeRepository, user_repo: IUserRepository) -> None:
        self.atividades_repo = atividades_repo
        self.user_repo = user_repo

    def carregar_questionario(self) -> Questionnaire:
        # Carrega atividades do repositório e converte para Questions
        atividades = list(self.atividades_repo.listar())
        questions = [question_from_atividade(a) for a in atividades]
        return Questionnaire(questions)

    def avaliar_para_usuario(self, username: str, respostas: Dict[str, str]) -> Dict[str, Any]:
        user = self.user_repo.obter_por_username(username)
        gabaritos = getattr(user, "gabaritos", None) or {}

        q = self.carregar_questionario()
        resultado = q.avaliar(respostas, gabaritos_pessoais=gabaritos)

        # Primeira vez: persistir gabaritos pessoais (para PersonalQuestion)
        if not gabaritos:
            novos = {
                quest.id: respostas.get(quest.id, "")
                for quest in q.questions
                if quest.__class__.__name__ == "PersonalQuestion"
            }
            if novos:
                self.user_repo.salvar_gabaritos(username, novos)

        return resultado
