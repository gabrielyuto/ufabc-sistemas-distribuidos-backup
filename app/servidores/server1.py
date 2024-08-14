from socket import *
import servicesdb

def verify_db_status():
  limit_table = 2
  count = servicesdb.count_register("server1")
  print("--------- VERIFICACAO DO SERVIDOR PELO MANAGER ---------")
  print("Limite do servidor 1: ", limit_table)
  print("Total de registros no servidor 1: ", count)

  if (count >= limit_table):
    print("Servidor 1 cheio")
    return "Full"
  
  print("Servidor 1 livre")
  print("--------------------------------------------------------")
  return "Free"

def send_to_replica(data, replica_port):
    host = "127.0.0.1"
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, replica_port))
        client_socket.send(data)
        client_socket.close()
    except Exception as e:
        print(f"Erro ao enviar os dados a replica: {e}")


if __name__ == "__main__":
  host = "127.0.0.1"
  port = 12001

  server_socket = socket(AF_INET, SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)
  print(f'Servidor 1 escutando em {host}:{port}')

  while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data_decoded = data.decode()
    print(f'Conexao de {addr}')
  
    if (data_decoded == "Analyze"):
      status = verify_db_status()
      status_db_encoded = status.encode()
      client_socket.send(status_db_encoded)

    else:
      # Separar o cabeçalho do conteúdo do arquivo
      dados_separados = data.split(b'\n', 1)
      cabecalho = dados_separados[0].decode('utf-8')

      if (cabecalho.startswith("PORTA")):
        numero_porta_replica = int(cabecalho.split(':')[1])
        conteudo_arquivo = dados_separados[1]

        servicesdb.save("server1", conteudo_arquivo)

        header = f"REPLICA\n"
        file_with_header = header.encode('utf-8') + conteudo_arquivo
        send_to_replica(file_with_header, numero_porta_replica)
      
      elif (cabecalho.startswith("REPLICA")):
        conteudo_arquivo = dados_separados[1]
        servicesdb.save("server1", conteudo_arquivo)
    
    client_socket.close()
  
