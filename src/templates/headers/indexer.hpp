#ifndef INDEXER_HPP
#define INDEXER_HPP
#include <stdio.h>

// #include<stdlib.h>
// #include <string.h>
#include <iostream>
#include "utils.hpp"
#include "BSTree.hpp"

template<class T> // indexer recebe nodeBlock
class Indexer {
private:
    FILE *_fp;
    bool _hasValid;
    // utils::Logger _logger;
    BinaryTree<T> index; // árvore é do tipo nodeBlock

public:
    std::string filePath; // path do arquivo que vai ser indexado
    std::string indexPath; // path que o indice sera salvo

    char *fileBuffer; // Alocado e Re-alocado on-copy
    unsigned long fileBufferSize;

    void add(T nodeBlock);

    int read(unsigned const size);

    unsigned long long seekFromIndex(T &block); // Isso vai pegar key de uma váriavel

    void deleteIndex(T nodeBlock);


};


template<class T> // indexer recebe nodeBlock
void Indexer<T>::add(T nodeBlock) {
    // if(nodeBlock == NULL)
        // this->_logger = utils::Logger(
        //     (char *) "Indexer",
        //     (char *) "indexer.log",
        //     utils::Logger::Debug
        // );
    this->index.add(nodeBlock);
}


template<class T> // indexer recebe nodeBlock
int Indexer<T>::read(unsigned const size) {

    char *byteBuffer = (char *) malloc(sizeof(char) * size);

    if (size != fread(&byteBuffer, sizeof(char), size, this->_fp)) {
        // this->_logger.error(
        //     "Unable to READ bytes in %d, from file %s.\n",
        //     this->_fp,
        //     this->filePath);
        return 1;
    }

    this->fileBufferSize += size;
    this->fileBuffer = (char *) realloc(this->fileBuffer, this->fileBufferSize);
}


template<class T> // indexer recebe nodeBlock
unsigned long long Indexer<T>::seekFromIndex(T &block) {
    if (!this->index.lookup(block))
        return 1;

    return block.offset;
}



template<class T> // indexer recebe nodeBlock
void Indexer<T>::deleteIndex(T nodeBlock){
    this->index.deleteTree(nodeBlock);
}

#endif
