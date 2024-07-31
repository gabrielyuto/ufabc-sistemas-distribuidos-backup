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

def discover_server_free():
  print("------------------------------")
  print("Start choose destiny server...")
  
  list_used_port = []
  limit_requests = 0

  while True:
    ports = [12001, 12002]
    random_port = random.choice(ports)

    if random_port not in list_used_port:
      solicitation_type = "Analyze"
      data_received = send_to_server(solicitation_type.encode(), random_port)
      
      if (data_received.decode() == "Free"):
        print("Server choosen: ", random_port)
        print("------------------------------")
        return random_port
    
      list_used_port.append(random_port)

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
      server_chosen_port = discover_server_free()          
      send_to_server(data, server_chosen_port)
      print(f'File sent to server on port: {server_chosen_port}')
      print("------------------------------")

    except Exception as e:
      print(f"-----------------------------")
    finally:
      client_socket.close()