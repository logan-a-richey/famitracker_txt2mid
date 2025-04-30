// text_export_reader.cpp

#include <iostream>
#include <cstring> // Required for strcpy

#include "text_export_reader.h"

// constructor
TextExportReader::TextExportReader(Project* p) : project(p) {
    // Constructor body (initialize project pointer)
}

// read file line by line, load Project* with data
int TextExportReader::read(std::string& input_file) {
    std::string line;
    std::ifstream file(input_file);
    int i = 0;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            // std::cout << "LINE = " << i << " \'" << line << "\'" << std::endl;
            // printf(" LINE %i = \'%s\'\n", i, line.c_str());
            std::cout << line << std::endl;
            i++;
        }
        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
        return 1;
    }
    return 0;
}
