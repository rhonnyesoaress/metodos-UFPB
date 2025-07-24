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
        username = input("Digite um nome de usuário: ")
        password = input("Digite uma senha: ")
        if self.manager.register_user(username, password):
            print("Usuário registrado com sucesso!")
        else:
            print("Usuário já existe.")

    def login_view(self):
        username = input("Usuário: ")
        password = input("Senha: ")
        if self.manager.login(username, password):
            print(f"Bem-vindo, {username}!")
        else:
            print("Usuário ou senha incorretos.")

    def listar_usuarios_view(self):
        usuarios = self.manager.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário registrado.")
        else:
            print("Usuários registrados:")
            for nome in usuarios:
                print(f"- {nome}")