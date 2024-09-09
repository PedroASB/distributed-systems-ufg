import socket
import threading

PORT = 5050
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME) # "192.168.56.1"
ADDRESS = (SERVER_IP, PORT)
HEADER = 64 # 64 bytes
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

def handle_client(connection, address):
    print(f'Nova conexão: {address} conectado.')
    while True:
        message_lenght = int(connection.recv(HEADER).decode(FORMAT))
        message = connection.recv(message_lenght).decode(FORMAT)
        if message == DISCONNECT_MSG:
            break
        print(f'Mensagem de [{address}]: {message}')
    connection.close()


def start_server():
    server_socket.listen() # Esperando novas mensagens
    print(f'Servidor iniciado em {SERVER_IP}')
    while True:
        connection, address = server_socket.accept() # Mensagem recebida
        # Iniciar uma nova thread
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        # Uma thread é a que está rodando "start_server"
        # As demais threads são as que estão rodando os clientes
        print(f'Conexões ativas: {threading.activeCount() - 1}')
        print(f'Conexões ativas: {threading.active_count() - 1}')


# Main
start_server()