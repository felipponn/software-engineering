---
title: "Listagem de requisitos"
permalink: /posts/2024/08/requisitos-1/
date: 2024-08-29
---

# Entrevista

## Requisitos Funcionais

RF02: Pagamento sem aplicativos da máquina (direto no nosso app) + comprovante digital.

RF04: Notificação de pagamento.

RF07: Usuários podem fazer comentários sobre produtos e serviços.

RF07: Avaliação tanto dos produtos quanto dos vendedores após pagamento.

RF18: Receber notificações de promoções, produtos novos e tudo.

RF19: O sistema deve permitir que os usuários personalizem as notificações.

RF22: Usuários podem fazer perfis com foto, informações pessoais, histórico de compra.

RF23: Seguir outros usuários.

RF24: Conversar com outros usuários.

RF27: Bonificação do usuário.

RF29: Gamificação do app, com rank e desafios.

RF32: Personalizar o app.

RF33: Reportar problema em relação a compras no app/site, ou qualquer interação.

## Requisitos Não Funcionais

RF03: Segurança dos dados do usuário em relação ao pagamento. (Product Requirements / Security Requirements)



# História de usuário


## Otavio Matos's User Story

### INITIAL ASSUMPTION:
O usuário é um estudante universitário que baixou o aplicativo e criou um perfil. Ele quer vender alguns de seus produtos no aplicativo.

### NORMAL:
- O usuário inicia o aplicativo em seu dispositivo.
- O usuário toca no botão "Vender" ou "Tornar-se um vendedor".
- O usuário é solicitado a inserir detalhes sobre o produto que deseja vender, incluindo: Nome do produto, Descrição, Preço, Categoria (por exemplo, livros, eletrônicos, roupas), Fotos
- O usuário escolhe se deseja lidar com o envio ou oferecer entrega local. Se oferecer entrega local, ele pode especificar sua localização.
- O usuário avalia os detalhes da listagem e a envia para aprovação.

### What can go wrong:
- Se o usuário inserir informações incompletas ou incorretas, o sistema deve exibir mensagens de erro e solicitar que ele corrija os detalhes.
- O sistema pode exigir um número mínimo de fotos para cada listagem de produto. Se o usuário não fornecer fotos suficientes, ele deve ser notificado e solicitado a adicionar mais.
- O sistema pode ter um processo de moderação para revisar e aprovar as listagens antes que elas fiquem visíveis para outros usuários. Se a listagem não atender às diretrizes da plataforma, ela pode ser rejeitada ou exigir revisões.

### Other activities: 
- O usuário pode atualizar ou remover suas listagens conforme necessário.
- O sistema deve registrar a criação, modificação e exclusão de listagens, juntamente com as ações e carimbos de data/hora do usuário.

### System state on completion: 
- O perfil do usuário é atualizado para incluir a nova listagem de produtos.
- A listagem do produto é adicionada ao marketplace do aplicativo para que outros usuários visualizem e comprem.
- Um registro é adicionado ao log do sistema indicando a criação da listagem do produto e o usuário envolvido.

---

## Fabricio Venturim's User Story

### Estória de Usuário:
Como usuário, quero poder procurar pessoas na rede social, segui-las e enviar mensagens, para que eu possa interagir e me conectar com amigos.

### Caso de Uso:
#### Initial assumption:
O usuário já possui uma conta na rede social e está logado no sistema.

#### Normal: 
1. O usuário acessa a página de pesquisa e insere o nome do amigo que deseja seguir.
2. O sistema exibe os resultados da pesquisa com os perfis correspondentes.
   2. O amigo não é encontrado na pesquisa devido a um erro de digitação, falha no sistema de busca ou amigo não cadastrado. 
   3. O sistema então alerta que nenhum usuário foi encontrado ou que não foi possível fazer a busca (caso de conexão).
3. O usuário localiza o perfil correto e clica no nome do amigo para acessar o perfil.
4. Dentro do perfil do amigo, o usuário clica no botão "Seguir".
   1. Usuário pode enviar mensagem antes de seguir (passo 6)
5. O sistema atualiza o status, indicando que o usuário agora está seguindo o amigo.
6. O usuário, ainda no perfil, clica na opção "Enviar mensagem".
7. Uma janela de bate-papo se abre, e o usuário escreve sua mensagem e a envia.
   1. A mensagem não pode ser enviada devido a problemas de conectividade. O sistema salva a mensagem em rascunho e tenta enviá-la automaticamente quando a conexão for restabelecida.
   2. O usuário pode cancelar que aquela mensagem seja enviada automaticamente quando a conexão for restabelecida.
8. O sistema confirma o envio da mensagem e a exibe no histórico de conversas.


#### What can go wrong:
1. O amigo não é encontrado na pesquisa devido a um erro de digitação, falha no sistema de busca ou amigo não cadastrado. O sistema alerta que nenhum usuário foi encontrado ou que não foi possível fazer a busca (caso de conexão).
2. O botão "Seguir" não aparece ou não responde dentro do perfil devido a uma falha de conexão. O sistema deve notificar o usuário para tentar novamente mais tarde.
3. A mensagem não pode ser enviada devido a problemas de conectividade. O sistema salva a mensagem em rascunho e tenta enviá-la automaticamente quando a conexão for restabelecida. O usuário pode cancelar que aquela mensagem seja enviada automaticamente quando a conexão for restabelecida.

#### Other activities: 
- Enquanto o usuário está enviando a mensagem, ele pode continuar navegando no perfil do amigo ou em outras áreas da rede social. O sistema salva a mensagem em rascunho para quando ele voltar.
- O usuário pode enviar uma mensagem para o amigo antes de seguir ele.

