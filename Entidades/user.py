# user.py
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password  # Em um sistema real, você usaria hashing aqui

    def check_password(self, password: str) -> bool:
        return self.password == password
    
    def to_dict(self):
        """Converte o objeto User em um dicionário para serialização."""
        return {"username": self.username, "password": self.password}

    @staticmethod
    def from_dict(data):
        """Cria um objeto User a partir de um dicionário."""
        return User(data['username'], data['password'])