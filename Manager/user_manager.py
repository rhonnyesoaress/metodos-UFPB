# user_manager.py
from Entidades.user import User
from Validators.login_validator import LoginValidator
from Validators.password_validator import PasswordValidator
from Storages.user_file_storage import UserFileStorage

class UserManager:
    def __init__(self):
        self.storage = UserFileStorage()
        self.users = self.storage.load_users()  # dict com username -> User

    def register_user(self, username, password):
        LoginValidator.validate(username)
        PasswordValidator.validate(password)
        
        # Verificação de unicidade do usuário
        if any(user.username == username for user in self.users):
            raise ValueError("Usuário já existe.")
        # Tudo correto
        self.users.append(User(username, password))
        self.storage.save_users(self.users)

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

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def save_users(self):
        # delega para storage
        self.storage.save_users(self.users)

    def update_gabarito(self, username, gabarito: dict):
        user = self.get_user(username)
        if not user:
            raise ValueError("Usuário não encontrado.")
        user.gabarito = gabarito
        self.save_users()
