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


    class Logger {

    public:
        enum logPriority : unsigned short {Debug = 0, Info, Warning, Error, Critical};
        static bool DEBUG; // Refers to debug mode (if set to true, will also print to terminal)
        static bool color;

    private:
        unsigned short _priority;
        std::string _logFilePath;
        char* _prefix;
        bool echo;

        template<typename... Args>
        void _appendToFile(const char* priorityStr, const char* message, Args... args) {
            std::ofstream logFile;
            FILE* pFile;

            std::string loggingPath;
            if (Logger::DEBUG)
                loggingPath = this->_logFilePath;
            else
                loggingPath = std::string("main.log");

            pFile = fopen((const char*) loggingPath.c_str(), "a+");

            std::fprintf(pFile, "[%s] - %s - %s - ", priorityStr, this->_prefix, currentDateTime().c_str());
            std::fprintf(pFile, message, args...);
            std::fprintf(pFile, ";\n");

            fclose(pFile);
        }

        template<typename... Args>
        void _logToStdOut(const char* priorityStr, const char* message, Args... args) {

            const char *color = this->color ? this->_getColor().c_str() : COLOR_RESET;

            std::fprintf(stdout, "[%s%s%s] - %s - %s - ",
                color, priorityStr, COLOR_RESET,
                this->_prefix, currentDateTime().c_str());

            std::fprintf(stdout, message, args...);
            std::fprintf(stdout, ";\n");
        }

        std::string _getColor() {

            std::string color;

            // {Debug = 0, Info, Warning, Error, Critical};
            switch (this->getPriority()) {
                case Logger::Debug:
                    break;

                case Logger::Info:
                    color = std::string(CYN);
                    break;

                case Logger::Warning:
                    color = std::string(BLU);
                    break;

                case Logger::Error:
                    color = std::string(YEL);
                    break;

                case Logger::Critical:
                    color = std::string(RED);
                    break;
            }

            return color;
        }


    public:
        Logger() {}
        Logger(char *loggerName, char *logFilePath, bool color=true, bool echo=false, unsigned short priority=Error) {

            this->_prefix = loggerName;
            this->_logFilePath = std::string(logFilePath);
            this->_priority = priority;

            this->color = color;
            this->echo = echo;
        }

        static void setDebug() {
            Logger::DEBUG = true;
        }

        static void unsetDebug() {
            Logger::DEBUG = false;
        }

        void setPriority(unsigned short priority) {
            this->_priority = priority;
        }

        unsigned short getPriority() {
            return this->_priority;
        }

        // Basic logging funcions:
        template<typename... Args>
        void debug(const char* message, Args... args) {
            if (this->_priority <= Logger::Debug) {
                this->_appendToFile("DEBUG\0", message, args...);
                if (Logger::DEBUG)
                    this->_logToStdOut("DEBUG\0", message, args...);
            }
        }

        template<typename... Args>
        void info(const char* message, Args... args) {
            if (this->_priority <= Logger::Info) {
                this->_appendToFile("INFO\0", message, args...);
                if (Logger::DEBUG)
                    this->_logToStdOut("INFO\0", message, args...);
            }
        }

        template<typename... Args>
        void warning(const char* message, Args... args) {
            if (this->_priority <= Logger::Warning) {
                this->_appendToFile("WARNING\0", message, args...);
                if (Logger::DEBUG)
                    this->_logToStdOut("WARNING\0", message, args...);
            }
        }

        template<typename... Args>
        void error(const char* message, Args... args) {
            if (this->_priority <= Logger::Error) {
                this->_appendToFile("ERROR\0", message, args...);
                if (Logger::DEBUG)
                    this->_logToStdOut("ERROR\0", message, args...);
            }
        }

        template<typename... Args>
        void critical(const char* message, Args... args) {
            if (this->_priority <= Logger::Critical) {
                this->_appendToFile("CRITICAL\0", message, args...);
                if (Logger::DEBUG)
                    this->_logToStdOut("CRITICAL\0", message, args...);
            }
        }
    };
}

#endif // UTILS_H
