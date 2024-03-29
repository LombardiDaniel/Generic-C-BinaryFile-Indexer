// This file is to be used as part of a Jinja2 template


// error handling:
//      https://www.youtube.com/watch?v=IZiUT-ipnj0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>


{% obj.c_struct %}
typedef {% obj.struct_name %} userStruct;

static const size_t SIZE_OF_STRUCT = sizeof(userStruct);

{% if obj.is_variable_size %}
    {obj.c_struct_head} // c_struct_head is first fixed sizes
    typedef {% obj.struct_head_name %} userStructInput;

    static const size_t SIZE_OF_STRUCT_HEAD = sizeof(userStructInput);
{% endif %}

#define DEBUG                                               {% file.debug|default(0, true) %}


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
