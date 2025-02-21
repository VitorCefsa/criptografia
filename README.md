# Sistema Cliente-Servidor com Cifra de César e Comunicação TCP

Este projeto implementa um sistema de comunicação cliente-servidor utilizando o protocolo TCP, onde as mensagens enviadas e recebidas entre o cliente e o servidor são criptografadas usando a **Cifra de César**. O código oferece suporte a caracteres acentuados e outros caracteres ASCII, garantindo que a comunicação seja robusta e funcional para diferentes tipos de entrada.

## Descrição

O sistema é composto por duas partes principais:

1. **Cliente**:
   - O cliente envia uma mensagem para o servidor, a qual é criptografada usando a cifra de César.
   - Após receber a resposta do servidor, o cliente descriptografa a mensagem e a exibe para o usuário.

2. **Servidor**:
   - O servidor recebe uma mensagem criptografada do cliente.
   - Descriptografa a mensagem para processamento, converte para maiúsculas e a retorna ao cliente de forma criptografada.

## Funcionamento

- **Cifra de César**: A cifra de César desloca os caracteres da mensagem por um número fixo de posições no alfabeto ou na tabela ASCII.
- **Suporte a Caracteres Especiais**: A cifra é adaptada para lidar corretamente com letras acentuadas e outros caracteres especiais.
- **Protocolo TCP**: A comunicação é realizada por meio de sockets TCP, com o servidor ouvindo em uma porta específica e o cliente se conectando para enviar e receber dados.

## Como Executar

### 1. Executar o Servidor

O servidor escuta na porta `1300` e aguarda conexões de clientes. O código do servidor deve ser executado primeiro para que ele fique pronto para receber conexões.

Execute o servidor com o seguinte comando:

```bash
python servidor.py
