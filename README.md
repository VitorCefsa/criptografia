# **Documentação - Cliente TCP com Criptografia utilizando Cifra de César e Diffie-Hellman**

## **Visão Geral**

Este cliente TCP utiliza a **Cifra de César** e o **algoritmo de troca de chaves Diffie-Hellman** para criptografar e descriptografar mensagens enviadas e recebidas de um servidor. A aplicação realiza a comunicação através de sockets, criptografando a mensagem antes de enviá-la ao servidor e descriptografando a resposta do servidor antes de exibi-la ao usuário. A cifra de César aplicada no projeto é uma variação híbrida, suportando não apenas o alfabeto, mas também caracteres acentuados e outros símbolos ASCII. O algoritmo Diffie-Hellman é utilizado para gerar uma chave compartilhada segura entre o cliente e o servidor.

## **Objetivo**

- **Cliente TCP**: Estabelece uma conexão com o servidor TCP, envia uma mensagem criptografada e recebe uma resposta criptografada.
- **Criptografia**: Utiliza a cifra de César para garantir a segurança da comunicação entre o cliente e o servidor, tanto para caracteres alfabéticos quanto caracteres especiais e acentuados.
- **Troca de Chaves Segura**: Implementa o algoritmo Diffie-Hellman para gerar uma chave compartilhada segura, utilizada no deslocamento da cifra de César.

---

## **Arquitetura do Sistema**

### **Cliente**
O cliente realiza as seguintes ações principais:
1. Solicita ao usuário a entrada de uma mensagem.
2. Estabelece uma conexão TCP com o servidor.
3. Realiza a troca de chaves Diffie-Hellman para gerar uma chave compartilhada segura.
4. Criptografa a mensagem utilizando a cifra de César e a chave gerada.
5. Envia a mensagem criptografada ao servidor.
6. Recebe a resposta criptografada do servidor.
7. Descriptografa a resposta e exibe para o usuário.
8. Encerra a conexão.

### **Servidor**
Embora não descrito aqui, o servidor é configurado para escutar na mesma porta e endereço IP que o cliente. Ele:
1. Recebe a mensagem criptografada.
2. Realiza a troca de chaves Diffie-Hellman para gerar a mesma chave compartilhada segura.
3. Descriptografa a mensagem recebida.
4. Processa a mensagem (exemplo: converte para maiúsculas).
5. Criptografa novamente a resposta e a envia ao cliente.

---

## **Funções do Código**

### `cifra_cesar(mensagem, deslocamento, criptografar=True)`

**Descrição**: Implementação da cifra de César, responsável por criptografar ou descriptografar uma mensagem.

#### Parâmetros:
- **mensagem** (`str`): A mensagem que será criptografada ou descriptografada.
- **deslocamento** (`int`): O número de posições a ser deslocado cada caractere no alfabeto ou na tabela ASCII.
- **criptografar** (`bool`): Define se a operação será de criptografia (`True`) ou descriptografia (`False`).

#### Retorno:
- **resultado** (`str`): A mensagem resultante após a aplicação do deslocamento. A mensagem pode ser criptografada ou descriptografada, dependendo do valor de `criptografar`.

#### Comportamento:
- A função aplica a cifra de César ao alfabeto (letras minúsculas e maiúsculas).
- Para caracteres acentuados, utiliza uma lista customizada de caracteres acentuados.
- Para outros caracteres (símbolos, números, etc.), aplica o deslocamento na tabela ASCII.

### `diffie_hellman(N, g, private_key)`

**Descrição**: Implementação do algoritmo Diffie-Hellman para troca segura de chaves.

#### Parâmetros:
- **N** (`int`): Número primo utilizado no cálculo da chave.
- **g** (`int`): Gerador utilizado na exponenciação modular.
- **private_key** (`int`): Chave privada do usuário (cliente ou servidor).

#### Retorno:
- **public_key** (`int`): Chave pública gerada pelo usuário.

#### Comportamento:
- O cliente e o servidor geram suas chaves privadas aleatoriamente.
- Cada um calcula sua chave pública e a envia para o outro.
- A partir da chave pública recebida, ambos geram a mesma chave compartilhada de forma segura.

---

## **Fluxo de Execução do Cliente**

1. **Entrada do Usuário**:
   O cliente solicita ao usuário que digite uma mensagem, que será criptografada utilizando a cifra de César.

2. **Troca de Chaves Diffie-Hellman**:
   O cliente e o servidor realizam a troca de chaves para gerar uma chave compartilhada segura.

3. **Criptografia da Mensagem**:
   O cliente criptografa a mensagem utilizando a cifra de César e a chave compartilhada gerada.

4. **Conexão com o Servidor**:
   O cliente estabelece uma conexão com o servidor utilizando um socket TCP, conectando-se ao endereço `serverName = "10.1.70.40"` e à porta `serverPort = 1300`.

5. **Envio da Mensagem Criptografada**:
   A mensagem criptografada é enviada ao servidor por meio do socket TCP. A codificação utilizada para a transmissão é `latin1`, garantindo que todos os caracteres (incluindo especiais) sejam corretamente transmitidos.

6. **Recebimento da Resposta**:
   O cliente aguarda a resposta do servidor, que chega criptografada.

7. **Descriptografia da Resposta**:
   Após receber a resposta criptografada, o cliente descriptografa a mensagem para exibição. A operação de descriptografia é realizada aplicando um deslocamento negativo.

8. **Exibição da Mensagem**:
   A resposta descriptografada é exibida para o usuário, permitindo que ele veja a mensagem processada.

9. **Encerramento da Conexão**:
   O cliente encerra a conexão com o servidor após a comunicação ser concluída.

