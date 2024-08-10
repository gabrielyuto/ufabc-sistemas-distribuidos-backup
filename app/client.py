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



from socket import *

def display_menu():
    print("Bem-vindo ao Sistema de Backup")
    print("1. Iniciar Backup")
    print("2. Sair")

def send_file(file_name, host='127.0.0.1', port=12000):
    try:
        # Conectar ao servidor
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))

        file_path = f'../teste/{file_name}'
        
        # Enviar o arquivo
        with open(file_path, 'rb') as f:
            data = f.read(1024)
            while data:
                client_socket.send(data)
                data = f.read(1024)
        
        client_socket.close()
        print('Arquivo enviado com sucesso!')
    except FileNotFoundError:
        print('Arquivo não encontrado. Verifique o caminho e tente novamente.')
    except Exception as e:
        print(f'Erro ao enviar o arquivo: {e}')

if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Escolha uma opção (1 ou 2): ")

        if choice == '1':
            file_name = input("Digite o nome do arquivo a ser enviado: ")
            send_file(file_name)
        elif choice == '2':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
