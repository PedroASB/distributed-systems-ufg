"""
Este módulo contém os métodos de serialização e desserialização do servidor.
"""

from struct import pack, unpack
from person import *

FORMAT = 'utf-8'
SIZE_OF_INT = 4
SIZE_OF_LONG = 8


def deserialize_int(connection):
    return unpack('!I', connection.recv(SIZE_OF_INT))[0]

def deserialize_long(connection):
    return unpack('!Q', connection.recv(SIZE_OF_LONG))[0]

def deserialize_string(connection):
	string_lenght = deserialize_int(connection)
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
                            number = deserialize_long(connection)
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

def serialize_int(connection, number):
    connection.send(pack('!I', number))

def serialize_long(connection, number):
    connection.send(pack('!Q', number))

def serialize_string(connection, string):
    serialize_int(connection, len(string))
    connection.send(string.encode(FORMAT))

def serialize_person(connection, person):
    serialize_string(connection, "nome")
    serialize_string(connection, person.name)

    serialize_string(connection, "endereco")
    serialize_string(connection, "rua")
    serialize_string(connection, person.address.street)
    serialize_string(connection, "bairro")
    serialize_string(connection, person.address.neighborhood)
    serialize_string(connection, "numero")
    serialize_long(connection, person.address.number)

    serialize_string(connection, "dados_bancarios")
    serialize_string(connection, "banco")
    serialize_string(connection, person.bank_details.bank)
    serialize_string(connection, "agencia")
    serialize_string(connection, person.bank_details.agency)
    serialize_string(connection, "conta")
    serialize_string(connection, person.bank_details.account)
