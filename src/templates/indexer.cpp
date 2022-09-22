#include <stdio.h>

#include "headers/indexer.hpp"
// #include "headers/utils.hpp"
#include "headers/BSTree.hpp"


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

void Indexer::seekFromIndex(void *key) {
    if (!tee.lookup(key)){
     this->_logger.error(
         "Unable to SEEK %p from file %s.\n", 
         this-> Key, this->filePath);
        return 1;
    }
    return tee.lookup(key);
}


