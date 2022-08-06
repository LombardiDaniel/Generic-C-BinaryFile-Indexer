#include <iostream>
#include <stdlib.h>
#include <ctime>
#include <sys/stat.h>
#include <sys/time.h>
#include <chrono>
#include <dirent.h>

#include <sstream>
#include <iomanip>

#include "headers/utils.hpp"
#include "headers/ANSI_color_codes.h"


#define BLACK                                      "\e[0;30m"
#define RED                                        "\e[0;31m"
#define GREEN                                      "\e[0;32m"
#define YELLOW                                     "\e[0;33m"
#define BLUE                                       "\e[0;34m"
#define MAGENTA                                    "\e[0;35m"
#define CYAN                                       "\e[0;36m"
#define WHITE                                      "\e[0;37m"
#define RESET                                       "\x1b[0m"
#define BOLD                                       "\033[;1m"


namespace utils {

    bool Logger::DEBUG = 0;

    const std::string frameDefaultFileName = "ASCII_stl_renderer_";


    bool fileExists(const std::string& filePath) {
        struct stat buffer;
        return (stat (filePath.c_str(), &buffer) == 0);
    }


    std::string getNextFileName(const std::string sDir, std::string filePattern) {
        // This functions gets the next file name for saving "screen shots".
        //
        // Args:
        //     - sDir: The directory to where the file will be saved.
        //     - filePattern: The pattern the file will be saved.
        //          ex: "stl_screenshot_"
        //
        // Returns:
        //     - fileName: The filePattern appended with the correct (next)
        //          number in the sequence, ex: "stl_screenshot_1"
        //          if the returned string is empty, means the program could not open
        //          the directory.


        unsigned counter = 0;
        std::vector<std::string> files;

        DIR *dir;
        dirent *diread;

        if ((dir = opendir(sDir.c_str())) != nullptr) {

            while ((diread = readdir(dir)) != nullptr)
                files.push_back(diread->d_name);

            closedir(dir);
        } else
            return std::string("");

        for (const auto & currDirPath : files)
            if (currDirPath.rfind(filePattern, 0) == 0) // maybe check if file ends with desired extension?
                counter++;

        filePattern.append(std::to_string(counter));

        return filePattern;
    }


    const std::string currentDateTime() {
        // Get current date/time, format is YYYY-MM-DD.HH-mm-ss
        auto t = std::time(nullptr);
        auto tm = *std::localtime(&t);

        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d.%H:%M:%S");
        auto str = oss.str();

        return str;
    }
}
