from socket import *
 
# Lista de letras acentuadas para deslocamento manual
letras_acentuadas = "áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ"
 
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
        else:  # Qualquer outro caractere (números, símbolos, emojis, etc.) será deslocado na tabela ASCII
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
 
        # Receber mensagem criptografada
        received = connectionSocket.recv(65000).decode("latin1")  # "latin1" suporta toda a tabela ASCII
        print("Recebido do cliente (criptografado):", received)
 
        # Descriptografar APENAS para exibição
        deslocamento = 3
        mensagem_descriptografada = cifra_cesar(received, deslocamento, criptografar=False)
        print("Mensagem descriptografada (apenas para exibição):", mensagem_descriptografada)
 
        # Processar (convertendo para maiúsculas)
        capitalizedSentence = mensagem_descriptografada.upper()
 
        # Criptografar novamente antes de enviar
        mensagem_criptografada = cifra_cesar(capitalizedSentence, deslocamento, criptografar=True)
 
        # Enviar ao cliente
        connectionSocket.send(mensagem_criptografada.encode("latin1"))
        print("Enviado ao cliente (criptografado):", mensagem_criptografada)
 
        # Fechar a conexão após o envio
        connectionSocket.close()
        print("Conexão encerrada.\nAguardando nova conexão...\n")
    except Exception as e:
        print(f"Erro durante a comunicação: {e}")
 