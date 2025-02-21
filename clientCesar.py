import random
from socket import *

# Lista de letras acentuadas para deslocamento manual
letras_acentuadas = "áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ"

# Função para verificar se um número é primo (simplificado para uso no Diffie-Hellman)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Função de troca de chaves Diffie-Hellman
def diffie_hellman(N, g, private_key):
    # Calculando a chave pública a partir da chave privada
    public_key = pow(g, private_key, N)
    return public_key

# Função para gerar a chave compartilhada usando Diffie-Hellman
def gerar_chave_compartilhada(recebida_chave_publica, N, private_key):
    chave_compartilhada = pow(recebida_chave_publica, private_key, N)
    return chave_compartilhada

# Função para cifra de César com suporte híbrido: alfabeto + ASCII
def cifra_cesar(mensagem, deslocamento, criptografar=True):
    resultado = ""
    deslocamento = deslocamento if criptografar else -deslocamento

    for char in mensagem:
        if 'a' <= char <= 'z':  # Letras minúsculas
            novo_char = chr(((ord(char) - ord('a') + deslocamento) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':  # Letras maiúsculas
            novo_char = chr(((ord(char) - ord('A') + deslocamento) % 26) + ord('A'))
        elif char in letras_acentuadas:  # Letras acentuadas
            indice = letras_acentuadas.index(char)
            novo_char = letras_acentuadas[(indice + deslocamento) % len(letras_acentuadas)]
        else:  # Qualquer outro caractere será deslocado na tabela ASCII
            novo_char = chr((ord(char) + deslocamento) % 256)

        resultado += novo_char

    return resultado

# Configuração do cliente
serverName = "10.1.70.40"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Definir os parâmetros do Diffie-Hellman
N = 23  # Número primo
g = 5   # Gerador (base)

# Verificar se N é primo
if not is_prime(N):
    print(f"O número {N} não é primo. Por favor, digite um número primo.")
else:
    # Gerar a chave privada para o cliente
    private_key_cliente = random.randint(2, N-2)

    # Calcular a chave pública do cliente
    public_key_cliente = diffie_hellman(N, g, private_key_cliente)

    # Enviar a chave pública do cliente para o servidor
    clientSocket.send(str(public_key_cliente).encode("latin1"))
    print("Chave pública do cliente enviada:", public_key_cliente)

    # Receber a chave pública do servidor
    received_public_key_servidor = clientSocket.recv(65000).decode("latin1")
    if not received_public_key_servidor:
        print("Erro: chave pública do servidor não recebida ou inválida.")
    else:
        received_public_key_servidor = int(received_public_key_servidor)
        print(f"Chave pública do servidor recebida: {received_public_key_servidor}")

        # Gerar a chave compartilhada
        chave_compartilhada = gerar_chave_compartilhada(received_public_key_servidor, N, private_key_cliente)
        print(f"Chave compartilhada gerada: {chave_compartilhada}")

        # Entrada do usuário
        sentence = input("Digite a mensagem: ")

        # Criptografar antes de enviar
        sentence_criptografada = cifra_cesar(sentence, chave_compartilhada, criptografar=True)

        # Enviar mensagem criptografada
        clientSocket.send(sentence_criptografada.encode("latin1"))

        # Receber a resposta criptografada do servidor
        modifiedSentence = clientSocket.recv(65000).decode("latin1")

        # Descriptografar APENAS para exibição
        text_descriptografado = cifra_cesar(modifiedSentence, chave_compartilhada, criptografar=False)

        # Exibir mensagem descriptografada
        print("Recebido do servidor (descriptografado para exibição):", text_descriptografado)

        # Fechar conexão
        clientSocket.close()
