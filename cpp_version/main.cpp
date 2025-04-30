#include <iostream>

// #include "project.h"

#include "project.h"
#include "reader.h"

int main(int argc, char** argv){
    std::cout << "Famitracker C++" << std::endl;

    if (argc <= 1){
        std::cout << "usage: ./main input.txt" << std::endl;
        return 1;
    }
    std::string input_file = argv[1];

    Reader reader;
    Project project;

    reader.read(&project, input_file);

    return 0;
}
