#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include "person.h"
#include "serialization.h"

#define PORT 5050
#define SERVER_IP "127.0.1.1"

int main() {
	int status, client_socket, n_people;
	struct sockaddr_in serv_addr;

	if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("\n[ERRO] Falha na criacao do socket.\n");
		return -1;
	}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	if (inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0) {
		printf("\n[ERRO] Endereco invalido ou nao suportado.\n");
		return -1;
	}

	if ((status = connect(client_socket, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) {
		printf("\n[ERRO] Falha na conexao.\n");
		return -1;
	}

	printf("[STATUS] Conexao com o servidor estabelecida.\n\n");

	Pessoa pessoa = create_person();

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
					printf("\nNenhuma pessoa inserida.\n\n");
				else {
                    int i;
                    printf("\nLista de pessoas:\n\n");
                    for (i = 1; i <= n_people; i++) {
                        printf("(Pessoa #%d) ", i);
                        pessoa = deserialize_person(client_socket);
                        print_person(pessoa);
                        printf("\n\n");
                    }
                }
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

    free_person(&pessoa);
	close(client_socket);
	return 0;
}