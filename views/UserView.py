import streamlit as st
from Manager.user_manager import UserManager
from views.QuestionnaireView import QuestionnaireView # Você também precisará adaptar esta View

class UserView:
    def __init__(self):
        self.manager = UserManager()
        
        # Inicializa o estado de login se ainda não existir
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        if 'current_user' not in st.session_state:
            st.session_state['current_user'] = None

    def menu_streamlit(self):
        st.subheader("👤 Gerenciamento de Usuários")

        # 1. Fluxo Pós-Login
        if st.session_state['logged_in']:
            self._logged_in_view()
        
        # 2. Fluxo Pré-Login (Exibe Login, Registro e Lista)
        else:
            self._login_register_tabs()

    def _logged_in_view(self):
        """Mostra o menu do Questionário e o botão de Logout após o login."""
        
        st.success(f"Bem-vindo(a), {st.session_state['current_user']}!")
        
        # Botão de Logout
        if st.button("Sair (Logout)", type="secondary"):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = None
            st.rerun() # Reinicia a página para mostrar o menu de login

        st.divider()
        st.header("Responder Questionário")
        # Após o login, chamamos o menu do Questionário
        # NOTE: Você precisará garantir que QuestionnaireView.menu_streamlit() exista
        qview = QuestionnaireView(st.session_state['current_user'])
        qview.menu_streamlit()

    def _login_register_tabs(self):
        """Exibe as abas de Login, Registro e Listar Usuários."""
        
        tab_login, tab_register, tab_list = st.tabs(["🔒 Login", "✍️ Registrar", "📄 Listar"])
        
        with tab_login:
            self._login_view_streamlit()
            
        with tab_register:
            self._register_view_streamlit()

        with tab_list:
            self._listar_usuarios_view_streamlit()


    # -----------------------------------------------------------
    # Métodos de Ação (Refatorados do Terminal para Streamlit)
    # -----------------------------------------------------------
    
    def _register_view_streamlit(self):
        """Formulário de Registro de Usuário."""
        with st.form("form_register"):
            st.write("Crie sua conta:")
            username = st.text_input("Novo usuário:", key="reg_user")
            # O type="password" esconde a entrada
            password = st.text_input("Nova senha:", type="password", key="reg_pass")
            
            submitted = st.form_submit_button("Registrar")
            
            if submitted:
                try:
                    self.manager.register_user(username, password)
                    st.success(f"Usuário '{username}' registrado com sucesso! Agora faça o login.")
                except ValueError as e:
                    st.error(f"Erro no registro: {e}")

    def _login_view_streamlit(self):
        """Formulário de Login de Usuário."""
        with st.form("form_login"):
            st.write("Acesse sua conta:")
            username = st.text_input("Usuário:", key="log_user")
            password = st.text_input("Senha:", type="password", key="log_pass")
            
            submitted = st.form_submit_button("Entrar")
            
            if submitted:
                try:
                    if self.manager.login(username, password):
                        # Define o estado da sessão para TRUE e armazena o usuário
                        st.session_state['logged_in'] = True
                        st.session_state['current_user'] = username
                        st.success("Login bem-sucedido! Redirecionando...")
                        st.rerun() # Recarrega a página para mostrar o menu pós-login
                    else:
                        st.error("Usuário ou senha inválidos.")
                except ValueError as e:
                    st.error(f"Erro no login: {e}")

    def _listar_usuarios_view_streamlit(self):
        """Exibe a lista de usuários em formato de tabela/texto."""
        usuarios = self.manager.listar_usuarios()
        
        st.subheader("Usuários Registrados:")
        
        if not usuarios:
            st.info("Nenhum usuário registrado ainda.")
        else:
            # Converte a lista simples em um DataFrame para uma exibição melhor
            import pandas as pd
            df = pd.DataFrame(usuarios, columns=["Nome de Usuário"])
            st.dataframe(df, hide_index=True)