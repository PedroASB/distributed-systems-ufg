import socket

HEADER = 64 # 64 bytes
FORMAT = 'utf-8'
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
PORT = 5050
ADDRESS = (SERVER_IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)

def send_message(message):
    message = message.encode(FORMAT)
    message_length = str(len(message)).encode(FORMAT)
    message_length += b' ' * (HEADER - len(message_length))
    client_socket.send(message_length)
    client_socket.send(message)
    

# Main
message = ""
print('[INÍCIO] Conexão com o servidor estabelecida.')
while message != DISCONNECT_MESSAGE:
    message = str(input('Mensagem a ser enviada: '))
    send_message(message)