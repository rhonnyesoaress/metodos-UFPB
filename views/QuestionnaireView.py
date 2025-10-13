import streamlit as st
from Manager.user_manager import UserManager
from Manager.atividade_manager import AtividadeManager


class QuestionnaireView:
    """Versão Streamlit da View de Questionário.
    - Renderiza um questionário baseado nas atividades.
    - Salva/atualiza gabarito de respostas pessoais no UserManager.
    - Mostra resultado da comparação entre respostas e gabarito/resposta correta.
    """

    def __init__(self, username: str = None):
        self.username = username
        self.manager = UserManager()
        self.atividade_manager = AtividadeManager()

    def _get_questions_from_atividades(self):
        atividades = self.atividade_manager.listar()
        questions = []
        for a in atividades:
            questions.append({
                "id": str(a.id),
                "text": a.descricao or a.nome,
                "type": getattr(a, 'tipo', 'text'),
                "options": getattr(a, 'opcoes', []),
                "categoria": getattr(a, 'categoria', 'pessoal'),
                "resposta": getattr(a, 'resposta', None)
            })
        return questions

    @staticmethod
    def _normalize_answer(ans: str) -> str:
        if ans is None:
            return ""
        return ans.strip().lower()

    @staticmethod
    def _strip_option_label(text: str) -> str:
        if not text:
            return ""
        t = text.strip()
        if len(t) >= 2 and t[0].isalpha() and (t[1] == ')' or t[1] == '.'):
            return t[2:].strip().lower()
        return t.lower()

    # ---------------- Streamlit UI ----------------
    def menu_streamlit(self):
        st.subheader("Responder Questionário")

        # Se username não foi passado, pedir
        if not self.username:
            self.username = st.text_input("Usuário para o questionário:", key="q_user")

        if not self.username:
            st.info("Informe um usuário para iniciar o questionário.")
            return

        user = self.manager.get_user(self.username)
        if not user:
            st.error("Usuário não encontrado.")
            return

        questions = self._get_questions_from_atividades()
        if not questions:
            st.info("Nenhuma atividade disponível para gerar o questionário.")
            return

        # Usamos um form para submeter todas as respostas de uma vez
        form_key = f"form_questionnaire_{self.username}"
        with st.form(form_key):
            st.write(f"Questionário para: {self.username}")
            respostas = {}
            for q in questions:
                qid = q['id']
                qtext = q['text']
                categoria = q.get('categoria', 'pessoal')
                tipo = q.get('type', 'text')

                if tipo == 'multiple':
                    opts = q.get('options', [])
                    # mostrar como radio com as opções originais
                    escolha = st.radio(qtext, opts or ["(sem opções)"], key=f"q_{qid}")
                    # normalizar escolha: permitir letra ou texto inteiro
                    val = escolha
                    # Se for uma opção com rótulo (a) texto), armazenamos o texto
                    if isinstance(val, str):
                        norm = self._normalize_answer(val)
                        respostas[qid] = norm
                    else:
                        respostas[qid] = self._normalize_answer(str(val))
                else:
                    # campo de texto livre
                    if qtext and qtext.strip():
                        # Se qtext tiver conteúdo, mostre-o como um rótulo visível
                        ans_text = st.text_input(label=qtext, key=f"q_{qid}")
                    else:
                        # Se qtext estiver vazio, crie um rótulo para acessibilidade, mas esconda-o visualmente
                        ans_text = st.text_input(
                            label=f"Resposta para a questão {qid}", # Um rótulo descritivo para leitores de tela
                            key=f"q_{qid}",
                            label_visibility="collapsed" # ou "hidden"
                        )
                    if categoria == 'objetiva':
                        respostas[qid] = (ans_text or "").strip().lower()
                    else:
                        respostas[qid] = self._normalize_answer(ans_text)

            submitted = st.form_submit_button("Enviar respostas")

        if submitted:
            self._process_submission(user, questions, respostas)

    # ---------------- Lógica de Negócio ----------------
    def _process_submission(self, user, questions, respostas):
        # Salvar novas respostas pessoais no gabarito do usuário
        gabarito = user.gabarito or {}
        additions = {}
        for q in questions:
            if q.get('categoria', 'pessoal') == 'pessoal':
                qid = q['id']
                if not gabarito.get(qid):
                    additions[qid] = respostas.get(qid, "")
        if additions:
            gabarito.update(additions)
            self.manager.update_gabarito(self.username, gabarito)
            st.success("Novas respostas pessoais salvas no gabarito do usuário.")

        # Comparação e apresentação de resultados
        total = len(questions)
        acertos = 0
        rows = []
        for q in questions:
            qid = q['id']
            categoria = q.get('categoria', 'pessoal')
            tipo = q.get('type', 'text')

            # determinar referência correta
            if categoria == 'pessoal':
                resp_ref = self._normalize_answer(gabarito.get(qid, ""))
            else:
                raw_ref = q.get('resposta') or ""
                if tipo == 'multiple':
                    opts = q.get('options', [])
                    ref_norm = (raw_ref or "").strip().lower()
                    if len(ref_norm) == 1 and ref_norm >= 'a' and ref_norm <= 'z':
                        idx = ord(ref_norm) - ord('a')
                        if 0 <= idx < len(opts):
                            resp_ref = self._normalize_answer(self._strip_option_label(opts[idx]))
                        else:
                            resp_ref = ref_norm
                    else:
                        resp_ref = self._normalize_answer(self._strip_option_label(ref_norm))
                else:
                    resp_ref = (raw_ref or "").strip().lower()

            resp_now = respostas.get(qid, "") or ""
            if tipo == 'multiple' and resp_now:
                if not (len(resp_now) == 1 and 'a' <= resp_now <= 'z'):
                    resp_now = self._normalize_answer(self._strip_option_label(resp_now))

            igual = False
            if resp_ref and resp_ref == resp_now:
                igual = True
            else:
                if categoria == 'pessoal' and tipo == 'text' and resp_ref and resp_now:
                    if resp_ref in resp_now or resp_now in resp_ref:
                        igual = True
                if not igual and categoria == 'objetiva' and tipo == 'multiple':
                    opts = q.get('options', [])
                    if len(resp_now) == 1 and 'a' <= resp_now <= 'z':
                        idx = ord(resp_now) - ord('a')
                        if 0 <= idx < len(opts):
                            mapped = self._normalize_answer(self._strip_option_label(opts[idx]))
                            if mapped == resp_ref:
                                igual = True
                    else:
                        if resp_now == resp_ref:
                            igual = True

            if igual:
                acertos += 1

            display_ref = resp_ref or '<vazio>'
            if categoria == 'objetiva' and tipo == 'multiple' and display_ref and len(display_ref) == 1 and 'a' <= display_ref <= 'z':
                opts = q.get('options', [])
                idx = ord(display_ref) - ord('a')
                if 0 <= idx < len(opts):
                    display_ref = self._strip_option_label(opts[idx])

            rows.append({
                'Pergunta': q['text'],
                'Referência': display_ref,
                'Sua resposta': resp_now or '<vazio>',
                'Igual': 'Sim' if igual else 'Não'
            })

        # Exibir resumo e tabela
        st.write(f"Total: {acertos}/{total} perguntas iguais às referências.")
        try:
            import pandas as pd
            df = pd.DataFrame(rows)
            # use_container_width expands the dataframe to fill available width
            st.dataframe(df, width="stretch")
        except Exception:
            # fallback simples
            for r in rows:
                st.write(r)

