from views.UserView import UserView
from views.AtividadeView import AtividadeView
from Repositories.user_repository import UserRepository
from Repositories.atividade_repository import AtividadeRepository
from Services.questionnaire_service import QuestionnaireService
from Manager.user_manager import UserManager
from Manager.atividade_manager import AtividadeManager

def main():
    while True:
        print("\n Sistema MemórIA ")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Atividades")
        print("3 - Executar Questionário")
        print("4 - Gerar Relatórios")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            user_view = UserView()
            user_view.menu()

        elif opcao == "2":
            atividade_view = AtividadeView()
            atividade_view.menu()

        elif opcao == "3":
            username = input("Digite o nome do usuário: ")

            user_manager = UserManager()
            atividade_manager = AtividadeManager()

            user_repo = UserRepository(user_manager)
            atividade_repo = AtividadeRepository(atividade_manager)

            service = QuestionnaireService(atividade_repo, user_repo)

            print("\n--- Questionário ---")
            questionario = service.carregar_questionario()

            respostas = {}
            for q in questionario.questions:
                print(f"\nPergunta {q.id}: {q.enunciado}")
                if hasattr(q, "opcoes") and q.opcoes:
                    for idx, opcao in enumerate(q.opcoes, start=1):
                        print(f"  {idx}. {opcao}")
                resposta = input("Sua resposta: ")
                respostas[q.id] = resposta

            resultado = service.avaliar_para_usuario(username, respostas)
            print("\n--- Resultado ---")
            print(f"Acertos: {resultado['acertos']} de {resultado['total']}")
            for det in resultado["detalhe"]:
                print(f"  {det['id']}: {'✔️' if det['correta'] else '❌'}")

        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        
        elif opcao == '4':
            from Presentation.RelatorioView import RelatorioView
            rel_view = RelatorioView(atividade_manager)
            rel_view.menu()
        else:
                    print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
