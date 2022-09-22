typedef struct {
    size_t size;
    unsigned long long id;
    char[80] myCustomClass;
    size_t classBloat;
    size_t secondClassBloat;
    float price;
    char grade;
    std::string description;
} myStruct;

print(
    size : 1;
    id : 2;
    myCustomClass : 3;
    classBloat : 4;
    secondClassBloat : 5;
    price : 6;
    grade : 7;
    description : 8;
)


(valor do CAMPO_ESPECIFICADO_DO_USUARIO; rrn do registro)

struct nos nós da árvore: (price, RRN)
->
adicionar os rrns da busca numa lista [rrn0, rrn1, rrn2, ...]
->
buscar pelos rrns no arquivo original
->
printar os structs
