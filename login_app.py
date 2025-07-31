import streamlit as st
from Manager.user_manager import UserManager

# Inicializa a instância no estado da sessão
if "manager" not in st.session_state:
    st.session_state.manager = UserManager()

st.title("🔐 Sistema de Login com Streamlit")

aba = st.radio("Escolha uma opção:", ["Login", "Registrar", "Usuários Registrados"])

# LOGIN
if aba == "Login":
    st.subheader("Fazer Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if st.session_state.manager.login(username, password):
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Usuário ou senha incorretos.")

# REGISTRO
elif aba == "Registrar":
    st.subheader("Registrar Novo Usuário")

    if "reg_username" not in st.session_state:
        st.session_state.reg_username = ""
    if "reg_password" not in st.session_state:
        st.session_state.reg_password = ""

    st.session_state.reg_username = st.text_input("Novo usuário", value=st.session_state.reg_username, key="username_input")
    st.session_state.reg_password = st.text_input("Nova senha", type="password", value=st.session_state.reg_password, key="password_input")

    if st.button("Registrar"):
        if st.session_state.reg_username.strip() == "" or st.session_state.reg_password.strip() == "":
            st.warning("Preencha todos os campos.")
        elif st.session_state.manager.register_user(st.session_state.reg_username, st.session_state.reg_password):
            st.success("Usuário registrado com sucesso!")
            # Limpa campos após sucesso
            st.session_state.reg_username = ""
            st.session_state.reg_password = ""
        else:
            st.warning("Usuário já existe.")

# LISTAR USUÁRIOS
elif aba == "Usuários Registrados":
    st.subheader("Lista de Usuários")
    usuarios = st.session_state.manager.listar_usuarios()
    if not usuarios:
        st.info("Nenhum usuário registrado ainda.")
    else:
        st.write("Usuários:")
        for u in usuarios:
            st.write(f"- {u}")