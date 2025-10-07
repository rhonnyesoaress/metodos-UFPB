# user.py
class User:
    def __init__(self, username: str, password: str, gabarito: dict = None):
        self.username = username
        self.password = password  # Em um sistema real, você usaria hashing aqui
        # gabarito guarda as respostas "corretas" (guardadas na primeira vez que o usuário respondeu)
        # estrutura: {"q1": "resposta normalizada", "q2": "b", ...}
        self.gabarito = gabarito or {}

    def check_password(self, password: str) -> bool:
        return self.password == password

    def to_dict(self):
        """Converte o objeto User em um dicionário para serialização."""
        return {"username": self.username, "password": self.password, "gabarito": self.gabarito}

    @staticmethod
    def from_dict(data):
        """Cria um objeto User a partir de um dicionário."""
        # compatibilidade com formatos antigos que têm só username/password
        username = data.get('username')
        password = data.get('password')
        gabarito = data.get('gabarito', {})
        return User(username, password, gabarito)