import socket
import threading
from person import *
from serialization import *

PORT = 5050
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
ADDRESS = (SERVER_IP, PORT)

def handle_client(connection, address):
    print(f'[NOVA CONEXÃO] Cliente {address[0]}:{address[1]} conectado.')
    people_list: list[Person] = []

    while True:
        option = deserialize_int(connection)
        match option:
            case 1: # Inserir pessoa
                print(f'[COMANDO] {address[0]}:{address[1]}: Inserir pessoa.')
                person = deserialize_person(connection)
                people_list.append(person)
                print(f'Pessoa inserida: {person}.')
                
            case 2: # Listar pessoas
                print(f'[COMANDO] {address[0]}:{address[1]}: Listar pessoas.')
                serialize_int(connection, len(people_list))
                for person in people_list:
                    serialize_person(connection, person)
                    
            case 0: # Finalizar
                print(f'[COMANDO] {address[0]}:{address[1]}: Finalizar.')
                break
            
            case _:
                pass

    connection.close()
    print(f'[CONEXÃO ENCERRADA] Cliente {address[0]}:{address[1]} desconectado.')


def start_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(ADDRESS)
	server_socket.listen()
	print(f'[STATUS] Servidor iniciado em {SERVER_IP}:{PORT}.')
	while True:
		connection, address = server_socket.accept()
		thread = threading.Thread(target=handle_client, args=(connection, address))
		thread.start()
		print(f'Conexões ativas: {threading.active_count() - 1}')


# Main
start_server()