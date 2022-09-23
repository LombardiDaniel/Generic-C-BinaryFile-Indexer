// This file is to be used as part of a Jinja2 template

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>


#define DEBUG                                               true
#define USER_FILE_PATH "/Users/daniellombardi/Desktop/UFSCar/_current.nosync/ORI/TRAB/Generic-C-BinaryFile-Indexer/descricao.txt"
#define INDEXER_C_TYPE "float"

typedef float indexed_data_type;

struct {
    
        unsigned id;
    
        unsigned categoria;
    
        char myCustomClass[40];
    
} userStructHead;

struct {
    
        unsigned id;
    
        unsigned categoria;
    
        char myCustomClass[40];
    
        float __index__preco;
    
} userStruct;

static const size_t SIZE_OF_STRUCT = sizeof(userStruct);
static const size_t SIZE_OF_HEAD = sizeof(userStructHead);

struct nodeBlock {
    float userField;
    unsigned long long rrn;
};
// need to save "__index__preco"

template<typename... Args>
void log(const char* message, Args... args);
void log(const char* message);
void log(const std::string message);


int main(int argc, char const *argv[]) {
    // Expected args:
    //      - 0 : TABLE_PATH (str) : path of the table to be indexed
    //      - 1 : COMMAND (int) :
    //              - 0 : User is asking to index table
    //              - 1 : User is asking to print index table
    const std::string TABLE_PATH = std::string(argv[0]);
    const int COMMAND = atoi(argv[1]);

    const std::string INDEX_PATH = TABLE_PATH + std::string("_INDEX");

    ind = Indexer<nodeBlock>();

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