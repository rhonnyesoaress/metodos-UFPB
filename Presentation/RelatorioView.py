# Presentation/RelatorioView.py
from Business.Bridge.implementors import FileOutputImplementor, ConsoleOutputImplementor
# Importa a nova classe de relatório
from Business.Bridge.abstractions import ActivityReport, LogReport

class RelatorioView:
    def __init__(self, atividade_manager):
        self._atividade_manager = atividade_manager

    def menu(self):
        print("\n--- Geração de Relatórios (Bridge) ---")
        print("Qual relatório deseja gerar?")
        # --- MUDANÇA AQUI ---
        print("1 - Relatório de Estatísticas de Atividades")
        print("2 - Relatório de Log de Movimentações") # <-- NOVA OPÇÃO
        
        report_choice = input("Escolha: ")
        
        print("\nOnde deseja salvar o relatório?")
        print("1 - Em um arquivo (report.txt)")
        print("2 - Exibir no Console")
        
        output_choice = input("Escolha: ")

        # Seleciona o implementor (lógica existente, sem alterações)
        if output_choice == '1':
            implementor = FileOutputImplementor("report.txt")
        elif output_choice == '2':
            implementor = ConsoleOutputImplementor()
        else:
            print("Opção de saída inválida.")
            return

        # Seleciona a abstração e a combina com o implementor
        report = None
        if report_choice == '1':
            report = ActivityReport(implementor, self._atividade_manager)
        
        # --- NOVO BLOCO DE LÓGICA AQUI ---
        elif report_choice == '2':
            # Cria a instância do novo relatório, passando o caminho do arquivo de log
            report = LogReport(implementor, "memoria.log")
        
        # A lógica de exportação funciona para qualquer tipo de relatório
        if report:
            report.export()
        else:
            print("Opção de relatório inválida.")