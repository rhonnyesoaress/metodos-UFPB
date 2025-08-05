# Salva usuários em arquivo json
import json
import os
from Entidades.user import User

class UserFileStorage:
    def __init__(self, file_path="users.json"):
        self.file_path = file_path

    def load_users(self):
        """Carrega usuários do arquivo JSON, retornando uma lista de objetos User."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return [User.from_dict(user_data) for user_data in data]
                    else:
                        print("Aviso: O arquivo users.json está mal formatado. Criando nova lista.")
            except (json.JSONDecodeError, FileNotFoundError):
                print("Aviso: O arquivo users.json está corrompido ou vazio. Criando nova lista.")
        
        return []

    def save_users(self, users: list):
        """Salva a lista de objetos User no arquivo JSON."""
        with open(self.file_path, "w") as f:
            data = [user.to_dict() for user in users]
            json.dump(data, f, indent=4)