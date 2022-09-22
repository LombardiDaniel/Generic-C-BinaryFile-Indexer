#ifndef INDEXER_HPP
#define INDEXER_HPP
#include <stdio.h>

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

    void seekFromIndex(T key);
    
    void in


};

Indexer::Indexer() {
    this->_logger = utils::Logger(
        (char *) "Indexer",
        (char *) "indexer.log",
        utils::Logger::Debug
    );

    this->_logger.setDebug();
}

int Indexer::read(unsigned const size) {

    char *byteBuffer = (char *) malloc(sizeof(char) * size);

    if (len != fread(&byteBuffer, sizeof(char), len, this->_fp)) {
        this->_logger.error(
            "Unable to READ bytes in %d, from file %s.\n",
            this->_fp,
            this->filePath);
        return 1;
    }

    this->fileBufferSize += len;
    this->fileBuffer = (char *) realloc(this->fileBuffer, this->fileBufferSize);
}

void Indexer::seekFromIndex(index key) {
    if (!tee.lookup(key)){
        this->_logger.error(
            "Unable to SEEK %p from file %s.\n", 
            this->key, this->filePath);
        return 1;
    }
    return key.rrn;
}


void Idexer::indexar

#endif
