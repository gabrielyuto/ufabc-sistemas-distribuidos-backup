from socket import * 

def sendToServer(sentence, serverPort):
  serverName = "127.0.0.1"

  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((serverName, serverPort))
  clientSocket.send(sentence)

  modifiedSentence = clientSocket.recv(1024)

  print("From server: ", modifiedSentence.decode())

  clientSocket.close() 

  return modifiedSentence

if __name__ == "__main__":
  serverPort = 12000

  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  print('The server is ready to receive')

  while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)

    # Verifica dados no servidor1
    verificacao = "VERIFICAR"
    resultadoVerificacao = sendToServer(verificacao, 12001)
    # result2 = sendToServer(sentence, 12002)

    if (resultadoVerificacao == "CHEIO"):
      print ("Ta tudo cheio")
      
    print('Server received')
    connectionSocket.close()
    
