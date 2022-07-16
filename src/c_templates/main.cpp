#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <vector>


#define TAM_NOME                                        1<<10
#define DEBUG                                               0


#define BLACK                                      "\e[0;30m"
#define RED                                        "\e[0;31m"
#define GREEN                                      "\e[0;32m"
#define YELLOW                                     "\e[0;33m"
#define BLUE                                       "\e[0;34m"
#define MAGENTA                                    "\e[0;35m"
#define CYAN                                       "\e[0;36m"
#define WHITE                                      "\e[0;37m"
#define RESET                                       "\x1b[0m"
#define BOLD                                       "\033[;1m"


template<typename... Args>
void log(const char* message, Args... args);
void log(const char* message);


int main(int argc, char const *argv[]) {

    // scanf em C mesmo pq eh mais facil
    // char cFileName[TAM_NOME] = {0};
    // scanf("%s", cFileName);

    std::string fileName;
    std::cin.ignore();
    getline(std::cin, fileName);

    FILE *fp = fopen(fileName.c_str(), "r");

    if (fp != NULL) {
        long long unsigned numMoedas;
        fscanf(fp, "%llu", &numMoedas);
        log("numMoedas: %lld\n", numMoedas);

        int *pesos = new int[numMoedas];
        for (size_t i = 0; i < numMoedas; i++)
            fscanf(fp, "%d", &pesos[i]);
    } else {
        printf(RED);
        printf("FILE NOT FOUND\n");
        printf(WHITE);
    }

    fclose(fp);

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
