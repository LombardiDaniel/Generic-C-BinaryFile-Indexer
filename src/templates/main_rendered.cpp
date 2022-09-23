// This file is to be used as part of a Jinja2 template
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include "headers/indexer.hpp"


#define DEBUG                                               true
#define USER_FILE_PATH "/Users/daniellombardi/Desktop/UFSCar/_current.nosync/ORI/NPs/2/table"
#define INDEXER_C_TYPE "float"

typedef float indexed_data_type;

typedef struct {
    
        unsigned int id;
    
        unsigned int categoria;
    
        char myCustomClass[40];
    
} userStructHead;

typedef struct {
    
        unsigned int id;
    
        unsigned int categoria;
    
        char myCustomClass[40];
    
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
void *castToType(void *arg);

template<typename... Args>
void log(const char* message, Args... args);
void log(const char* message);
void log(const std::string message);


int main(int argc, char const *argv[]) {
    if (argc < 2) {
        // Mensagem de erro aí
        return 1;
    }

    char *op;
    memcpy(op, argv[1], 5);

    if (strcmp(op, "INDEX") == 0) {
        index_file(USER_FILE_PATH);

    // } else if(strcmp(utils::toUpperCase(op), "SEARCH") == 0) {
    //     search(PATH, (index_type)argv[1]);
    }

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
        break;
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
        
            printf("myCustomClass: %s\n", tmp.myCustomClass);
        
            printf("__index__preco: %f\n", tmp.__index__preco);
        
        break;
    }

    fclose(fp);
}

void *castToType(void *arg) { // vai ser utilizada no search
    if (strcmp(INDEXER_C_TYPE, "float") == 0) {
        float *tmp = (float *) malloc(sizeof(float) * 1);
        *tmp = atof((char *) arg);
        return tmp;
    }
    // } else if () {
    //
    // }
}