import socket
from struct import pack

from classes import * # Como este cenário é apenas um exemplo, o cliente está acessando as mesmas 
                      # classes do servidor, isto é, pelo mesmo arquivo 'classes.py'; porém, na 
                      # versão em C, ele não terá acesso a esse arquivo, pois a ideia é que o 
                      # cliente faça sua própria implementação das classes e serialize para o servidor

FORMAT = 'utf-8'
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
PORT = 5050
ADDRESS = (SERVER_IP, PORT)
SIZE_OF_INT = 4
SIZE_OF_LONG = 8
HEADER = 16

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)

def serialize_string(string):
    client_socket.send(pack('!I', len(string)))
    client_socket.send(string.encode(FORMAT))

def serialize(person: Person):
    serialize_string('nome')
    serialize_string(person.name)

    serialize_string('endereco')
    serialize_string('rua')
    serialize_string(person.address.street)
    serialize_string('bairro')
    serialize_string(person.address.neighborhood)
    serialize_string('numero')
    client_socket.send(pack('!I', person.address.number))

    serialize_string('dados_bancarios')
    serialize_string('banco')
    serialize_string(person.bank_details.bank)
    serialize_string('agencia')
    serialize_string(person.bank_details.agency)
    serialize_string('conta')
    serialize_string(person.bank_details.account)
    

# Main
print('[INÍCIO] Conexão com o servidor estabelecida.')

person = Person('Fulano', Address('Rua 15', 'Bairro B', 123), 
                BankDetails('Banco ABC', 'Agencia', '123456'))

num_people = int(input('Quantidade de Pessoas: '))
client_socket.send(pack('!I', num_people))
for _ in range(num_people):
    serialize(person)

client_socket.close()