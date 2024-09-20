#include "serialization.h"
#include <stdlib.h>
#include <string.h>

#define MAX_STR_LEN 256

void serialize_int(int client_socket, uint32_t number) {
	uint32_t number_network_order = htonl(number);
	send(client_socket, &number_network_order, sizeof(number_network_order), 0);
}

void serialize_long(int client_socket, uint64_t number) {
	uint32_t high_part = htonl((uint32_t) (number >> 32));
	uint32_t low_part = htonl((uint32_t) (number & 0xFFFFFFFF));
	send(client_socket, &high_part, sizeof(high_part), 0);
	send(client_socket, &low_part, sizeof(low_part), 0);
}

void serialize_string(int client_socket, const char *string) {;
	uint32_t length = htonl(strlen(string));
	send(client_socket, &length, sizeof(length), 0);
	send(client_socket, string, strlen(string), 0);
}

void serialize_person(int client_socket, Pessoa pessoa) {
	serialize_string(client_socket, "nome");
	serialize_string(client_socket, pessoa.nome);

	serialize_string(client_socket, "endereco");
	serialize_string(client_socket, "rua");
	serialize_string(client_socket, pessoa.endereco.rua);
	serialize_string(client_socket, "bairro");
	serialize_string(client_socket, pessoa.endereco.bairro);
	serialize_string(client_socket, "numero");
	serialize_long(client_socket, pessoa.endereco.numero);

	serialize_string(client_socket, "dados_bancarios");
	serialize_string(client_socket, "banco");
	serialize_string(client_socket, pessoa.dados_bancarios->banco);
	serialize_string(client_socket, "agencia");
	serialize_string(client_socket, pessoa.dados_bancarios->agencia);
	serialize_string(client_socket, "conta");
	serialize_string(client_socket, pessoa.dados_bancarios->conta);
}

int deserialize_int(int client_socket) {
	uint32_t number_network_order;
	recv(client_socket, &number_network_order, sizeof(number_network_order), 0);
	int number = ntohl(number_network_order);
	return number;
}

long deserialize_long(int client_socket) {
    uint32_t high_part, low_part;
    recv(client_socket, &high_part, sizeof(high_part), 0);
    recv(client_socket, &low_part, sizeof(low_part), 0);
    high_part = ntohl(high_part);
    low_part = ntohl(low_part);
    long number = ((long) high_part << 32) | low_part;  
    return number;
}

char *deserialize_string(int client_socket) {
	uint32_t length_network_order;
	recv(client_socket, &length_network_order, sizeof(length_network_order), 0);
	uint32_t length = ntohl(length_network_order);
	char *string = (char*) malloc(length + 1);
	recv(client_socket, string, length, 0);
	string[length] = '\0';
	return string;
}

Pessoa deserialize_person(int client_socket) {
    int i, j;
    char *person_field, *address_field, *bank_details_field;
    Pessoa pessoa = create_person();

    for (i = 0; i < 3; i++) {
        person_field = deserialize_string(client_socket);

        if (!strcmp(person_field, "nome")) {
            pessoa.nome = deserialize_string(client_socket);
        }

        else if (!strcmp(person_field, "endereco")) {
            for (j = 0; j < 3; j++) {
                address_field = deserialize_string(client_socket);
                if (!strcmp(address_field, "rua"))
                    pessoa.endereco.rua = deserialize_string(client_socket);
                else if (!strcmp(address_field, "bairro"))
                    pessoa.endereco.bairro = deserialize_string(client_socket);
                else if (!strcmp(address_field, "numero"))
                    pessoa.endereco.numero = deserialize_long(client_socket);
            }
        }

        else if (!strcmp(person_field, "dados_bancarios")) {
            for (j = 0; j < 3; j++) {
                bank_details_field = deserialize_string(client_socket);
                if (!strcmp(bank_details_field, "banco"))
                    pessoa.dados_bancarios->banco = deserialize_string(client_socket);
                else if (!strcmp(bank_details_field, "agencia"))
                    pessoa.dados_bancarios->agencia = deserialize_string(client_socket);
                else if (!strcmp(bank_details_field, "conta"))
                    pessoa.dados_bancarios->conta = deserialize_string(client_socket);
            }
        }
    }

    return pessoa;
}
