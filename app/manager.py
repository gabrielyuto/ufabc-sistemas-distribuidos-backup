from socket import *
import random

def send_to_server(data, port):
  host = "127.0.0.1"

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((host, port))
  client_socket.sendall(data)

  data_received = client_socket.recv(1024)

  client_socket.close()

  return data_received

def discover_servers_free():
  print("------------------------------")
  print("Iniciando a escolha da servidor...")
  
  limit_requests = 0
  ports = [12001, 12002, 12003]
  free_ports = []
  tested_ports = []

  while True:
    random_port = random.choice(ports)

    if random_port not in tested_ports:
      tested_ports.append(random_port)
      try:
        solicitation_type = "Analyze"
        data_received = send_to_server(solicitation_type.encode(), random_port)
        
        if (data_received.decode() == "Free"):
          free_ports.append(random_port)

          if (len(free_ports) == 2):
            return free_ports
      
      except Exception as e:
        print()
    
    elif (limit_requests > len(ports) + 2):
      print("Nao ha servidores livres")
      break
    
    limit_requests += 1

if __name__ == "__main__":
  host = '127.0.0.1'
  port = 12000
  
  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Gerenciador escutando em {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(f'Conexao de {addr}')
    
    try:
      free_servers = discover_servers_free()
      choosen_server_port = free_servers[0]
      replica_server_port = free_servers[1]
      
      print(f"Iniciando envio de arquivos ao servidor na porta: {choosen_server_port}")
      header = f"PORTA_REPLICA:{replica_server_port}\n"
      file_with_header = header.encode('utf-8') + data
      
      send_to_server(file_with_header, choosen_server_port)

    except Exception as e:
      print(f"-----------------------------")
    finally:
      client_socket.close()