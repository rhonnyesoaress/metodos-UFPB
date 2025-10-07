import streamlit as st
import pandas as pd
from Manager.atividade_manager import AtividadeManager 
# Assumindo que AtividadeManager está acessível

class AtividadeView:
    def __init__(self):
        self.manager = AtividadeManager()

    def menu_streamlit(self):
        """
        Substitui o menu do terminal por abas do Streamlit.
        """
        st.subheader("📝 Gerenciamento de Atividades")

        # Cria as abas para as diferentes operações
        tab_list, tab_create, tab_update, tab_delete = st.tabs(
            ["📋 Listar", "➕ Criar", "✏️ Atualizar", "🗑️ Deletar"]
        )

        with tab_list:
            self._listar_streamlit()
        
        with tab_create:
            self._criar_streamlit()

        with tab_update:
            self._atualizar_streamlit()

        with tab_delete:
            self._deletar_streamlit()

    # -----------------------------------------------------------
    # Métodos de Ação (Refatorados do Terminal para Streamlit)
    # -----------------------------------------------------------

    def _listar_streamlit(self):
        """
        Exibe a lista de atividades em um st.dataframe.
        """
        atividades = self.manager.listar()

        if not atividades:
            st.info("Nenhuma atividade cadastrada.")
            return

        # Prepara os dados para o DataFrame
        data = []
        for a in atividades:
            row = {
                "ID": a.id,
                "Nome": a.nome,
                "Descrição": a.descricao,
                "Dificuldade": a.dificuldade,
                "Tipo": getattr(a, 'tipo', 'text'),
                "Categoria": getattr(a, 'categoria', 'pessoal'),
                # Adiciona opções/resposta se existirem e for relevante
                "Detalhes": self._formatar_detalhes(a)
            }
            data.append(row)

        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    def _formatar_detalhes(self, atividade):
        """Função auxiliar para formatar detalhes específicos."""
        detalhes = []
        
        tipo = getattr(atividade, 'tipo', 'text')
        categoria = getattr(atividade, 'categoria', 'pessoal')

        if tipo == 'multiple' and hasattr(atividade, 'opcoes') and atividade.opcoes:
            detalhes.append(f"Opções: {', '.join(atividade.opcoes)}")
        
        if categoria == 'objetiva' and hasattr(atividade, 'resposta') and atividade.resposta:
            detalhes.append(f"Resposta Correta: {atividade.resposta}")
            
        return " | ".join(detalhes) if detalhes else "N/A"


    def _criar_streamlit(self):
        """
        Formulário para criar uma nova atividade.
        """
        with st.form("form_criar_atividade", clear_on_submit=True):
            st.write("Insira os dados da nova atividade:")

            # Colunas para organização do formulário
            col1, col2 = st.columns(2)
            
            with col1:
                id_a = st.text_input("ID da atividade:", help="ID deve ser único.")
                nome = st.text_input("Nome:")
                dificuldade = st.selectbox(
                    "Dificuldade:", 
                    ["Fácil", "Médio", "Difícil"], 
                    index=0 # Padrão para Fácil
                )
                categoria = st.selectbox(
                    "Categoria:", 
                    ["pessoal", "objetiva"], 
                    index=0 # Padrão para pessoal
                )

            with col2:
                descricao = st.text_area("Descrição:")
                tipo = st.selectbox(
                    "Tipo:", 
                    ["text", "multiple"], 
                    index=0 # Padrão para text
                )
            
            # Campos condicionais (opções para tipo 'multiple' e resposta para 'objetiva')
            opcoes = None
            if tipo == 'multiple':
                raw_opcoes = st.text_input(
                    "Opções (separe por ; ):",
                    help="Ex: a) Azul; b) Verde; c) Vermelho"
                )
                if raw_opcoes:
                    opcoes = [o.strip() for o in raw_opcoes.split(';') if o.strip()]

            resposta = None
            if categoria == 'objetiva':
                resposta = st.text_input(
                    "Resposta correta:",
                    help="Para 'multiple' use exatamente uma das opções ou a letra. Para 'text' use o texto exato."
                )
                # Normalização da resposta (como feito no código original)
                if resposta:
                    resposta = resposta.strip().lower()

            submitted = st.form_submit_button("Criar Atividade")

            if submitted:
                try:
                    self.manager.criar(
                        id_a, 
                        nome, 
                        descricao, 
                        dificuldade, 
                        tipo, 
                        opcoes, 
                        categoria, 
                        resposta
                    )
                    st.success("Atividade criada com sucesso!")
                except ValueError as e:
                    st.error(f"Erro ao criar atividade: {e}")

    
    def _atualizar_streamlit(self):
        """
        Formulário para atualizar uma atividade existente.
        """
        st.info("Para atualizar, o ID é obrigatório. Deixe os outros campos vazios para manter o valor atual.")
        
        # O formulário de atualização é similar ao de criação, mas todos os campos são opcionais (exceto ID)
        with st.form("form_atualizar_atividade", clear_on_submit=True):
            id_a = st.text_input("ID da atividade a atualizar:")

            # Campos opcionais
            nome = st.text_input("Novo Nome:")
            descricao = st.text_area("Nova Descrição:")
            dificuldade = st.selectbox(
                "Nova Dificuldade:", 
                ["", "Fácil", "Médio", "Difícil"], # Adiciona opção vazia para manter
                index=0
            )
            tipo = st.selectbox(
                "Novo Tipo:", 
                ["", "text", "multiple"], 
                index=0
            )
            categoria = st.selectbox(
                "Nova Categoria:", 
                ["", "pessoal", "objetiva"], 
                index=0
            )
            
            opcoes = None
            # Mostrar campo de opções se o tipo for (ou estiver sendo mudado para) 'multiple'
            if tipo == 'multiple':
                raw_opcoes = st.text_input(
                    "Novas Opções (separe por ; ) (deixe vazio para manter):",
                )
                # Se o usuário digitou algo, processa as novas opções
                if raw_opcoes:
                    opcoes = [o.strip() for o in raw_opcoes.split(';') if o.strip()]
            
            resposta = None
            # Mostrar campo de resposta se a categoria for (ou estiver sendo mudada para) 'objetiva'
            if categoria == 'objetiva':
                raw_resp = st.text_input("Nova Resposta Correta (deixe vazio para manter):")
                if raw_resp:
                    resposta = raw_resp.strip().lower()


            submitted = st.form_submit_button("Atualizar Atividade")

            if submitted:
                # O Streamlit retorna strings vazias ('') ou None/False (para selects). 
                # Passamos None para o manager, a menos que o campo seja essencial.
                
                if not id_a:
                    st.error("O ID da atividade é obrigatório para atualização.")
                    return

                try:
                    self.manager.atualizar(
                        id_a,
                        nome or None,
                        descricao or None,
                        dificuldade or None,
                        tipo or None,
                        opcoes, # Passa as opções (lista ou None)
                        categoria or None,
                        resposta # Passa a resposta (string ou None)
                    )
                    st.success("Atividade atualizada com sucesso!")
                except ValueError as e:
                    st.error(f"Erro ao atualizar atividade: {e}")


    def _deletar_streamlit(self):
        """
        Formulário para deletar uma atividade.
        """
        st.warning("Esta ação é irreversível.")
        
        with st.form("form_deletar_atividade", clear_on_submit=True):
            id_a = st.text_input("ID da atividade a deletar:")
            
            # O botão de deletar é vermelho/perigoso
            submitted = st.form_submit_button("Deletar Atividade", type="primary") 

            if submitted:
                if not id_a:
                    st.error("O ID da atividade é obrigatório.")
                    return

                try:
                    self.manager.deletar(id_a)
                    st.success(f"Atividade com ID '{id_a}' deletada com sucesso!")
                except ValueError as e:
                    st.error(f"Erro ao deletar atividade: {e}")