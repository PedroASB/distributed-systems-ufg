#ifndef _PERSON_H
#define _PERSON_H

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


Pessoa create_person();

void free_person(Pessoa *pessoa);

void print_person(Pessoa pessoa);


#endif // _PERSON_H