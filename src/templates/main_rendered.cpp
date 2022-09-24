// This file is to be used as part of a Jinja2 template
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include "headers/indexer.hpp"


#define DEBUG                                               true
#define USER_FILE_PATH "/Users/daniellombardi/Desktop/UFSCar/_current.nosync/ORI/TRAB/Generic-C-BinaryFile-Indexer/src/tester/table"
#define INDEXER_C_TYPE "float"

typedef float indexed_data_type;

typedef struct {
    
        unsigned int id;
    
        unsigned int categoria;
    
        char nome[40];
    
} userStructHead;

typedef struct {
    
        unsigned int id;
    
        unsigned int categoria;
    
        char nome[40];
    
        float __index__preco;
    
} userStruct;

static const size_t SIZE_OF_STRUCT = sizeof(userStruct);
static const size_t SIZE_OF_HEAD = sizeof(userStructHead);

typedef struct {
    float userField;
    unsigned long long offset;
} nodeBlock;
// need to save "__index__preco"

static Indexer<nodeBlock> indexer;

// functions
int index_file(char * path);
int search(char *path, indexed_data_type value);
void *castToType(char *arg);

template<typename... Args>
void log(const char* message, Args... args);
void log(const char* message);
void log(const std::string message);


int main(int argc, char const *argv[]) {

    char op[99];

    while (true) {
        scanf("%s", op);

        if (strcmp(op, "INDEX") == 0) {
            index_file(USER_FILE_PATH);

        } else if (strcmp(op, "SEARCH") == 0) {

            char key[99];
            scanf("%s", key);

            indexed_data_type val = *(indexed_data_type *) castToType(key);
            search(USER_FILE_PATH, val);
        }
    }

    // if (strcmp(argv[1], "INDEX") == 0) {
    //     index_file(USER_FILE_PATH);
    //
    // } else if (strcmp(argv[1], "SEARCH") == 0) {
    //     // indexed_data_type val = (indexed_data_type) castToType(argv[1]);
    //     if (argc < 3)
    //         return 2;
    //
    //     indexed_data_type val = *(indexed_data_type *) castToType(argv[2]);
    //     search(USER_FILE_PATH, val);
    // }

    // Expected args:
    //      - 0 : TABLE_PATH (str) : path of the table to be indexed
    //      - 1 : COMMAND (int) :
    //              - 0 : User is asking to index table
    //              - 1 : User is asking to print index table
    // const std::string TABLE_PATH = std::string(argv[0]);
    // const int COMMAND = atoi(argv[1]);
    //
    // const std::string INDEX_PATH = TABLE_PATH + std::string("_INDEX");

    // ind = Indexer<nodeBlock>();

    return 0;
}


template<typename... Args>
void log(const char* message, Args... args) {
    if (DEBUG)
        printf(message, args...);
}

void log(const char* message) {
    if (DEBUG)
        printf("%s", message);
}

void log(const std::string message) {
    if (DEBUG)
        std::cout << message << '\n';
}

int index_file(char * path) {
    nodeBlock nodeblk;

    FILE *fp = fopen(USER_FILE_PATH, "rb");
    userStruct tmp;
    while (fread(&tmp, sizeof(userStruct), 1, fp)) {
        nodeblk.offset = ftell(fp) - sizeof(userStruct);
        nodeblk.userField = tmp.__index__preco;
        indexer.add(nodeblk);
    }

    fclose(fp);
    return 0;
}

int search(char *path, indexed_data_type value) {
    FILE *fp = fopen(USER_FILE_PATH, "rb");
    userStruct tmp;

    nodeBlock blkTmp;
    blkTmp.userField = value;

    int offset = indexer.seekFromIndex(blkTmp);
    fseek(fp, offset, SEEK_SET);

    while (fread(&tmp, sizeof(userStruct), 1, fp)) {
        
            printf("id: %u\n", tmp.id);
        
            printf("categoria: %u\n", tmp.categoria);
        
            printf("nome: %s\n", tmp.nome);
        
            printf("__index__preco: %f\n", tmp.__index__preco);
        
        break;
    }

    fclose(fp);
}

void *castToType(char *arg) { // vai ser utilizada no search
    indexed_data_type *tmp = (indexed_data_type *) malloc(sizeof(indexed_data_type) * 1);

    if (strcmp(INDEXER_C_TYPE, "float") == 0) {
        *tmp = atof((char *) arg);
    } else if (strcmp(INDEXER_C_TYPE, "double") == 0) {
        *tmp = strtod((char *) arg, NULL);
    } else if (strcmp(INDEXER_C_TYPE, "int") == 0) {
        *tmp = atoi((char *) arg);
    } else if (strcmp(INDEXER_C_TYPE, "unsigned int") == 0) {
       *tmp = atoi((char *) arg);
    // } else if (strcmp(INDEXER_C_TYPE, "long long int") == 0) {
        // *tmp = strtoll((char *) arg, NULL);
    } else {
        *tmp = atoi((char *) arg);
    }

    return tmp;
}