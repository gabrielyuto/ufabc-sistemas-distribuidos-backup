from socket import *
import random
import os
import struct 

def send_to_server(data, port):
  host = "127.0.0.1"

  client_socket = socket(AF_INET, SOCK_STREAM)
  client_socket.connect((host, port))
  client_socket.send(data)

  modified_sentence = client_socket.recv(1024)
  modified_sentence_decoded = modified_sentence.decode()

  print("From server: ", modified_sentence_decoded)

  client_socket.close()

  return modified_sentence_decoded

def discover_server_free():
  print("Start choose destiny server...")
  
  while True:
    random_port = random.randint(12001, 12002)

    solicitation_type = "Analyze"
    result_server = send_to_server(solicitation_type.encode(), random_port)

    if (result_server == "Free"):
      print("Server choosen: ", random_port)
      return random_port

# def choose_server():
#   print("Start choose destiny server...")
#   choose_server = 0

#   solicitation_type = "Analyze"
#   result_server_1 = send_to_server(solicitation_type.encode(), 12001)
#   result_server_2 = send_to_server(solicitation_type.encode(), 12002)

#   if (result_server_1 == "Free" and result_server_2 == "Free"):
#     random_number = random.randint(12001, 12001)
#     choose_server = random_number
#   elif (result_server_1 == "Free" and result_server_2 == "Full"):
#     choose_server = 12001
#   elif (result_server_1 == "Full" and result_server_2 == "Free"):
#     choose_server = 12002
  
#   print("Server choosen: ", choose_server)

#   return choose_server

if __name__ == "__main__":
  diretorio_arquivo = '../arquivo-manager'
  host = '127.0.0.1'
  port = 12000

  if not os.path.exists(diretorio_arquivo):
    os.makedirs(diretorio_arquivo)
    
  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Manager listening on {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    
    file_path = os.path.join(diretorio_arquivo, 'received_file.txt')
    
    with open(file_path, 'wb') as f:
      while True:
        data = client_socket.recv(1024)
        if not data:
          break

        try:
          file_name = os.path.basename(file_path)
          file_size = os.path.getsize(file_path)
          action_type = "Reply"
          
          header = f"{file_name}:{file_size}:{action_type}"
          header = header.encode('utf-8')
          header_length = struct.pack('!I', len(header))

          server_chosen_port = discover_server_free()          
          
          send_to_server(header_length, server_chosen_port)
          send_to_server(header, server_chosen_port)
          send_to_server(data, server_chosen_port)
          f.write(data)
        
        except Exception as e:
          print(f"Failed to send file: {e}")
        finally:
          client_socket.close()

    client_socket.close()
    print(f'File received and saved to {file_path}')