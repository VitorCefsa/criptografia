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
 
# Configuração do servidor
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
 
# Permitindo reutilização da porta
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
 
# Bind com "0.0.0.0" para aceitar conexões de qualquer endereço
serverSocket.bind(("0.0.0.0", serverPort))
 
# Iniciando o servidor para escutar
serverSocket.listen(5)
 
print("Servidor TCP iniciado...\nAguardando conexões...")
 
while True:
    try:
        # Aceitar uma nova conexão
        connectionSocket, addr = serverSocket.accept()
        print(f"Conexão estabelecida com {addr}")
 
        # Definir os parâmetros do Diffie-Hellman
        N = 23  # Número primo
        g = 5   # Gerador (base)
 
        # Verificar se N é primo
        if not is_prime(N):
            print(f"O número {N} não é primo. Por favor, digite um número primo.")
            continue
 
        # Gerar a chave privada para o servidor
        private_key = random.randint(2, N-2)
 
        # Calcular a chave pública do servidor
        public_key = diffie_hellman(N, g, private_key)
 
        # Enviar a chave pública do servidor para o cliente
        connectionSocket.send(str(public_key).encode("latin1"))
        print("Chave pública do servidor enviada:", public_key)
 
        # Receber a chave pública do cliente
        received_public_key_cliente = connectionSocket.recv(65000).decode("latin1")
        if not received_public_key_cliente:
            print("Erro: chave pública do cliente não recebida ou inválida.")
            continue
        received_public_key_cliente = int(received_public_key_cliente)
        print(f"Chave pública do cliente recebida: {received_public_key_cliente}")
 
        # Gerar a chave compartilhada
        chave_compartilhada = gerar_chave_compartilhada(received_public_key_cliente, N, private_key)
        print(f"Chave compartilhada gerada: {chave_compartilhada}")
 
        # Receber mensagem criptografada
        received = connectionSocket.recv(65000).decode("latin1")  # "latin1" suporta toda a tabela ASCII
        if not received:
            print("Erro: mensagem não recebida ou inválida.")
            continue
        print("Recebido do cliente (criptografado):", received)
 
        # Descriptografar a mensagem recebida com a chave compartilhada
        mensagem_descriptografada = cifra_cesar(received, chave_compartilhada, criptografar=False)
        print("Mensagem descriptografada (apenas para exibição):", mensagem_descriptografada)
 
        # Processar (convertendo para maiúsculas)
        capitalizedSentence = mensagem_descriptografada.upper()
 
        # Criptografar novamente antes de enviar
        mensagem_criptografada = cifra_cesar(capitalizedSentence, chave_compartilhada, criptografar=True)
 
        # Enviar ao cliente
        connectionSocket.send(mensagem_criptografada.encode("latin1"))
        print("Enviado ao cliente (criptografado):", mensagem_criptografada)
 
        # Fechar a conexão após o envio
        connectionSocket.close()
        print("Conexão encerrada.\nAguardando nova conexão...\n")
    except Exception as e:
        print(f"Erro durante a comunicação: {e}")
