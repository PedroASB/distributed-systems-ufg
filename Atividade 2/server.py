import socket
import threading
from struct import unpack
from classes import *

PORT = 5050
HOST_NAME = socket.gethostname()
# SERVER_IP = socket.gethostbyname(HOST_NAME)
SERVER_IP = "0.0.0.0"
ADDRESS = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SIZE_OF_INT = 4
SIZE_OF_LONG = 8
HEADER = 16

def deserialize_string(connection):
    string_lenght = int(unpack('!I', connection.recv(SIZE_OF_INT))[0])
    return connection.recv(string_lenght).decode(FORMAT)

def deserialize(connection):
    for _ in range(0, 3):
        person_field = deserialize_string(connection)
        match person_field:
            case 'nome':
                name = deserialize_string(connection)
            case 'endereco':
                for _ in range(0, 3):
                    address_field = deserialize_string(connection)
                    match address_field:
                        case 'rua':
                            street = deserialize_string(connection)
                        case 'bairro':
                            neighborhood = deserialize_string(connection)
                        case 'numero':
                            number = int(unpack('!I', connection.recv(SIZE_OF_INT))[0])
                        case _:
                            pass
            case 'dados_bancarios':
                for _ in range(0, 3):
                    bank_details_field = deserialize_string(connection)
                    match bank_details_field:
                        case 'banco':
                            bank = deserialize_string(connection)
                        case 'agencia':
                            agency = deserialize_string(connection)
                        case 'conta':
                            account = deserialize_string(connection)
                        case _:
                            pass
            case _:
                pass
    return Person(name, Address(street, neighborhood, number), BankDetails(bank, agency, account))


def handle_client(connection, address):
    print(f'[NOVA CONEXÃO] Cliente {address[0]}:{address[1]} conectado')
    num_people = unpack('!I', connection.recv(SIZE_OF_INT))[0]
    people_list: list[Person] = []

    for _ in range(num_people):
        person = deserialize(connection)
        people_list.append(person)

    print('Pessoas salvas:')
    for person in people_list:
        print(person)
    print('----------------')

    connection.close()
    print(f'[CONEXÃO ENCERRADA] Cliente {address[0]}:{address[1]} desconectado.')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDRESS)
    server_socket.listen() # Esperando novas mensagens
    print(f'[STATUS] Servidor iniciado em {SERVER_IP}:{PORT}.')
    while True:
        connection, address = server_socket.accept() # Mensagem recebida
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f'Conexões ativas: {threading.active_count() - 1}')
        # handle_client(connection, address)


# Main
start_server()
