from socket import *
import random

def send_to_server(data, port):
  host = "127.0.0.1"

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((host, port))
  client_socket.send(data)

  data_received = client_socket.recv(1024)

  client_socket.close()

  return data_received

def discover_server_free(used_ports):
  print("------------------------------")
  print("Start choose destiny server...")
  
  limit_requests = 0
  ports = [12001, 12002]

  while True:
    random_port = random.choice(ports)

    if random_port not in used_ports:
      solicitation_type = "Analyze"
      data_received = send_to_server(solicitation_type.encode(), random_port)
      
      if (data_received.decode() == "Free"):
        print("Server choosen: ", random_port)
        print("------------------------------")
        return random_port
    
      used_ports.append(random_port)

    elif (limit_requests > len(ports) + 2):
      print("Theres no free servers")
      break

    limit_requests += 1

if __name__ == "__main__":
  host = '127.0.0.1'
  port = 12000
  
  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Manager listening on {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(f'Connection from {addr}')

    try:
      used_ports = []
      primary_port = discover_server_free(used_ports)
      if primary_port:
        used_ports.append(primary_port)
        replica_port = discover_server_free(used_ports)
        if replica_port:
          print(f'Primary server chosen: {primary_port}')
          print(f'Replica server chosen: {replica_port}')

          # Send data to primary server
          send_to_server(data, primary_port)
          print(f'File sent to primary server on port: {primary_port}')
                    
          # Notify primary server to send data to replica
          data_to_send = f"Replica:{replica_port}".encode()
          send_to_server(data_to_send, primary_port)
        else:
          print("No available replica server.")
      else:
        print("No available primary server.")    

    except Exception as e:
      print(f"-----------------------------")
    finally:
      client_socket.close()