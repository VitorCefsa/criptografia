# **Documentação - Cliente TCP com Criptografia utilizando Cifra de César**

## **Visão Geral**

Este cliente TCP utiliza a **Cifra de César** para criptografar e descriptografar mensagens enviadas e recebidas de um servidor. A aplicação realiza a comunicação através de sockets, criptografando a mensagem antes de enviá-la ao servidor e descriptografando a resposta do servidor antes de exibi-la ao usuário. A cifra de César aplicada no projeto é uma variação híbrida, suportando não apenas o alfabeto, mas também caracteres acentuados e outros símbolos ASCII.

## **Objetivo**

- **Cliente TCP**: Estabelece uma conexão com o servidor TCP, envia uma mensagem criptografada e recebe uma resposta criptografada.
- **Criptografia**: Utiliza a cifra de César para garantir a segurança da comunicação entre o cliente e o servidor, tanto para caracteres alfabéticos quanto caracteres especiais e acentuados.

---

## **Arquitetura do Sistema**

### **Cliente**
O cliente realiza as seguintes ações principais:
1. Solicita ao usuário a entrada de uma mensagem.
2. Criptografa a mensagem utilizando a cifra de César.
3. Estabelece uma conexão TCP com o servidor.
4. Envia a mensagem criptografada ao servidor.
5. Recebe a resposta criptografada do servidor.
6. Descriptografa a resposta e exibe para o usuário.
7. Encerra a conexão.

### **Servidor**
Embora não descrito aqui, o servidor é configurado para escutar na mesma porta e endereço IP que o cliente. Ele:
1. Recebe a mensagem criptografada.
2. Descriptografa a mensagem recebida.
3. Processa a mensagem (exemplo: converte para maiúsculas).
4. Criptografa novamente a resposta e a envia ao cliente.

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

---

## **Fluxo de Execução do Cliente**

1. **Entrada do Usuário**:
   O cliente solicita ao usuário que digite uma mensagem, que será criptografada utilizando a cifra de César.

2. **Criptografia da Mensagem**:
   O cliente criptografa a mensagem utilizando o deslocamento especificado (por padrão, `deslocamento = 3`).

3. **Conexão com o Servidor**:
   O cliente estabelece uma conexão com o servidor utilizando um socket TCP, conectando-se ao endereço `serverName = "10.1.70.40"` e à porta `serverPort = 1300`.

4. **Envio da Mensagem Criptografada**:
   A mensagem criptografada é enviada ao servidor por meio do socket TCP. A codificação utilizada para a transmissão é `latin1`, garantindo que todos os caracteres (incluindo especiais) sejam corretamente transmitidos.

5. **Recebimento da Resposta**:
   O cliente aguarda a resposta do servidor, que chega criptografada.

6. **Descriptografia da Resposta**:
   Após receber a resposta criptografada, o cliente descriptografa a mensagem para exibição. A operação de descriptografia é realizada aplicando um deslocamento negativo.

7. **Exibição da Mensagem**:
   A resposta descriptografada é exibida para o usuário, permitindo que ele veja a mensagem processada.

8. **Encerramento da Conexão**:
   O cliente encerra a conexão com o servidor após a comunicação ser concluída.

---
