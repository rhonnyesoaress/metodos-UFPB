class Atividade:
    def __init__(self, id, nome, descricao, dificuldade="Fácil"):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dificuldade = dificuldade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "dificuldade": self.dificuldade
        }

    @staticmethod
    def from_dict(data):
        return Atividade(
            id=data["id"],
            nome=data["nome"],
            descricao=data["descricao"],
            dificuldade=data.get("dificuldade", "Fácil")
        )
