#ifndef INDEXER_HPP
#define INDEXER_HPP

// #include <stdlib.h>
// #include <string.h>
#include <iostream>
#include "utils.hpp"


class Indexer {
private:
    FILE *_fp;
    bool _hasValid;
    utils::Logger _logger;

public:
    std::string filePath;
    std::string indexPath;

    char *fileBuffer; // Alocado e Re-alocado on-copy
    unsigned long fileBufferSize;

    Indexer ();
    virtual ~Indexer ();

    int readStr(unsigned const len);
    int readSize(unsigned const size);

    void seekFromIndex(void *key);


};



#endif
