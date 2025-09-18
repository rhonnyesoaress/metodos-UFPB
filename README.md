# metodos-UFPB
 Trabalho de Metodos de Projeto de Software

 Neste trabalho, implementaremos um sistema de apoio a idosos com Alzheimer, como forma de tardamento das perdas cognitivas dos usuários.

 A aplicação visa, com o acompanhamento da Inteligência Artificial, criar um caminho de jogos para os níveis de perdas cognitivas diversas. Tal que, o usuário receba um jogo de próxima fase, com base no seu desempenho na anterior, tendo em vista tardar a perca da memória.

 Para o desenvolvimento do projeto, a equipe escolhe o desenvolvimento web com a linguagem python com o framework Flask.

 Documentação de requisitos do projeto: - https://docs.google.com/document/d/1GsUDEq24Sa9pXWozzbTYL8AJC163UCiJ7rDML9g-Ygs/edit?usp=sharing - 
 Sprints:

 Sprint 1 - Desenvolvimento do Diagrama de Classes e Implementação inicial do caso de uso de gerenciar usuário.

 -Imagem 1 - Diagrama UML -

 ![alt text](image/image.png)

 -Imagem 2 - Diagrama de Classes - 

 ![alt text](image/image2.png)

 Sprint 2 - Atualização do Diagrama de Classes - Implementação de validação para login e senha e persistência de dados com arquivo JSON.

-Imagem 3 - Diagrama de Classes -

![alt text](image/image3.png)

Sprint 3 - Atualização do Diagrama de Classe - Implementação da camada de Task.

-Imagem 4 - Diagrama de Classes -

![alt text](image/image4.png)

Sprint 4 - Diagrama de Classes - Separação das camadas de business e persistência, implementando o uso de Factory Method. Além do uso do padrão Adapter para o cenário de "adaptar" a interface do LegacyUserStorage para a interface DAO . Na camada business foi implementado com Template Method a geração de relotório em HTML e PDF, gerando estatísticas de acesso ao sistema pelo usuário

-Imagem 5 - Diagrama de Classes -

![alt text](image/image5.jpg)
