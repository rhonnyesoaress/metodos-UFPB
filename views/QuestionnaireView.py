from Manager.user_manager import UserManager
from Manager.atividade_manager import AtividadeManager


class QuestionnaireView:
    """Apresenta um questionário de 10 perguntas. Na primeira vez que o usuário responde,
    suas respostas são salvas como gabarito (respostas "corretas"). Nas próximas vezes, as
    respostas do usuário são comparadas com o gabarito e mostra o resultado.
    """

    def _get_questions_from_atividades(self):
        atividades = self.atividade_manager.listar()
        questions = []
        for a in atividades:
            # usar o id da atividade como chave do item do questionário
            questions.append({
                "id": str(a.id),
                "text": a.descricao or a.nome,
                "type": getattr(a, 'tipo', 'text'),
                "options": getattr(a, 'opcoes', []),
                "categoria": getattr(a, 'categoria', 'pessoal'),
                "resposta": getattr(a, 'resposta', None)
            })
        return questions

    def __init__(self, username: str = None):
        self.username = username
        self.manager = UserManager()
        self.atividade_manager = AtividadeManager()

    @staticmethod
    def _normalize_answer(ans: str) -> str:
        if ans is None:
            return ""
        return ans.strip().lower()

    @staticmethod
    def _strip_option_label(text: str) -> str:
        """Remove possíveis rótulos de opção como 'a)', 'b)', 'a) ' ou 'a.' no início."""
        if not text:
            return ""
        t = text.strip()
        # remover rótulos como 'a) ', 'a)','a.' ou 'a.' seguido de espaço
        if len(t) >= 2 and t[0].isalpha() and (t[1] == ')' or t[1] == '.'):
            return t[2:].strip().lower()
        return t.lower()

    def run(self):
        user = self.manager.get_user(self.username)
        if not user:
            print("Usuário não encontrado para questionário.")
            return
        # carregar perguntas a partir das atividades
        questions = self._get_questions_from_atividades()
        if not questions:
            print("Nenhuma atividade disponível para gerar o questionário.")
            return

        first_time = not bool(user.gabarito)

        print(f"\nQuestionário para: {self.username}")
        respostas = {}

        for q in questions:
            print("\n" + q["text"])
            categoria = q.get("categoria", "pessoal")
            # se for objetiva e do tipo text, instruir sobre caixa baixa
            if q.get("type") == "multiple":
                opts = q.get("options", [])
                letters = []
                for i, opt in enumerate(opts):
                    letter = chr(ord('a') + i)
                    letters.append(letter)
                    print(f"{letter}) {opt}")
                ans = input("Escolha (escreva a letra ou a resposta): ")
                norm = self._normalize_answer(ans)
                if len(norm) == 1 and norm in letters:
                    index = ord(norm) - ord('a')
                    mapped = opts[index] if index < len(opts) else ""
                    user_answer = self._normalize_answer(mapped)
                else:
                    user_answer = norm
            else:
                ans = input("Resposta: ")
                # se objetiva e texto, guardar em minusculas
                if categoria == 'objetiva':
                    user_answer = (ans or "").strip().lower()
                else:
                    user_answer = self._normalize_answer(ans)

            # para perguntas pessoais, armazenamos o valor no dicionário de respostas do usuário
            # para perguntas objetivas, a resposta correta deve estar em q['resposta'] (definida na criação)
            respostas[q["id"]] = user_answer

        # Salvar novas respostas pessoais no gabarito do usuário (mesmo que já exista um gabarito)
        gabarito = user.gabarito or {}
        additions = {}
        for q in questions:
            if q.get('categoria', 'pessoal') == 'pessoal':
                qid = q['id']
                # se não existe referência para esta pergunta no gabarito, salvar a resposta atual
                if not gabarito.get(qid):
                    # guardar a resposta do usuário (normalizada)
                    additions[qid] = respostas.get(qid, "")
        if additions:
            # mesclar e salvar
            gabarito.update(additions)
            self.manager.update_gabarito(self.username, gabarito)
            print("Novas respostas pessoais salvas no gabarito do usuário.")
        total = len(questions)
        acertos = 0
        print("\nResultado da comparação:")
        for q in questions:
            qid = q["id"]
            categoria = q.get('categoria', 'pessoal')
            tipo = q.get('type', 'text')

            # determinar referência correta
            if categoria == 'pessoal':
                resp_ref = self._normalize_answer(gabarito.get(qid, ""))
            else:
                # objetiva -> referência vem da atividade; normalizar conforme tipo
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
                        # pode ser texto da opção; normalizar removendo rótulos
                        resp_ref = self._normalize_answer(self._strip_option_label(ref_norm))
                else:
                    resp_ref = (raw_ref or "").strip().lower()

            resp_now = respostas.get(qid, "") or ""
            # se resp_now vem de uma opção mapeada, também strip labels
            if tipo == 'multiple' and resp_now:
                # se resp_now é uma letra, mantemos como letra (tratamos depois)
                if not (len(resp_now) == 1 and 'a' <= resp_now <= 'z'):
                    resp_now = self._normalize_answer(self._strip_option_label(resp_now))

            igual = False
            # comparação principal (já normalizada quando aplicável)
            if resp_ref and resp_ref == resp_now:
                igual = True
            else:
                # regras tolerantes para texto pessoal: substring
                if categoria == 'pessoal' and tipo == 'text' and resp_ref and resp_now:
                    if resp_ref in resp_now or resp_now in resp_ref:
                        igual = True
                # se referência é uma opção (multiple) e resp_now é uma letra, mapear e comparar
                if not igual and categoria == 'objetiva' and tipo == 'multiple':
                    opts = q.get('options', [])
                    # se resp_now é uma letra, mapear
                    if len(resp_now) == 1 and 'a' <= resp_now <= 'z':
                        idx = ord(resp_now) - ord('a')
                        if 0 <= idx < len(opts):
                            mapped = self._normalize_answer(self._strip_option_label(opts[idx]))
                            if mapped == resp_ref:
                                igual = True
                    else:
                        # se resp_now é texto, já normalizamos acima
                        if resp_now == resp_ref:
                            igual = True

            if igual:
                acertos += 1

            # mostrar referência de forma legível: para múltipla escolha, tentar mapear letra para opção
            display_ref = resp_ref or '<vazio>'
            if categoria == 'objetiva' and tipo == 'multiple' and display_ref and len(display_ref) == 1 and 'a' <= display_ref <= 'z':
                opts = q.get('options', [])
                idx = ord(display_ref) - ord('a')
                if 0 <= idx < len(opts):
                    display_ref = self._strip_option_label(opts[idx])

            print(f"{q['text']}\n  Referência: {display_ref}\n  Sua resposta: {resp_now or '<vazio>'}\n  Igual: {'Sim' if igual else 'Não'}\n")

        print(f"Total: {acertos}/{total} perguntas iguais às referências.")

    # adaptar ao estilo de menu do AtividadeView
    def menu(self):
        while True:
            print("\n1 - Listar atividades")
            print("2 - Fazer questionário")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                self.listar_atividades()
            elif opcao == "2":
                # se username não foi passado, pedir
                if not self.username:
                    self.username = input("Usuário para o questionário: ")
                self.run()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

    def listar_atividades(self):
        atividades = self.atividade_manager.listar()
        if not atividades:
            print("Nenhuma atividade cadastrada.")
            return
        for a in atividades:
            print(f"ID: {a.id} | Nome: {a.nome} | Dificuldade: {a.dificuldade}")
