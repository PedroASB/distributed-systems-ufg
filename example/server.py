import socket
import threading

HEADER = 64 # 64 bytes
FORMAT = 'utf-8'
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
PORT = 5050
ADDRESS = (SERVER_IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


def handle_client(connection, address):
    print(f'[NOVA CONEXÃO] Cliente {address[0]}:{address[1]} conectado')
    while True:
        message_lenght = connection.recv(HEADER).decode(FORMAT)
        if message_lenght:
            message_lenght = int(message_lenght)
            message = connection.recv(message_lenght).decode(FORMAT)
            if message == DISCONNECT_MESSAGE:
                break
            print(f'Mensagem de {address[0]}:{address[1]}: {message}')
    connection.close()
    print(f'[CONEXÃO ENCERRADA] Cliente {address[0]}:{address[1]} desconectado')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDRESS)
    server_socket.listen() # Esperando novas mensagens
    print(f'[INÍCIO] Servidor iniciado em {SERVER_IP}:{PORT}')
    while True:
        connection, address = server_socket.accept() # Mensagem recebida
        # Iniciar uma nova thread
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        # Uma thread é a que está rodando "start_server", as demais threads são as que estão lidando com os clientes
        print(f'Conexões ativas: {threading.active_count() - 1}')


# Main
start_server()