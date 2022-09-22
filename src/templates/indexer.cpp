#include <stdio.h>

#include "headers/indexer.hpp"
// #include "headers/utils.hpp"


Indexer::Indexer() {
    this->_logger = utils::Logger(
        (char *) "Indexer",
        (char *) "indexer.log",
        utils::Logger::Debug
    );

    this->_logger.setDebug();
}

int Indexer::readStr(unsigned const len) {

    char *byteBuffer = (char *) malloc(sizeof(char) * len);

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

void Indexer::readSize(unsigned const size) {
    
}
