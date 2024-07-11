from socket import * 
import servicesdb1

serverPort = 12001

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

# servicesdb1.create_table()

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()

    print('The server is ready to receive: ', capitalizedSentence)
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()