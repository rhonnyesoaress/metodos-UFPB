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

    def criar(self, id, nome, descricao, dificuldade="Fácil", tipo="text", opcoes=None, categoria="pessoal", resposta=None):
        if self.buscar_por_id(id):
            raise ValueError("Já existe uma atividade com este ID.")
        # se for objetiva e do tipo text, armazenar resposta em minusculas
        if categoria == 'objetiva' and tipo == 'text' and isinstance(resposta, str):
            resposta = resposta.strip().lower()
        nova = Atividade(id, nome, descricao, dificuldade, tipo, opcoes or [], categoria, resposta)
        self.atividades.append(nova)
        AtividadeFileStorage.save(self.atividades)
        return nova

    def atualizar(self, id, nome=None, descricao=None, dificuldade=None, tipo=None, opcoes=None, categoria=None, resposta=None):
        atividade = self.buscar_por_id(id)
        if not atividade:
            raise ValueError("Atividade não encontrada.")
        if nome:
            atividade.nome = nome
        if descricao:
            atividade.descricao = descricao
        if dificuldade:
            atividade.dificuldade = dificuldade
        if tipo:
            atividade.tipo = tipo
        if opcoes is not None:
            atividade.opcoes = opcoes
        if categoria:
            atividade.categoria = categoria
        if resposta is not None:
            # normalizar se objetiva texto
            if atividade.categoria == 'objetiva' and atividade.tipo == 'text' and isinstance(resposta, str):
                atividade.resposta = resposta.strip().lower()
            else:
                atividade.resposta = resposta
        AtividadeFileStorage.save(self.atividades)
        return atividade

    def deletar(self, id):
        atividade = self.buscar_por_id(id)
        if not atividade:
            raise ValueError("Atividade não encontrada.")
        self.atividades.remove(atividade)
        AtividadeFileStorage.save(self.atividades)
        return True
