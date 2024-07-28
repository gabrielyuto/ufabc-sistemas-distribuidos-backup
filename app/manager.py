from socket import *
import random 

def sendToServer(sentence, serverPort):
  sentence_encoded = sentence.encode()
  server_name = "127.0.0.1"

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((server_name, serverPort))
  client_socket.send(sentence_encoded)

  modified_sentence = client_socket.recv(1024)
  modified_sentence_decoded = modified_sentence.decode()

  print("From server: ", modified_sentence_decoded)

  client_socket.close()

  return modified_sentence_decoded

def escolher_servidor():
  print("INICIANDO A ESCOLHA DO SERVIDOR")
  servidor_escolhido = 0

  tipo_solicitacao = "VERIFICAR"
  resultado_servidor_1 = sendToServer(tipo_solicitacao, 12001)
  # resultado_servidor_2 = sendToServer(sentence, 12002)
  resultado_servidor_2 = "CHEIO"

  if (resultado_servidor_1 == "LIVRE" and resultado_servidor_2 == "LIVRE"):
    #usar qualquer servidor
    numero_aleatorio = random.randint(1, 2)
    servidor_escolhido = numero_aleatorio
  elif (resultado_servidor_1 == "LIVRE" and resultado_servidor_2 == "CHEIO"):
    # Usar servidor 1
    servidor_escolhido = 1
  elif (resultado_servidor_1 == "CHEIO" and resultado_servidor_2 == "LIVRE"):
    # Usar servidor 2
    servidor_escolhido = 2
  
  print("SERVIDOR ESCOLHIDO: ", servidor_escolhido)

  return servidor_escolhido

def enviar_arquivo_ao_servidor(sentence, servidor):
  server_port = 0

  print("SERVIDOR:", servidor)
  if (servidor == 1):
    server_port = 12001
  elif (servidor == 2):
    server_port = 12002

  print("PORTA ", server_port)

  sendToServer(sentence, server_port)

if __name__ == "__main__":
  serverPort = 12000

  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  print('STATUS GERENCIADOR: READY')

  while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    sentence_decoded = sentence.decode()

    servidor = escolher_servidor()

    enviar_arquivo_ao_servidor(sentence_decoded, servidor)

    print('Server received')

    connectionSocket.send("OK!".encode())
    connectionSocket.close()
    
