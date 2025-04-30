// main.cpp

#include <iostream>
#include <cstdio>
#include <string>
#include <fstream>
#include <memory>

#include <vector>
#include <map>

#include "project.h"
#include "text_export_reader.h"

int main(int argc, char** argv)
{
    // get input file from cmdline
    if (argc <= 1) {
        printf("[USAGE] ./main input.txt\n");
        return 1;
    }
    std::string input_file = argv[1];
    
    // create Project object as unique_ptr
    std::unique_ptr<Project> project = std::make_unique<Project>();
    
    // create TextExportReader object as unique_ptr and pass the Project pointer
    std::unique_ptr<TextExportReader> reader = std::make_unique<TextExportReader>(project.get());

    // Call the read function
    reader->read(input_file);
    
    // No need to delete anything since unique_ptr will automatically free the memory
    return 0;
}
