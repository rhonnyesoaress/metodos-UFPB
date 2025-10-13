from abc import ABC, abstractmethod
from Business.Visitors.statistics_visitor import StatisticsVisitor
from .implementors import IOutputImplementor
import os

class Report(ABC):
    def __init__(self, implementor):
        self.implementor = implementor

    @abstractmethod
    def _generate_content(self):
        pass

    def export(self):
        content = self._generate_content()
        self.implementor.save(content)


class ActivityReport(Report):
    def __init__(self, implementor, atividades):
        super().__init__(implementor)
        self.atividades = atividades

    def _generate_content(self):
        visitor = StatisticsVisitor()

        for atividade in self.atividades.listar():
            visitor.visit_activity(atividade)

        conteudo = (
            f"Total de Atividades: {visitor.activity_count}\n"
            f"Contagem por Dificuldade:\n"
        )

        for dificuldade, qtd in visitor.difficulty_count.items():
            conteudo += f"  - {dificuldade}: {qtd}\n"

        return conteudo

class LogReport(Report):
    """
    Uma nova Abstração Refinada que gera um relatório lendo diretamente
    o arquivo de log do sistema.
    """
    def __init__(self, implementor: IOutputImplementor, log_file_path: str):
        super().__init__(implementor)
        self._log_file_path = log_file_path

    def _generate_content(self) -> str:
        """
        A lógica deste relatório é simples: ler e retornar o conteúdo
        do arquivo de log.
        """
        print(f"Gerando relatório a partir de '{self._log_file_path}'...")
        
        # Verifica se o arquivo de log existe
        if not os.path.exists(self._log_file_path):
            return "Nenhuma atividade registrada ainda. O arquivo de log não foi encontrado."

        try:
            with open(self._log_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return "O log de atividades está vazio."
                # Adiciona um cabeçalho ao conteúdo do log
                return "--- LOG DE MOVIMENTAÇÕES DO SISTEMA ---\n\n" + content
        except Exception as e:
            return f"Ocorreu um erro ao ler o arquivo de log: {e}"