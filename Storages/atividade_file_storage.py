import json
import os
from Entidades.atividade import Atividade

class AtividadeFileStorage:
    FILE_PATH = "atividades.json"

    @staticmethod
    def load():
        if not os.path.exists(AtividadeFileStorage.FILE_PATH):
            return []
        with open(AtividadeFileStorage.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Atividade.from_dict(item) for item in data]

    @staticmethod
    def save(atividades):
        with open(AtividadeFileStorage.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in atividades], f, indent=4, ensure_ascii=False)
