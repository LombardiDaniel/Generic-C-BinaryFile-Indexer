#ifndef INDEXER_HPP
#define INDEXER_HPP

// #include <stdlib.h>
// #include <string.h>
#include <iostream>
#include "utils.hpp"
#include "btree.h"


class Indexer {
private:
    FILE *_fp;
    bool _hasValid;
    utils::Logger _logger;
    BTREE index;

public:
    std::string filePath; // path do arquivo que vai ser indexado
    std::string indexPath; // path que o indice sera salvo

    char *fileBuffer; // Alocado e Re-alocado on-copy
    unsigned long fileBufferSize;

    Indexer ();
    virtual ~Indexer ();

    int readStr(unsigned const len);     // le string de tamanho `len`
    int readSize(unsigned const size);   // le item de tamanho `size`

    void seekFromIndex(void *key);


};



#endif
