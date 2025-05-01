#include <iostream>

// #include "project.h"

#include "project.h"
#include "reader.h"

int main(int argc, char** argv){
    // simple check usage
    if (argc <= 1){
        std::cout << "usage: ./main input.txt" << std::endl;
        return 1;
    }

    // get the input file
    const std::string input_file = argv[1];

    // create an instance of project and reader
    Project project;
    Reader reader;

    // read data from input.txt using Reader into Project
    reader.read(&project, input_file);

    std::cout << project << std::endl;

    return 0;
}
