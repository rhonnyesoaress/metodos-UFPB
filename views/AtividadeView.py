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
            info = f"ID: {a.id} | Nome: {a.nome} | Dificuldade: {a.dificuldade} | Tipo: {getattr(a, 'tipo', 'text')}"
            if getattr(a, 'tipo', 'text') == 'multiple':
                info += f" | Opções: {', '.join(getattr(a, 'opcoes', []))}"
            print(info)

    def criar(self):
        id = input("ID da atividade: ")
        nome = input("Nome: ")
        descricao = input("Descrição: ")
        dificuldade = input("Dificuldade (Fácil/Médio/Difícil): ") or "Fácil"
        tipo = input("Tipo (text/multiple) [text]: ") or "text"
        opcoes = None
        if tipo == 'multiple':
            raw = input("Opções (separe por ; ) Ex: a) Azul; b) Verde; c) Vermelho: ")
            opcoes = [o.strip() for o in raw.split(';') if o.strip()]

        categoria = input("Categoria (pessoal/objetiva) [pessoal]: ") or "pessoal"
        resposta = None
        # para perguntas objetivas, exigir resposta ao criar
        if categoria == 'objetiva':
            if tipo == 'text':
                raw_resp = input("Resposta correta (texto) - será armazenada em minúsculas: ")
                resposta = raw_resp.strip().lower()
            elif tipo == 'multiple':
                raw_resp = input("Resposta correta (coloque exatamente uma das opções ou a letra): ")
                # tentar normalizar letra para opção
                if raw_resp and len(raw_resp.strip()) == 1:
                    # letra - mapear mais tarde pelo questionário; aqui salvo a letra minúscula
                    resposta = raw_resp.strip().lower()
                else:
                    resposta = raw_resp.strip().lower()

        try:
            self.manager.criar(id, nome, descricao, dificuldade, tipo, opcoes, categoria, resposta)
            print("Atividade criada com sucesso!")
        except ValueError as e:
            print(e)

    def atualizar(self):
        id = input("ID da atividade a atualizar: ")
        nome = input("Novo nome (ou Enter para manter): ")
        descricao = input("Nova descrição (ou Enter para manter): ")
        dificuldade = input("Nova dificuldade (ou Enter para manter): ")
        tipo = input("Novo tipo (text/multiple) (ou Enter para manter): ")
        opcoes = None
        if tipo == 'multiple':
            raw = input("Novas opções (separe por ; ) (ou Enter para manter): ")
            if raw:
                opcoes = [o.strip() for o in raw.split(';') if o.strip()]
        categoria = input("Nova categoria (pessoal/objetiva) (ou Enter para manter): ")
        resposta = None
        if categoria == 'objetiva' or (not categoria and tipo == 'text'):
            # perguntar resposta caso seja objetiva e texto (se o usuário mudou para objetiva ou já era)
            raw_resp = input("Nova resposta correta (ou Enter para manter): ")
            if raw_resp:
                resposta = raw_resp.strip().lower()

        try:
            self.manager.atualizar(id, nome or None, descricao or None, dificuldade or None, tipo or None, opcoes, categoria or None, resposta)
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
