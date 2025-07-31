# user_manager.py
from Entidades.user import User

class UserManager:
    def __init__(self):
        self.users = []  # dict com username -> User


    def register_user(self, username, password):
        if any(user.username == username for user in self.users):
            raise ValueError("Usuário já existe.")
        self.users.append(User(username, password))


    def login(self, username, password):
        for user in self.users:
            if user.username == username:
                if user.check_password(password):
                    return True
                else:
                    raise ValueError("Senha incorreta.")
        raise ValueError("Usuário não encontrado.")



    def listar_usuarios(self):
        return [user.username for user in self.users]
