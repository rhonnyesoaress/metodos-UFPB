from Entidades.atividade import Atividade
from Storages.atividade_file_storage import AtividadeFileStorage

class AtividadeManager:
    def __init__(self):
        self.atividades = AtividadeFileStorage.load()

    def listar(self):
        return self.atividades

    def buscar_por_id(self, id):
        for atividade in self.atividades:
            if atividade.id == id:
                return atividade
        return None

    def criar(self, id, nome, descricao, dificuldade="Fácil"):
        if self.buscar_por_id(id):
            raise ValueError("Já existe uma atividade com este ID.")
        nova = Atividade(id, nome, descricao, dificuldade)
        self.atividades.append(nova)
        AtividadeFileStorage.save(self.atividades)
        return nova

    def atualizar(self, id, nome=None, descricao=None, dificuldade=None):
        atividade = self.buscar_por_id(id)
        if not atividade:
            raise ValueError("Atividade não encontrada.")
        if nome:
            atividade.nome = nome
        if descricao:
            atividade.descricao = descricao
        if dificuldade:
            atividade.dificuldade = dificuldade
        AtividadeFileStorage.save(self.atividades)
        return atividade

    def deletar(self, id):
        atividade = self.buscar_por_id(id)
        if not atividade:
            raise ValueError("Atividade não encontrada.")
        self.atividades.remove(atividade)
        AtividadeFileStorage.save(self.atividades)
        return True
