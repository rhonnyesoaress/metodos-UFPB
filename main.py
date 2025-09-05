from views.UserView import UserView
from views.AtividadeView import AtividadeView

def main():
    while True:
        print("\n Sistema MemórIA ")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Atividades")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            user_view = UserView()
            user_view.menu()
        elif opcao == "2":
            atividade_view = AtividadeView()
            atividade_view.menu()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
