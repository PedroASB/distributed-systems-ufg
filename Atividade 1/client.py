import socket
import os

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
PORT = 5050
ADDRESS = (SERVER_IP, PORT)

def send_image(client_socket, image_name):
    if not os.path.exists(image_name):
        print("\n[ERRO] Arquivo de imagem não encontrado.")
        return
    client_socket.send("1".encode())
    client_socket.send(image_name.encode())
    image_size = os.path.getsize(image_name)
    client_socket.send(str(image_size).encode())
    with open(image_name, "rb") as file:
        while chunk := file.read(1024):
            client_socket.send(chunk)
    confirmation = client_socket.recv(1024).decode()
    print(confirmation)


def list_images(client_socket):
    client_socket.send(f'2'.encode())
    images = client_socket.recv(1024).decode()
    print("\nImagens armazenadas:\n" + images)


def search_image(client_socket, image_name):
    client_socket.send(f'3'.encode())
    client_socket.send(image_name.encode())
    has_image = client_socket.recv(1024).decode()
    if has_image == 'TRUE':
        print(f'\nA imagem "{image_name}" está armazenada.')
    else:
        print(f'\nA imagem "{image_name}" não está armazenada.')


# Main
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)
print('[INÍCIO] Conexão com o servidor estabelecida.')
while True:
    print('\nSelecione um comando:')
    print('1 - Enviar imagem')
    print('2 - Listar imagens salvas')
    print('3 - Pesquisar imagem')
    print('0 - Finalizar')
    command = input()
    match command:
        case '1':
            image_name = str(input("Imagem a ser enviada (ex.: image.jpg): "))
            send_image(client_socket, image_name)
        case '2':
            list_images(client_socket)
        case '3':
            image_name = str(input("Imagem a ser pesquisada (ex.: image.jpg): "))
            search_image(client_socket, image_name)
        case '0':
            client_socket.send(f'0'.encode())
            print('\nConexão encerrada.')
            break
        case _:
            print('[ERRO] Comando inválido.')
client_socket.close()
