# Generic C/C++ BinaryFile Indexer 🗂

##### _TO-DO_: Na programação em C/C++ utilizamos typedef p/ definir o tipo da struct.

tbm pode usar getpagesize() pra compilar o código e gerar a melhor indexação pra árvores-B

A generic indexer for C/C++ binary files. A Project for our Data Management Class in UFSCar

-   Daniel Lombardi - 738340
-   Leticia Machado - 790945
-   Vinicius Rodrigues - 790717

## Tabela de Conteúdos

-   [Sobre o Projeto](#sobre-o-projeto)
    -   [Descrição do YAML](#descricao-do-yaml)
    -   [Limitações](#limitacoes)
    -   [Feito com](#feito-com)
-   [Desenvolvendo](#desenvolvendo)
    -   [Pré requisitos](#pré-requisitos)
    -   [Organização do Projeto](#organização-do-projeto)
        <!-- -   [Variáveis de Ambiente](#variáveis-de-ambiente)
        -   [Chaves de Acesso](#chaves-de-acesso)
        -   [Logs](#logs)
        -   [Comandos](#comandos) -->
-   [License](#license)

## Sobre o Projeto

Nossa ideia para o trabalho é criar um programa genérico para indexação de arquivos binários.

O usuário passa a descrição das structs salvas por um arquivo YAML e nosso programa indexa e oferece uma interface para busca ao usuário.

O programa irá funcionar utilizando uma interface em python para a especificação da struct. Utilizando cookie-cutters, o programa (a partir de templates de arquivos em C/C++ para interação e indexação dos arquivos binários) gerará um código para ser compilado. O programa realizará chamadas ao g++ para compilar o código em C/C++, que terá seu terminal mapeado para o programa em python.

Ou seja, o programa terá seu executor escrito em C/C++ e compilado JIT, e terá uma CLI em python.

Ainda não foi decidido exatamente como a interação entre os arquivos C/C++ e python ocorrerá. No momento, pensamos em utilizar a biblioteca de sub-processos do python, já que permite total aceleração em C/C++.

Exemplo do arquivo YAML de configuração da struct:

```yaml
myStruct:
    - size_t: __size__ofStruct # encalpsulates next group
    # All size descriptors must have `_size_` in their
    - unsigned long long: id
    - 80: myCustomClass
    - size_t: # Since this item is a list, it is assumed this will be the size descriptor for EACH ITEM in the list
        - classBloat # this is part of a list, thus it is limited by the 'size_t' directive that came before it
        - secondClassBloat # part of list, thus same size
    - float: price
    - char: grade
    - _: description # '_' indicates this field is of variable size
```

### Descrição do YAML:

O YAML se estrutura abaixo de uma chave que indica o nome da struct. A chave abre uma lista de dicionários, cada dicionário tem o formato `tipo de dado`: `{diretiva_de_tamanho(opcinoal)}nome do campo`. Para o nome do campo, existem duas diretivas para representar **indicadores de tamanho**:

-   `__size__`: indica o tamanho do registro completo
-   `_size_`: indica o tamanho do **próximo** campo

Indicadores de tamanho serão utilizados para calcular os campos do tipo `_` ou `char *`. O indicador `_` é um curinga para `tamanho de campo variável`.

No exemplo `myStruct` demonstrado acima, temos `__size__ofStruct`, este sinaliza o tamanho total do registro atual, já que se inicializa com `__size__`.

Para ver os tipos de dados aceitos na yaml, ver o arquivo [src/c_data_types.py](src/c_data_types.py)

### Limitações:

Não consegue ler campos ou registros separados por limitadores.
Não consegue ler campos de tamanho variável.
__aligned__

Made with [python3.10](https://www.python.org/downloads/release/python-3100/).

Support for bit fields is NOT planned.


### Planed Stuff

- [x]
- [ ]

##### Python


##### C/C++ engine
