
# CaféLab ☕📱

## Bem-vindo ao CaféLab!

O CaféLab é um aplicativo multi-device que transforma a experiência de compra rápida de alimentos para alunos de graduação em algo mais prático, social e interativo. 🍽️📲 Com o CaféLab, você pode explorar máquinas de venda automática, ver avaliações, receber notificações importantes e até deixar comentários sobre os produtos! 🚀

Este projeto faz parte do curso de Engenharia de Software (2024.2) da Escola de Matemática Aplicada da Fundação Getulio Vargas (FGV - EMAp). 🎓

## Funcionalidades Implementadas:

### Sprint 1:

- **(RF33) Reportar Problemas:** Como usuário quero poder reportar problemas com as vending machines ou com a rede social e o gestor pode visualizá-las para que sejam resolvidas.


https://github.com/user-attachments/assets/fb8eeb25-e63f-4abd-9e33-de47a438287e

https://github.com/user-attachments/assets/98f6dec0-30f2-4be5-abc6-dd6ec3cfcba1


#### Como Rodar

Para rodar, basta estar na root e rodar o arquivo `main.py` (`pyhton3 web/main.py`) e abrir o `http://localhost:5000/report` ou `http://localhost:5000/manager_dashboard`

### Sprint 2: 

- **(RF40) Suporte a Diferentes Idiomas:** Como usuário, quero que o sistema esteja disponível em diferentes idiomas para que eu possa usá-lo confortavelmente.

#### Como Traduzir

Primeiro, no diretório `web`, precisamos puxar todos os textos que estão marcados no html para o arquivo `messages.pot` usando o comando `python3 -m babel.messages.frontend extract -F babel.cfg -o messages.pot .`.

Depois, precisamos traduzir os textos para o idioma desejado e salvar no arquivo `messages.po`. Por exemplo, para traduzir para o espanhol, usamos o comando `python3 -m babel.messages.frontend init -i messages.pot -d translations -l pt`

Por fim, precisamos compilar os arquivos `messages.po` para gerar o arquivo `messages.mo` usando o comando `python3 -m babel.messages.frontend compile -d translations`.

## 👨‍💻 Equipe de Desenvolvimento
Esta é a página do grupo 4 da disciplina de Engenharia de Software ministrada em 2024.2 pelo Prof. Dr. Rafael de Pinho. Nosso grupo é composto por [Fabrício Venturim](https://github.com/FabricioVenturim), [Gabriel Pereira](https://github.com/GabrielJP314), [Luís Felipe Marques](https://github.com/felipponn), e [Otávio Alves](https://github.com/atronee). 🎓💼

## 📙 Site com entregáveis
[Clique aqui](https://felipponn.github.io/software-engineering/).
