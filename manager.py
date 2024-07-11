from socket import * 

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

def sendToServer(sentence):
    serverName = "127.0.0.1"
    serverPort = 12001

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(sentence)

    modifiedSentence = clientSocket.recv(1024)

    print("From server: ", modifiedSentence.decode())

    clientSocket.close()   

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)

    sendToServer(sentence)

    print('Server received')
    connectionSocket.close()