#### System state on completion: 
- O usuário agora está seguindo o amigo, e a mensagem foi enviada e registrada no histórico de conversas. O sistema armazena a data e hora do seguimento e do envio da mensagem, além dos perfis envolvidos.

---

## Gabriel Pereira User Story and Use Case

### Estória de Usuário
Estória: Como entregador, quero poder visualizar e aceitar os pedidos de café em tempo real para que eu possa gerenciar minhas entregas de maneira eficiente.

### Caso de Uso
Ator: Entregador

Descrição: O entregador já possui uma conta na rede social de pedidos de café e está logado no sistema. Ele navega pelo aplicativo, acessa a lista de pedidos disponíveis, visualiza os detalhes de cada pedido, seleciona o pedido que deseja entregar, confirma a escolha para iniciar a entrega, e o sistema atualiza o status do pedido.

#### Fluxo Principal:
1. O entregador realiza o login.
1. O entregador acessa a página de pedidos.
1. O entregador visualiza os pedidos em aberto.
1. O entregador seleciona um pedido.
1. O entregador confirma a entrega.
1. O sistema atualiza o status do pedido para “em entrega”.

#### O que pode dar errado:
1. Problema de conexão: O entregador não consegue visualizar os pedidos disponíveis devido a uma falha de conectividade. O sistema exibe uma mensagem de erro e sugere que o entregador tente novamente mais tarde.
1. Pedido já aceito: O pedido que o entregador selecionou já foi aceito por outro entregador antes que ele pudesse confirmar. O sistema informa que o pedido não está mais disponível e atualiza a lista de pedidos.
1. Erro ao aceitar pedido: O botão "Aceitar" não responde devido a um problema no sistema. O sistema notifica o entregador para tentar novamente.
1. Falha no status de entrega: O sistema não consegue atualizar o status do pedido para "em entrega". O sistema salva a ação localmente e tenta novamente quando a conexão for restabelecida. O entregador é notificado sobre o problema e pode tentar manualmente ou aguardar o envio automático.

#### Outras atividades:
- O entregador pode visualizar múltiplos pedidos antes de escolher um, e até verificar informações de pedidos anteriores.
- Ele pode aceitar vários pedidos de uma só vez se estiver disponível para múltiplas entregas.
- O entregador pode navegar por outras áreas da plataforma, como relatórios ou perfis de clientes, enquanto aguarda novos pedidos.

#### Estado do Sistema ao Concluir:
- O entregador aceitou o pedido, e o sistema registrou o evento com a data e hora da aceitação, vinculando o pedido ao entregador.
- O status do pedido foi atualizado para "em entrega" e o entregador recebeu a confirmação do pedido, com todos os detalhes necessários para a entrega.
- O sistema armazena a data e hora da aceitação, o ID do entregador, e o status do pedido para fins de relatório e monitoramento.

## Luís Felipe Marques User Story and Use Case
### Estória de Usuário
Estória: Como técnico de TI da FGV, quero poder pedir um café pelo aplicativo para que possa recebê-lo sem sair de minha zona de trabalho.

### Caso de Uso
Ator: Cliente

Descrição: O cliente já possui uma conta na rede social de pedidos de café e está logado no sistema. Ele navega até a página de máquinas de café disponíveis, escolhe a máquina que preferir, e conclui o pedido pagando com moedas virtuais.

#### Fluxo Principal:
1. Acessar Máquinas: O cliente, já logado no sistema, acessa a página de máquinas de café disponíveis.
   1. Caso haja problemas de conexão, o usuário não visualizar a lista de máquinas.
   2. O sistema exibe uma mensagem de erro, sugerindo tentar novamente mais tarde.
2. Visualizar Máquinas: O cliente tem acesso a detalhes e avaliações das máquinas, como se alguma está com algum ingrediente faltando e se outros clientes gostaram do café fornecido por ela (isso é expresso por avaliações de até 5 estrelas).
3. Criar Pedido: O cliente seleciona a máquina que prefere e o pedido que deseja receber.
   1. Caso durante a criação do pedido, um usuário faz o report de que falta ingrediente essencial para o pedido em questão na máquina escolhida. Após clicar em “Enviar Pedido”, o sistema exibe uma mensagem de erro alertando que a máquina não está mais nas condições especificadas.
   2. O cliente volta ao passo 1, onde pode realizar um novo pedido.
4. Confirmar Pedido: O cliente confirma a criação do pedido clicando no botão “Enviar Pedido”, o que faz o valor correspondente ser debitado de sua conta.
   1. Um problema de conexão pode também ocorrer durante o envio do pedido ao sistema.
   2. Nesse caso, uma mensagem de erro é exibida sugerindo ao usuário tentar novamente mais tarde.
5. Atualizar Status: O sistema disponibiliza o pedido para que entregadores possam escolher realizar a entrega do pedido.
6. Visualizar Status: O cliente é direcionado à tela de status do pedido, onde pode checar se já foi aceito ou não.

#### Outras atividades:
- O cliente pode ler os comentários deixados por outros usuários sobre as máquinas de café.
- Ele pode filtrar sua busca por máquinas populares entre amigos, usando o sistema de seguidores da plataforma.
- O cliente pode criar vários pedidos, sem precisar que o anterior seja entregue para isso, de forma que vários entregadores podem atendê-lo.

#### Estado do Sistema ao Concluir:
- O cliente criou seu pedido, que aparece registrado no sistema como “aberto” para ser reivindicado por qualquer entregador.,
- A carteira virtual do cliente está com menos moedas, já que o pedido já está pago.
