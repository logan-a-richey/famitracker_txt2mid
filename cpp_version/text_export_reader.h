// text_export_reader.h

#ifndef TEXT_EXPORT_READER_H
#define TEXT_EXPORT_READER_H

#include <string>
#include <fstream>
#include <memory> // for unique_ptr

#include "project.h"

class TextExportReader {
public:
    Project* project;
    
    // Constructor declaration
    TextExportReader(Project* p);  // Constructor prototype
    
    // Read function
    int read(std::string& input_file);
};

#endif // TEXT_EXPORT_READER_H
