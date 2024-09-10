import socket
import threading
import os

FORMAT = 'utf-8'
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
PORT = 5050
ADDRESS = (SERVER_IP, PORT)

def handle_client(connection, address):
    print(f'[NOVA CONEXÃO] Cliente {address[0]}:{address[1]} conectado')
    while True:
        option = connection.recv(1024).decode()
        match option:
            case '1':
                image_name = connection.recv(1024).decode()
                image_path = os.path.join("images", image_name)
                image_size = int(connection.recv(1024).decode())

                # Recebe e armazena a imagem
                with open(image_path, 'wb') as file:
                    received_size = 0
                    while received_size < image_size:
                        data = connection.recv(1024)
                        file.write(data)
                        received_size += len(data)
                print(f'Imagem "{image_name}" armazenada com sucesso.')
                connection.send('[SERVIDOR] Imagem salva com sucesso.'.encode())
            case '2':
                images = os.listdir("images")
                if images:
                    connection.send("\n".join(images).encode())
                else:
                    connection.send("Nenhuma imagem armazenada.".encode())
            case '3':
                image_name = connection.recv(1024).decode()
                if image_name in os.listdir("images"):
                    connection.send("TRUE".encode())
                else:
                    connection.send("FALSE".encode())
            case '0':
                break
    connection.close()
    print(f'[CONEXÃO ENCERRADA] Cliente {address[0]}:{address[1]} desconectado.')
    


# Main
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)
server_socket.listen()
print(f'[INÍCIO] Servidor iniciado em {SERVER_IP}:{PORT}.')
while True:
    connection, address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(connection, address))
    thread.start()
    print(f'Conexões ativas: {threading.active_count() - 1}')
