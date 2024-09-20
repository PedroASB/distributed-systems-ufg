#include "person.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_STR_LEN 256

Pessoa create_person() {
    Pessoa pessoa;
    pessoa.nome = (char *) malloc(MAX_STR_LEN * sizeof(char));
    pessoa.endereco.rua = (char *) malloc(MAX_STR_LEN * sizeof(char));
    pessoa.endereco.bairro = (char *) malloc(MAX_STR_LEN * sizeof(char));
    pessoa.dados_bancarios = (DadosBancarios *) malloc(sizeof(DadosBancarios));
    pessoa.dados_bancarios->banco = (char *) malloc(MAX_STR_LEN * sizeof(char));
    pessoa.dados_bancarios->agencia = (char *) malloc(MAX_STR_LEN * sizeof(char));
    pessoa.dados_bancarios->conta = (char *) malloc(MAX_STR_LEN * sizeof(char));
    return pessoa;
}

void free_person(Pessoa *pessoa) {
    if (pessoa->endereco.rua) free(pessoa->endereco.rua);
    if (pessoa->endereco.bairro) free(pessoa->endereco.bairro);
    if (pessoa->dados_bancarios->banco) free(pessoa->dados_bancarios->banco);
    if (pessoa->dados_bancarios->agencia) free(pessoa->dados_bancarios->agencia);
    if (pessoa->dados_bancarios->conta) free(pessoa->dados_bancarios->conta);
    if (pessoa->dados_bancarios) free(pessoa->dados_bancarios);
}

void print_person(Pessoa pessoa) {
    printf("Nome: %s | Rua: %s | Bairro: %s | Numero: %lu | ", pessoa.nome,\
    pessoa.endereco.rua, pessoa.endereco.bairro, pessoa.endereco.numero);  
    printf("Banco: %s | Agencia: %s | Conta: %s", pessoa.dados_bancarios->banco,\
    pessoa.dados_bancarios->agencia, pessoa.dados_bancarios->conta);
}