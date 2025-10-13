class StatisticsVisitor:
    def __init__(self):
        self.activity_count = 0
        self.difficulty_count = {}

    def visit_activity(self, atividade):
        self.activity_count += 1
        dificuldade = getattr(atividade, "dificuldade", "Desconhecida")
        self.difficulty_count[dificuldade] = self.difficulty_count.get(dificuldade, 0) + 1
