# metodos-UFPB
 Trabalho de Metodos de Projeto de Software

 Neste trabalho, implementaremos um sistema de apoio a idosos com Alzheimer, como forma de tardamento das perdas cognitivas dos usuários.

 A aplicação visa, com o acompanhamento da Inteligência Artificial, criar um caminho de jogos para os níveis de perdas cognitivas diversas. Tal que, o usuário receba um jogo de próxima fase, com base no seu desempenho na anterior, tendo em vista tardar a perca da memória.

 Para o desenvolvimento do projeto, a equipe escolhe o desenvolvimento web com a linguagem python com o framework Flask.

 Sprints:

 Sprint 1 - Desenvolvimento do Diagrama de Classes e Implementação inicial do caso de uso de gerenciar usuário.

 -Imagem 1 - Diagrama UML -

 ![alt text](image/image.png)

 -Imagem 2 - Diagrama de Classes - 

 ![alt text](image/image2.png)

 Sprint 2 - Atualização do Diagrama de Classes e Implementação de validação para login e senha e persistência de dados com arquivo JSON.

-Imagem 3 - Diagrama de Classes -

![alt text](image/image3.png)

## Questionário e Atividades (uso rápido)

Este repositório tem um CRUD de atividades e uma tela de questionário que usa as atividades como perguntas.

Cada atividade agora possui os campos adicionais:
- `tipo`: `text` ou `multiple` (texto livre ou múltipla escolha)
- `opcoes`: lista de opções (apenas para `multiple`)
- `categoria`: `pessoal` ou `objetiva` (define se a pergunta é pessoal do usuário ou uma pergunta objetiva com resposta conhecida)
- `resposta`: resposta correta (apenas para `objetiva`)

Comportamento importante:
- Ao criar uma atividade com `categoria = objetiva` você deve informar a `resposta` imediatamente. Para `tipo = text`, a resposta é armazenada em minúsculas. Para `multiple` pode-se informar a letra (ex: `a`) ou o texto da opção (será normalizado em minúsculas).
- Perguntas `pessoal` têm suas respostas salvas no gabarito do usuário na primeira vez que ele faz o questionário. Nas próximas execuções, as respostas pessoais são comparadas com esse gabarito salvo.
- Perguntas `objetiva` usam a `resposta` armazenada na própria atividade para comparar (não são salvas no gabarito do usuário).

Exemplos (via interface de Atividade):

- Criar pergunta objetiva (texto):
	- ID: `q_brasil`
	- Nome: `Descobrimento do Brasil`
	- Descrição: `Em que ano ocorreu o descobrimento do Brasil?`
	- Tipo: `text`
	- Categoria: `objetiva`
	- Resposta correta: `1500`  (será armazenada em minúsculas)

- Criar pergunta objetiva (múltipla escolha):
	- ID: `q_capital`
	- Nome: `Capital do Brasil`
	- Descrição: `Qual é a capital do Brasil?`
	- Tipo: `multiple`
	- Opções: `a) Brasília; b) Rio; c) São Paulo`
	- Categoria: `objetiva`
	- Resposta correta: `a`  (ou `a) Brasília`)

- Criar pergunta pessoal:
	- ID: `q_nome`
	- Nome: `Nome completo`
	- Descrição: `Qual seu nome completo?`
	- Tipo: `text`
	- Categoria: `pessoal`

Fluxo do questionário:
- Execute o app (ou rode `main.py`) e escolha o menu de Atividades para criar as atividades acima.
- Faça o cadastro/login de um usuário (se necessário).
- No menu do Questionário, escolha `Fazer questionário` e informe o username.

Comportamento esperado:
- Para a pergunta objetiva `q_brasil`: o sistema compara a resposta do usuário (convertida para minúsculas) com `1500` e informa se está correta.
- Para a pergunta objetiva `q_capital`: o usuário pode digitar `a` ou `a) Brasília` ou `brasília`; o sistema normaliza e compara com a resposta armazenada.
- Para a pergunta pessoal `q_nome`: na primeira execução a resposta será salva no gabarito do usuário; nas próximas vezes será comparada com o gabarito salvo.

Comandos rápidos (PowerShell):
```powershell
python main.py
```

Se quiser, eu posso adicionar um pequeno script de demonstração que cria um usuário e algumas atividades de exemplo automaticamente e executa um fluxo de questionário programático — quer que eu faça isso?
