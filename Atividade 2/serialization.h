#ifndef _SERIALIZATION_H
#define _SERIALIZATION_H

#include <arpa/inet.h>
#include "person.h"

void serialize_int(int client_socket, uint32_t number);

void serialize_long(int client_socket, uint64_t number);

void serialize_string(int client_socket, const char *string);

void serialize_person(int client_socket, Pessoa pessoa);

int deserialize_int(int client_socket);

long deserialize_long(int client_socket);

char *deserialize_string(int client_socket);

Pessoa deserialize_person(int client_socket);


#endif // _SERIALIZATION_H