from socket import * 
import servicesdb

def verify_db_status():
  limit_table = 2
  count = servicesdb.count_register("server1")
  print("------------------------------")
  print("Limit of server 1: ", limit_table)
  print("Total count in table: ", count)

  if (count >= limit_table):
    print("Server 1 is Full")
    return "Full"
  
  print("Server 1 is Free")
  return "Free"

def reply(port):
  host = "127.0.0.1"
  port = 12002

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((host, port))
  client_socket.send(data)

  modified_sentence = client_socket.recv(1024)
  modified_sentence_decoded = modified_sentence.decode()

  print("From server: ", modified_sentence_decoded)

  client_socket.close()

  return modified_sentence_decoded

if __name__ == "__main__":
  host = "127.0.0.1"
  port = 12001

  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Server 1 listening on {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(f'Connection from {addr}')
  
    if (data_decoded == "Analyze"):
      status = verify_db_status()
      status_db_encoded = status.encode()
      client_socket.send(status_db_encoded)
      client_socket.close()
    
    else:
      servicesdb.save("server1", data)
      #reply(data)
    
    client_socket.close()
  
