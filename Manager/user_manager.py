# user_manager.py
from Entidades.user import User

class UserManager:
    def __init__(self):
        self.users = {}  # dict com username -> User

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False  # Já existe
        self.users[username] = User(username, password)
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False
        return user.check_password(password)
    
    def listar_usuarios(self):
        return list(self.users.keys())