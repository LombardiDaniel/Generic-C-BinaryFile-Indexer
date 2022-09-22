#define PATH "original.txt"

#include <iostream>
#include <cstring>
#include <fstream>

typedef char * index_type;


typedef struct {
    unsigned long long id;
    //char[80] myCustomClass;
    size_t classBloat;
    size_t secondClassBloat;
    float price;
    float horario;
    float outro;
    char grade;

} myStruct;



int size_before_indexed = sizeof(unsigned long long) +
                      80 + sizeof(size_t) + sizeof(size_t);
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
    unsigned long long rrn;
};

int index_file(char * path, index_type value){
   std::ifstream infile;
   infile.open("PATH");
   int current = size_before_indexed;

    struct nodeBlock bufferStruct;

   while(!EOF){

        infile.seekg(current, std::ios::beg);

        current = size_before_indexed + total_size_of_struct;
        infile.read(bufferStruct.userField, sizeof(index_type)) ;
        bufferStruct.rrn = (int)current / total_size_of_struct;

        // insert(bufferStruct);
   }

   infile.close();
   return 0;
}

int search(char * path, index_type value){

}

int main(int argc, char const* argv[]){
    if (argc < 2)
    {
        // Mensagem de erro aí
        return 1;
    }
    if(strcmp(toUpperCase(argv[1]), "INDEX") == 0){
        index_file(PATH, (index_type)*argv[1]);
    } else if(strcmp(toUpperCase(argv[1]), "SEARCH") == 0){
        search(PATH, (index_type)argv[1]);
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
