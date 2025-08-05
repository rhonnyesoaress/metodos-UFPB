# user_manager.py
from Entidades.user import User
from Validators.login_validator import LoginValidator
from Validators.password_validator import PasswordValidator
from Storages.user_file_storage import UserFileStorage

class UserManager:
    def __init__(self):
        self.storage = UserFileStorage()
        self.users = self.storage.load_users()  # dict com username -> User

    # def _load_users(self):
    #     if os.path.exists(self.file_path):
    #         try:
    #             with open(self.file_path, 'r') as f:
    #                 data = json.load(f)
    #                 if isinstance(data, list):
    #                     return [User.from_dict(user_data) for user_data in data]
    #                 else:
    #                     print('Aviso: Arquivo users.json está mal formatado. Criando nova lista.')
    #         except (json.JSONDecodeError, FileNotFoundError):
    #             print('Aviso: Arquivo users.json está corrompido ou vazio. Criano nova lista.')
    #     return []
        
    # def _save_users(self):
    #     with open(self.file_path, 'w') as f:
    #         data = [user.to_dict() for user in self.users]
    #         json.dump(data, f, indent=4)

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
