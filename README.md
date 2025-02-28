# **Documentação - Cliente TCP com Criptografia utilizando Cifra de César, Diffie-Hellman e RSA**

## **Visão Geral**

Este cliente TCP utiliza a **Cifra de César**, o **algoritmo de troca de chaves Diffie-Hellman** e **criptografia assimétrica RSA** para criptografar e descriptografar mensagens enviadas e recebidas de um servidor. A comunicação ocorre através de sockets, com camadas adicionais de segurança. A cifra de César protege os dados transmitidos, enquanto Diffie-Hellman gera uma chave compartilhada segura. O **RSA com chaves assimétricas de 4096 bits** é utilizado para criptografar a chave compartilhada antes de ser transmitida.

## **Objetivo**

- **Cliente TCP**: Estabelece uma conexão com o servidor TCP, envia uma mensagem criptografada e recebe uma resposta criptografada.
- **Criptografia**: Utiliza a cifra de César para garantir a segurança da comunicação entre o cliente e o servidor, tanto para caracteres alfabéticos quanto caracteres especiais e acentuados.
- **Troca de Chaves Segura**: Implementa o algoritmo Diffie-Hellman para gerar uma chave compartilhada segura.
- **Criptografia Assimétrica**: Usa RSA para criptografar a chave compartilhada antes de enviá-la ao outro lado da comunicação.

---

## **Arquitetura do Sistema**

### **Cliente**
O cliente realiza as seguintes ações principais:
1. Solicita ao usuário a entrada de uma mensagem.
2. Estabelece uma conexão TCP com o servidor.
3. **Gera um par de chaves RSA (privada e pública) de 4096 bits.**
4. **Envia sua chave pública RSA para o servidor.**
5. **Recebe a chave pública RSA do servidor.**
6. **Gera uma chave compartilhada usando Diffie-Hellman.**
7. **Criptografa a chave compartilhada com RSA antes de enviá-la ao servidor.**
8. **Recebe a chave compartilhada do servidor (criptografada com RSA) e a descriptografa.**
9. Criptografa a mensagem utilizando a cifra de César e a chave compartilhada.
10. Envia a mensagem criptografada ao servidor.
11. Recebe a resposta criptografada do servidor.
12. Descriptografa a resposta e exibe para o usuário.
13. Encerra a conexão.

### **Servidor**
Embora não descrito aqui, o servidor é configurado para escutar na mesma porta e endereço IP que o cliente. Ele:
1. **Gera um par de chaves RSA (privada e pública) de 4096 bits.**
2. **Troca as chaves públicas RSA com o cliente.**
3. **Gera uma chave compartilhada Diffie-Hellman.**
4. **Recebe a chave compartilhada criptografada do cliente e a descriptografa usando RSA.**
5. **Envia a chave compartilhada criptografada para o cliente, que a descriptografa com RSA.**
6. Descriptografa a mensagem recebida.
7. Processa a mensagem (exemplo: converte para maiúsculas).
8. Criptografa novamente a resposta e a envia ao cliente.

---

## **Funções do Código**

### `cifra_cesar(mensagem, deslocamento, criptografar=True)`

**Descrição**: Implementação da cifra de César, responsável por criptografar ou descriptografar uma mensagem.

### `diffie_hellman(N, g, private_key)`

**Descrição**: Implementação do algoritmo Diffie-Hellman para troca segura de chaves.

### `gerar_par_rsa()`

**Descrição**: Gera um par de chaves RSA (privada e pública) de 4096 bits para criptografia assimétrica.

### `criptografar_rsa(mensagem, chave_publica)`

**Descrição**: Utiliza a chave pública RSA para criptografar mensagens (como a chave compartilhada Diffie-Hellman).

### `descriptografar_rsa(mensagem, chave_privada)`

**Descrição**: Utiliza a chave privada RSA para descriptografar mensagens recebidas.

---

## **Fluxo de Execução do Cliente**

1. **Entrada do Usuário**:
   O cliente solicita ao usuário que digite uma mensagem, que será criptografada utilizando a cifra de César.

2. **Geração das Chaves RSA**:
   Cliente e servidor geram pares de chaves RSA de 4096 bits.

3. **Troca das Chaves Públicas RSA**:
   O cliente envia sua chave pública RSA para o servidor e recebe a chave pública RSA do servidor.

4. **Troca de Chaves Diffie-Hellman**:
   O cliente e o servidor realizam a troca de chaves Diffie-Hellman para gerar uma chave compartilhada segura.

5. **Criptografia da Chave Compartilhada com RSA**:
   A chave compartilhada gerada é criptografada usando a chave pública RSA do destinatário.

6. **Envio e Recebimento da Chave Compartilhada**:
   Cliente e servidor enviam a chave compartilhada criptografada um para o outro e a descriptografam com RSA.

7. **Criptografia da Mensagem**:
   O cliente criptografa a mensagem utilizando a cifra de César e a chave compartilhada gerada.

8. **Conexão com o Servidor**:
   O cliente estabelece uma conexão com o servidor utilizando um socket TCP.

9. **Envio da Mensagem Criptografada**:
   A mensagem criptografada é enviada ao servidor por meio do socket TCP.

10. **Recebimento da Resposta**:
   O cliente aguarda a resposta do servidor, que chega criptografada.

11. **Descriptografia da Resposta**:
   Após receber a resposta criptografada, o cliente descriptografa a mensagem.

12. **Exibição da Mensagem**:
   A resposta descriptografada é exibida para o usuário.

13. **Encerramento da Conexão**:
   O cliente encerra a conexão com o servidor após a comunicação ser concluída.

