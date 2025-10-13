class Atividade:
    def __init__(self, id, nome, descricao, dificuldade="Fácil", tipo="text", opcoes=None, categoria="pessoal", resposta=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dificuldade = dificuldade
        # tipo: "text" ou "multiple"
        self.tipo = tipo
        # opcoes: lista de strings quando tipo == "multiple"
        self.opcoes = opcoes or []
        # categoria: "pessoal" ou "objetiva"
        self.categoria = categoria
        # resposta: resposta correta para perguntas objetivas (string, normalizada quando aplicavel)
        self.resposta = resposta

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "dificuldade": self.dificuldade,
            "tipo": getattr(self, "tipo", "text"),
            "opcoes": getattr(self, "opcoes", []),
            "categoria": getattr(self, "categoria", "pessoal"),
            "resposta": getattr(self, "resposta", None)
        }

    @staticmethod
    def from_dict(data):
        return Atividade(
            id=data["id"],
            nome=data["nome"],
            descricao=data["descricao"],
            dificuldade=data.get("dificuldade", "Fácil"),
            tipo=data.get("tipo", "text"),
            opcoes=data.get("opcoes", []),
            categoria=data.get("categoria", "pessoal"),
            resposta=data.get("resposta", None)
        )
    
    def accept(self, visitor):
        # Visitor protocol uses English method name 'visit_activity' in the
        # StatisticsVisitor implementation. Call the common name to keep
        # compatibility. If an older visitor uses Portuguese name, try that
        # as a fallback.
        if hasattr(visitor, "visit_activity"):
            visitor.visit_activity(self)
        elif hasattr(visitor, "visit_atividade"):
            visitor.visit_atividade(self)
        else:
            # No visitor method found: no-op to avoid raising at runtime.
            return