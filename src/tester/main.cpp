// Daniel Lombardi - RA: 738340
//
// g++ -Wall -pedantic -O2 -Wno-unused-result -g main.cpp -o main -std=c++11
//
// Utilização:
// Após a compilação, roda `./main $COMANDO`, para COMANDO, temos 3 opções:
//      - READ:     Ler a tabela;
//      - WRITE:    Escrever (adicionar itens à tabela);
//      - EDIT:     Editar um item da tabela;

#include <stdio.h>
#include <stdlib.h>

#include <iostream>


#define DEBUG                                               0
#define FILE_NAME                                   "./table"


template<typename... Args>
void log(const char* message, Args... args);
void log(const char* message);

struct registro {
    unsigned ID;
    unsigned categoria;
    char nome[40];
    float preco;
};

void toUpperCase(char *string);
unsigned getNextProductID(FILE *fp);


int main(int argc, char const *argv[]) {

    log("[INFO]::PARAMETERS:\n");
    for (size_t i = 0; i < argc; i++)
        log("[INFO]::    %s\n", argv[i]);


    if (argc < 2) {
        printf("[ERROR]::No operation requested.\n");
        return 1;
    }

    if (std::strcmp(argv[1], "READ") == 0) {
        printf("What is the ID of the product you would like to view? (-1 for all)\n");
        long requestID;
        scanf("%ld", &requestID);

        FILE *fp = fopen(FILE_NAME, "rb");
        registro tmp;
        if (requestID == -1)
            while (fread(&tmp, sizeof(registro), 1, fp)) {
                printf("\nID:            %u\n", tmp.ID);
                printf("\tCATEGORIA:     %u\n", tmp.categoria);
                printf("\tNOME:          %s\n", tmp.nome);
                printf("\tPRECO:         %.2f\n", tmp.preco);
            }
        else {
            fseeko(fp, requestID * sizeof(registro), 0);
            if (fread(&tmp, sizeof(registro), 1, fp)) {
                printf("\tCATEGORIA:    %u\n", tmp.categoria);
                printf("\tNOME:         %s\n", tmp.nome);
                printf("\tPRECO:        %f\n", tmp.preco);
            } else
                printf("PRODUCT ID TOO LARGE, NOT IN TABLE.\n");
        }


    } else if (std::strcmp(argv[1], "WRITE") == 0) {
        printf("How many products would you like to write to the table?\n");

        unsigned quant;
        scanf("%u", &quant);
        log("[INFO]::quant = %u\n", quant);

        FILE *fp = fopen(FILE_NAME, "ab+");
        unsigned nextID = getNextProductID(fp);

        registro *regs = (registro *) malloc(sizeof(registro) * quant);
        printf("Input Data:\n");
        for (size_t i = 0; i < quant; i++) {
            regs[i].ID = nextID++;

            printf("\nPRODUTO %lu:\n", i + 1);
            printf("\tNUMERO CATEGORIA: ");
            scanf("%d", &regs[i].categoria);

            printf("\tNOME: ");
            scanf("%s", regs[i].nome);

            printf("\tPRECO: ");
            scanf("%f", &regs[i].preco);
        }


        fseek(fp, 0, SEEK_END);
        fwrite(regs, sizeof(registro), quant, fp);
        fclose(fp);


    } else if (std::strcmp(argv[1], "EDIT") == 0) {
        printf("What is the ID of the product you would like to edit?\n");
        unsigned requestID;
        scanf("%u", &requestID);

        FILE *fp = fopen(FILE_NAME, "rb+");

        fseek(fp, requestID * sizeof(registro), 0);

        registro tmp;
        if (fread(&tmp, sizeof(registro), 1, fp)) {
            printf("ID:             %u\n", tmp.ID);
            printf("\tCATEGORIA:    %u\n", tmp.categoria);
            printf("\tNOME:         %s\n", tmp.nome);
            printf("\tPRECO:        %.2f\n", tmp.preco);
        } else {
            printf("PRODUCT ID TOO LARGE, NOT IN TABLE.\n");
            return 1;
        }

        printf("If you do NOT wish to change the field, type [-1] on it.\n");

        char userInput[40] = {0};
        printf("\tNUMERO CATEGORIA: ");
        scanf("%s", userInput);
        if (strcmp(userInput, "-1") != 0)
            tmp.categoria = atoi(userInput);

        printf("\tNOME: ");
        scanf("%s", userInput);
        if (strcmp(userInput, "-1") != 0)
            strcpy(tmp.nome, userInput);

        printf("\tPRECO: ");
        scanf("%s", userInput);
        if (strcmp(userInput, "-1") != 0)
            tmp.preco = atof(userInput);

        fwrite(&tmp, sizeof(registro), 1, fp);

        printf("Updated item:\n");
        printf("\tID:           %u\n", tmp.ID);
        printf("\tCATEGORIA:    %u\n", tmp.categoria);
        printf("\tNOME:         %s\n", tmp.nome);
        printf("\tPRECO:        %.2f\n", tmp.preco);

        fclose(fp);
    }

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


void toUpperCase(char *charArr) {
    // Precisa garantir que tem um caracter nulo no final, pra sair do do_while

    int i = 0;
    do // garante que o 6º bit menos significativo seja zero
        charArr[i] = charArr[i] & ~0x20;    // 0x20 = 32 = 0b00100000
    while(charArr[++i]);
}


unsigned getNextProductID(FILE *fp) {
    std::rewind(fp);

    if (fp == NULL)
        return 0;

    int nextID = 0;

    registro tmp;
    while (fread(&tmp, sizeof(registro), 1, fp))
        nextID++;

    return nextID;
}
