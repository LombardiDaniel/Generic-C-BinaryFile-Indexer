#ifndef UTILS_H
#define UTILS_H


#include <iostream>
#include <vector>
#include <fstream>

#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "ANSI_color_codes.h"


#define PI                                          3.141592


namespace utils {

    const std::string currentDateTime();

    bool fileExists(const std::string& filePath);

    std::string getNextFileName(const std::string sDir, std::string filePattern);

    char *toUpperCase(char *string);

    inline char toUpperCase(char &c);

    template <typename T>
    T modulus(T val) {
        if (val >= 0)
            return val;
        return -val;
    }

    template <typename T = char*>
    void _insert_color(char* original, unsigned int pos, T new_insertion) {
        for (size_t i = 0; i < 6; i++)
            original[i + pos] = new_insertion[i + pos];
    }

    template <typename T>
    void swap(T& a, T& b) {
        T tmp = a;
        a = b;
        b = tmp;
    }

}

#endif // UTILS_H
