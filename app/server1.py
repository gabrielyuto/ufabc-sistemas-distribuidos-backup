from socket import * 
import servicesdb

def connection_db():
  DB_HOST = "127.0.0.1"
  DB_NAME = "database1"
  DB_USER = "user1"
  DB_PASS = "password1"

  return servicesdb.get_db_connection(DB_HOST, DB_NAME, DB_USER, DB_PASS)

if __name__ == "__main__":
  serverPort = 12001
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  print('The server 1 is ready to receive')

  while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    
    if (sentence.upper() == "VERIFICAR"):
      verificacao = "CHEIO"
      connectionSocket.send(verificacao)

    print('RESPONDENDO: ', verificacao)

    # connectionSocket.send(verificacao)
    connectionSocket.close()
