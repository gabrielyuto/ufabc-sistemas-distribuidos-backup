from socket import * 
import servicesdb

def verify_db_status():
  limit_table = 10
  count = servicesdb.count_register("server2")
  print("------------------------------")
  print("Limit of server 1: ", limit_table)
  print("Total count in table: ", count)

  if (count >= limit_table):
    print("Server 2 is Full")
    return "Full"
  
  print("Server 2 is Free")
  return "Free"

def send_to_replica(data, replica_port):
    host = "127.0.0.1"
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, replica_port))
        client_socket.send(data)
        client_socket.close()
    except Exception as e:
        print(f"Error sending data to replica: {e}")


if __name__ == "__main__":
  host = "127.0.0.1"
  port = 12002

  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Server 2 listening on {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(f'Connection from {addr}')
  
    if (data_decoded == "Analyze"):
      status = verify_db_status()
      status_db_encoded = status.encode()
      client_socket.send(status_db_encoded)

      if status == "Free":
        servicesdb.save( "server2", data)

        if data_decoded.startswith("Replica:"):
          replica_port = int(data_decoded.split(":")[1])

          client_socket.close()

          print("PORTA:")
          print(replica_port)

          send_to_replica(data, replica_port)

      else:
        print("Server is Full")    
    
    client_socket.close()