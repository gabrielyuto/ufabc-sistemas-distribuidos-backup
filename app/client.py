from socket import *

if __name__ == "__main__":
  host = "127.0.0.1"
  port = 12000
  file_path = '../teste/arquivo.txt'

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((host, port))
  
  with open(file_path, 'rb') as f:
    data = f.read(1024)
    while data:
      client_socket.send(data)
      data = f.read(1024)

  client_socket.close()
  print('File sent')
