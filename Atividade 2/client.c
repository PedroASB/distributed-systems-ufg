#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_STR_LEN 256
#define PORT 5050

typedef struct endereco {
	char *rua;
	char *bairro;
	long numero;
} Endereco;

typedef struct dadosBancarios {
	char *banco;
	char *agencia;
	char *conta;
} DadosBancarios;

typedef struct pessoa {
	char *nome;
	Endereco endereco;
	DadosBancarios *dados_bancarios;
} Pessoa;


void serialize_string(int client_socket, const char *string) {;
	uint32_t length = htonl(strlen(string));
	send(client_socket, &length, sizeof(length), 0);
	send(client_socket, string, strlen(string), 0);
}

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

char * deserialize_string(int client_socket) {
	uint32_t length_network_order;
	recv(client_socket, &length_network_order, sizeof(length_network_order), 0);
	uint32_t length = ntohl(length_network_order);
	char *string = (char*) malloc(length + 1);
	recv(client_socket, string, length, 0);
	string[length] = '\0';
	return string;
}

int main(int argc, char const* argv[]) {
	int status, valread, client_socket, n_people;
	char * person_repr;
	struct sockaddr_in serv_addr;

	if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("\n[ERRO] Falha na criacao do socket.\n");
		return -1;
	}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
		printf("\n[ERRO] Endereco invalido ou nao suportado.\n");
		return -1;
	}

	if ((status = connect(client_socket, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) {
		printf("\n[ERRO] Falha na conexao.\n");
		return -1;
	}

	printf("[STATUS] Conexao com o servidor estabelecida.\n");

	Pessoa pessoa;
	pessoa.nome = (char *) malloc(MAX_STR_LEN * sizeof(char));
	pessoa.endereco.rua = (char *) malloc(MAX_STR_LEN * sizeof(char));
	pessoa.endereco.bairro = (char *) malloc(MAX_STR_LEN * sizeof(char));
	pessoa.dados_bancarios = (DadosBancarios *) malloc(sizeof(DadosBancarios));
	pessoa.dados_bancarios->banco = (char *) malloc(MAX_STR_LEN * sizeof(char));
	pessoa.dados_bancarios->agencia = (char *) malloc(MAX_STR_LEN * sizeof(char));
	pessoa.dados_bancarios->conta = (char *) malloc(MAX_STR_LEN * sizeof(char));

	int option = 1;
	while (option) {
		printf("Selecione uma opcao:\n");
		printf("1 - Inserir pessoa\n");
		printf("2 - Listar pessoas\n");
		printf("0 - Finalizar\n");
		printf(">> ");
		scanf("%d%*c", &option);
		switch (option) {
			case 1: // Inserir pessoa
				printf("\nInsira os dados da pessoa:\n");
				printf("Nome: ");
				scanf("%[^\n]%*c", pessoa.nome);
				printf("Rua: ");
				scanf("%[^\n]%*c", pessoa.endereco.rua);
				printf("Bairro: ");
				scanf("%[^\n]%*c", pessoa.endereco.bairro);
				printf("Numero: ");
				scanf("%ld%*c", &pessoa.endereco.numero);
				printf("Banco: ");
				scanf("%[^\n]%*c", pessoa.dados_bancarios->banco);
				printf("Agencia: ");
				scanf("%[^\n]%*c", pessoa.dados_bancarios->agencia);
				printf("Conta: ");
				scanf("%[^\n]%*c", pessoa.dados_bancarios->conta);
				printf("\n");
				serialize_int(client_socket, 1);
				serialize_person(client_socket, pessoa);
				break;

			case 2: // Listar pessoas
				serialize_int(client_socket, 2);
				n_people = deserialize_int(client_socket);
				if (n_people == 0)
					printf("\nNenhuma pessoa inserida.\n");
				else
					printf("\nLista de pessoas:\n");
				while (n_people--) {
					person_repr = deserialize_string(client_socket);
					printf("%s\n", person_repr);
				}
				printf("\n");
				break;

			case 0: // Finalizar
				serialize_int(client_socket, 0);
				option = 0;
				break;

			default: // Opção inválida
				printf("\n[ERRO] Opcao invalida.\n\n");
				break;
		}
	}


	printf("\n[STATUS] Conexao com o servidor encerrada.\n");

	if (pessoa.endereco.rua) free(pessoa.endereco.rua);
	if (pessoa.endereco.bairro) free(pessoa.endereco.bairro);
	if (pessoa.dados_bancarios->banco) free(pessoa.dados_bancarios->banco);
	if (pessoa.dados_bancarios->agencia) free(pessoa.dados_bancarios->agencia);
	if (pessoa.dados_bancarios->conta) free(pessoa.dados_bancarios->conta);
	if (pessoa.dados_bancarios) free(pessoa.dados_bancarios);

	close(client_socket);
	return 0;
}
