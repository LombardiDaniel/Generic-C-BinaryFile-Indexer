#define PATH "original.txt"

#include "headers/indexer.hpp"
#include "headers/utils.hpp"

#include <iostream>
#include <cstring>
#include <fstream>

typedef float index_type;

#define INDEXER_C_TYPE "float"

typedef struct {
    unsigned id;
    unsigned cat;
    char nome[40];
    float __index__preco;
} myStruct;


int size_before_indexed = sizeof(unsigned) + sizeof(unsigned) + 40;
int total_size_of_struct = sizeof(myStruct);
/*

for reg in file:
    read(size_before_valid)
    valid = read()

    read(size_before_indexed - size_before_valid)
    index_val = read()

    read(total_size_of_struct - size_before_indexed)

*/

Indexer (indexer);

struct nodeBlock {
    index_type userField;
    unsigned long long rrn;
};

int index_file(char * path) {
   std::ifstream infile;
   infile.open("PATH");
   int current = size_before_indexed;

    struct nodeBlock bufferStruct;

    while (!EOF) {

        infile.seekg(current, std::ios::beg);

        current = size_before_indexed + total_size_of_struct;
        infile.read(bufferStruct.userField, sizeof(index_type));
        bufferStruct.rrn = (int)current / total_size_of_struct;

        indexer.add(bufferStruct);
    }
    FILE *fp = fopen(PATH, "rb");
    myStruct tmp;
    index_type value;
    fread(&tmp, size_before_indexed, 1, fp);
    while (fread(&value, sizeof(index_type), 1, fp)) {
        bufferStruct.rrn = ftell(fp);
        bufferStruct.userField = value;
    }

    infile.close();
    return 0;
}

int search(char * path, index_type value){
    int rrn = indexer.seekFromIndex(value);
    std::ifstream infile;
    infile.open("PATH");
    infile.seekg(total_size_of_struct * rrn, std::ios::beg);
}

void *castToType(void *arg);

int main(int argc, char const* argv[]) {
    if (argc < 2) {
        // Mensagem de erro aí
        return 1;
    }

    char *op;
    memcpy(op, argv[1], 5);

    if (strcmp(utils::toUpperCase(op), "INDEX") == 0) {
        index_file(PATH);

    // } else if(strcmp(utils::toUpperCase(op), "SEARCH") == 0) {
    //     search(PATH, (index_type)argv[1]);
    }

}


void *castToType(void *arg) { // vai ser utilizada no search
    if (strcmp(INDEXER_C_TYPE, "float") == 0) {
        float *tmp = (float *) malloc(sizeof(float) * 1);
        *tmp = atof((char *) arg);
        return tmp;
    }
}
/*
(valor do CAMPO_ESPECIFICADO_DO_USUARIO; rrn do registro)

struct nos nós da árvore: (price, RRN)
->
adicionar os rrns da busca numa lista [rrn0, rrn1, rrn2, ...]
->
buscar pelos rrns no arquivo original
->
printar os structs
*/
