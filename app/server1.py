from socket import * 
import servicesdb

def verificar_status_banco():
  contagem = servicesdb.contagem_registros_db("server1")

  if (contagem > 10):
    return "CHEIO"
  
  return "LIVRE"

if __name__ == "__main__":
  serverPort = 12001
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  print('STATUS SERVIDOR 1: READY')

  while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    sentence_decoded = sentence.decode()

    if (sentence_decoded == "VERIFICAR"):
      status = verificar_status_banco()
      status_db_encoded = status.encode()
      connectionSocket.send(status_db_encoded)
      connectionSocket.close()
    
    else:
      servicesdb.gravar_registro("server1", sentence_decoded)
    # connectionSocket.send(verificacao)
