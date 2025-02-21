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
        else:  # Qualquer outro caractere será deslocado na tabela ASCII
            novo_char = chr((ord(char) + deslocamento) % 256)
 
        resultado += novo_char
 
    return resultado
 
# Configuração do cliente
serverName = "10.1.70.40"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
 
# Entrada do usuário
sentence = input("Digite a mensagem: ")
 
# Escolha do deslocamento para a Cifra de César
deslocamento = 3
 
# Criptografar antes de enviar
sentence_criptografada = cifra_cesar(sentence, deslocamento, criptografar=True)
 
# Enviar mensagem criptografada
clientSocket.send(sentence_criptografada.encode("latin1"))
 
# Receber a resposta criptografada do servidor
modifiedSentence = clientSocket.recv(65000).decode("latin1")
 
# Descriptografar APENAS para exibição
text_descriptografado = cifra_cesar(modifiedSentence, deslocamento, criptografar=False)
 
# Exibir mensagem descriptografada, mas sem alterar o fluxo de envio/recebimento
print("Recebido do servidor (descriptografado para exibição):", text_descriptografado)
 
# Fechar conexão
clientSocket.close()