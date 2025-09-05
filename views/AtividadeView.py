from Manager.atividade_manager import AtividadeManager

class AtividadeView:
    def __init__(self):
        self.manager = AtividadeManager()

    def menu(self):
        while True:
            print("1 - Listar atividades")
            print("2 - Criar atividade")
            print("3 - Atualizar atividade")
            print("4 - Deletar atividade")
            print("0 - Sair")

            opcao = input("Escolha: ")

            if opcao == "1":
                self.listar()
            elif opcao == "2":
                self.criar()
            elif opcao == "3":
                self.atualizar()
            elif opcao == "4":
                self.deletar()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

    def listar(self):
        atividades = self.manager.listar()
        if not atividades:
            print("Nenhuma atividade cadastrada.")
        for a in atividades:
            print(f"ID: {a.id} | Nome: {a.nome} | Dificuldade: {a.dificuldade}")

    def criar(self):
        id = input("ID da atividade: ")
        nome = input("Nome: ")
        descricao = input("Descrição: ")
        dificuldade = input("Dificuldade (Fácil/Médio/Difícil): ") or "Fácil"
        try:
            self.manager.criar(id, nome, descricao, dificuldade)
            print("Atividade criada com sucesso!")
        except ValueError as e:
            print(e)

    def atualizar(self):
        id = input("ID da atividade a atualizar: ")
        nome = input("Novo nome (ou Enter para manter): ")
        descricao = input("Nova descrição (ou Enter para manter): ")
        dificuldade = input("Nova dificuldade (ou Enter para manter): ")
        try:
            self.manager.atualizar(id, nome or None, descricao or None, dificuldade or None)
            print("Atividade atualizada com sucesso!")
        except ValueError as e:
            print(e)

    def deletar(self):
        id = input("ID da atividade a deletar: ")
        try:
            self.manager.deletar(id)
            print("Atividade deletada com sucesso!")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    view = AtividadeView()
    view.menu()
