import random
from socket import *

def exp_modular(base, expoente, modulo):
    resultado = 1
    while expoente > 0:
        if expoente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        expoente //= 2
    return resultado

def gerar_chaves_rsa(bits=4096):
    while True:
        p = random.getrandbits(bits // 2)
        q = random.getrandbits(bits // 2)
        if p != q:
            break
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def criptografar_rsa(mensagem, chave_publica, n):
    return exp_modular(mensagem, chave_publica, n)

def descriptografar_rsa(mensagem, chave_privada, n):
    return exp_modular(mensagem, chave_privada, n)

def cifra_cesar(mensagem, deslocamento, criptografar=True):
    resultado = ""
    deslocamento = deslocamento if criptografar else -deslocamento
    for char in mensagem:
        novo_char = chr((ord(char) + deslocamento) % 256)
        resultado += novo_char
    return resultado

def diffie_hellman(N, g, private_key):
    return exp_modular(g, private_key, N)

def servidor():
    (public_key, n), (private_key, n) = gerar_chaves_rsa()
    serverPort = 1300
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", serverPort))
    serverSocket.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        connectionSocket, addr = serverSocket.accept()
        connectionSocket.send(f"{public_key},{n}".encode())
        chave_publica_cliente, n_cliente = map(int, connectionSocket.recv(65000).decode().split(","))
        private_dh = random.randint(2, 23-2)
        public_dh = diffie_hellman(23, 5, private_dh)
        chave_dh_encriptada = criptografar_rsa(public_dh, chave_publica_cliente, n_cliente)
        connectionSocket.send(str(chave_dh_encriptada).encode())
        received_encrypted_dh = int(connectionSocket.recv(65000).decode())
        received_dh = descriptografar_rsa(received_encrypted_dh, private_key, n)
        chave_compartilhada = exp_modular(received_dh, private_dh, 23)
        received = connectionSocket.recv(65000).decode("latin1")
        mensagem_descriptografada = cifra_cesar(received, chave_compartilhada, criptografar=False)
        resposta = mensagem_descriptografada.upper()
        resposta_criptografada = cifra_cesar(resposta, chave_compartilhada, criptografar=True)
        connectionSocket.send(resposta_criptografada.encode("latin1"))
        connectionSocket.close()

def cliente():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(("10.1.70.40", 1300))
    public_key_servidor, n_servidor = map(int, clientSocket.recv(65000).decode().split(","))
    (public_key, n), (private_key, n) = gerar_chaves_rsa()
    clientSocket.send(f"{public_key},{n}".encode())
    received_encrypted_dh = int(clientSocket.recv(65000).decode())
    received_dh = descriptografar_rsa(received_encrypted_dh, private_key, n)
    private_dh = random.randint(2, 23-2)
    public_dh = diffie_hellman(23, 5, private_dh)
    chave_dh_encriptada = criptografar_rsa(public_dh, public_key_servidor, n_servidor)
    clientSocket.send(str(chave_dh_encriptada).encode())
    chave_compartilhada = exp_modular(received_dh, private_dh, 23)
    mensagem = input("Digite a mensagem: ")
    mensagem_criptografada = cifra_cesar(mensagem, chave_compartilhada, criptografar=True)
    clientSocket.send(mensagem_criptografada.encode("latin1"))
    resposta_criptografada = clientSocket.recv(65000).decode("latin1")
    resposta_descriptografada = cifra_cesar(resposta_criptografada, chave_compartilhada, criptografar=False)
    print("Recebido do servidor (descriptografado):", resposta_descriptografada)
    clientSocket.close()

# Escolha entre servidor() e cliente() para rodar o código apropriado
