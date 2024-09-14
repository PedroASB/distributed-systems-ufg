import socket
import threading
from struct import pack, unpack
from person import *

PORT = 5050
SERVER_IP = "0.0.0.0"
ADDRESS = (SERVER_IP, PORT)
FORMAT = 'utf-8'
SIZE_OF_INT = 4
SIZE_OF_LONG = 8

def deserialize_string(connection):
	string_lenght = int(unpack('!I', connection.recv(SIZE_OF_INT))[0])
	return connection.recv(string_lenght).decode(FORMAT)

def deserialize_person(connection):
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
							number = int(unpack('!q', connection.recv(SIZE_OF_LONG))[0])
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


def serialize_string(connection, string):
	connection.send(pack('!I', len(string)))
	connection.send(string.encode(FORMAT))


def handle_client(connection, address):
	print(f'[NOVA CONEXÃO] Cliente {address[0]}:{address[1]} conectado.')
	people_list: list[Person] = []

	while True:
		option = unpack('!I', connection.recv(SIZE_OF_INT))[0]
		match option:
			case 1: # Inserir pessoa
				print(f'[COMANDO] {address[0]}:{address[1]}: Inserir pessoa.')
				person = deserialize_person(connection)
				people_list.append(person)
				print(f'Pessoa inserida: {person}.')
				
			case 2: # Listar pessoas
				print(f'[COMANDO] {address[0]}:{address[1]}: Listar pessoas.')
				connection.send(pack('!I', len(people_list)))
				for i, person in enumerate(people_list):
					person_repr = f'Nome: {person.name} | Rua: {person.address.street} | Bairro: ' + \
                                  f'{person.address.neighborhood} | Numero: {person.address.number}' + \
								  f' | Banco: {person.bank_details.bank} | Agencia: ' + \
								  f'{person.bank_details.agency} | Conta: {person.bank_details.account}'
					serialize_string(connection, f'Pessoa {i+1} - ' + person_repr)
					
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
