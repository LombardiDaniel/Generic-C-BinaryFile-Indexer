#ifndef INDEXER_HPP
#define INDEXER_HPP

// #include <stdlib.h>
// #include <string.h>
#include <iostream>
#include "utils.hpp"
#include "BSTree.hpp"

template <class T> // indexer recebe nodeBlock
class Indexer {
private:
    FILE *_fp;
    bool _hasValid;
    utils::Logger _logger;
    BinaryTree<T> index; // árvore é do tipo nodeBlock

public:
    std::string filePath; // path do arquivo que vai ser indexado
    std::string indexPath; // path que o indice sera salvo

    char *fileBuffer; // Alocado e Re-alocado on-copy
    unsigned long fileBufferSize;

    Indexer ();
    virtual ~Indexer ();

    int read(unsigned const size);

    void seekFromIndex(void *key);
};


// definição de funções:
// ...


#endif
