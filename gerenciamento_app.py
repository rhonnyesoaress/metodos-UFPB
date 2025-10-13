import streamlit as st
# Assumindo que suas classes UserView e AtividadeView estão no mesmo diretório
# E que elas possuem métodos que geram o conteúdo do Streamlit (em vez de menus de console).

# IMPORTANTE: Você precisará adaptar suas classes 'View' para
# usarem st.write, st.button, st.form, etc., em vez de print e input.
from views.UserView import UserView
from views.AtividadeView import AtividadeView 
from views.ReportView import ReportView

# Instancia as classes de View (a ser chamado conforme a escolha do menu)
user_view = UserView()
atividade_view = AtividadeView()

def main():
    st.set_page_config(
        page_title="MemórIA - Sistema de Gerenciamento",
        layout="centered"
    )

    st.title("🧠 Sistema MemórIA")

    # --- Estrutura de Menu com Abas (Tabs) ---
    # Usamos st.tabs para criar a navegação principal
    tab_inicio, tab_usuarios, tab_atividades, tab_relatorios = st.tabs(
        ["🏠 Início", "👤 Gerenciar Usuários", "📝 Gerenciar Atividades", "Gerar Relatórios"]
    )

    with tab_inicio:
        st.header("Bem-vindo(a) ao Sistema MemórIA!")
        st.markdown(
            """
            Use as abas acima para navegar entre o gerenciamento de Usuários e Atividades.

            **O que você precisa fazer agora?**
            - Clicar em "Gerenciar Usuários" para adicionar, visualizar ou editar usuários.
            - Clicar em "Gerenciar Atividades" para cadastrar e acompanhar atividades.
            """
        )

    with tab_usuarios:
        st.header("👤 Gerenciamento de Usuários")
        # Chama um método da sua classe adaptado para Streamlit
        # Sua UserView.menu() precisa ser reescrita para renderizar componentes
        user_view.menu_streamlit()

    with tab_atividades:
        st.header("📝 Gerenciamento de Atividades")
        # Chama um método da sua classe adaptado para Streamlit
        # Sua AtividadeView.menu() precisa ser reescrita para renderizar componentes
        atividade_view.menu_streamlit()

    with tab_relatorios:
        st.header("📊 Geração de Relatórios")
        # Instancia ReportView com as atividades gerenciadas
        # Você precisará passar a lista ou gerenciador de atividades
        # Aqui assumimos que atividade_view tem um atributo 'atividades'
        report_view = ReportView(atividade_view.manager)
        report_view.render()

if __name__ == "__main__":
    main()