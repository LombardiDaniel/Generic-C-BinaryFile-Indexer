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

struct nodeBlock {
    index_type userField;
    unsigned long long offset;
};

static Indexer<nodeBlock> indexer;

int index_file(char * path) {
   std::ifstream infile;
   infile.open(PATH);

    nodeBlock bufferStruct;

    FILE *fp = fopen(PATH, "rb");
    myStruct tmp;
    // fseek(fp, rrn, SEEK_START);
    // https://www.tutorialspoint.com/c_standard_library/c_function_fseek.htm
    while (fread(&tmp, sizeof(myStruct), 1, fp)) {
        bufferStruct.offset = ftell(fp) - sizeof(myStruct);
        // bufferStruct.userField = tmp.{{ indexer_c_name }};
        bufferStruct.userField = tmp.__index__preco;
        indexer.add(bufferStruct);
    }

    return 0;
}

int search(char *path, index_type value){
    FILE *fp = fopen(PATH, "rb");
    myStruct tmp;

    nodeBlock blkTmp;
    blkTmp.userField = value;

    int offset = indexer.seekFromIndex(blkTmp);
    fseek(fp, offset, SEEK_SET);

    while (fread(&tmp, sizeof(myStruct), 1, fp)) {
        // bufferStruct.userField = tmp.{{ indexer_c_name }};
        // tmp.userField = tmp.__index__preco;
        // aqui ja ta c a struct certa no tmp

        printf("id: %ud", tmp.id);

    }

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
