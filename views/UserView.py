# user_view.py
from Manager.user_manager import UserManager

class UserView:
    def __init__(self):
        self.manager = UserManager()

    def menu(self):
        while True:
            print("\n1 - Registrar")
            print("2 - Login")
            print("3 - Listar Usuários")
            print("4 - Sair")
            op = input("Escolha uma opção: ")

            if op == "1":
                self.register_view()
            elif op == "2":
                self.login_view() 
            elif op == "3":
                self.listar_usuarios_view()
            elif op == "4":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

    def register_view(self):
        username = input("Novo usuário: ")
        password = input("Nova senha: ")
        try:
            self.manager.register_user(username, password)
            print("Usuário registrado com sucesso!")
        except ValueError as e:
            print(f"Erro no registro: {e}")

    def login_view(self):
        username = input("Usuário: ")
        password = input("Senha: ")
        try:
            if self.manager.login(username, password):
                print("Login bem-sucedido!")
        except ValueError as e:
            print(f"Erro no login: {e}")

    def listar_usuarios_view(self):
        usuarios = self.manager.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário registrado.")
        else:
            print("Usuários registrados:")
            for nome in usuarios:
                print(f"- {nome}")