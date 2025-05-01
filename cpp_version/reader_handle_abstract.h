// reader_handle_abstract.h

#pragma once

#include <string>

class Project;
class Reader;

class ReaderHandleAbstract {
public:
    virtual void handle(
        Project& project, 
        Reader& reader, 
        const std::string tag, 
        const std::string line
    ) = 0;
    
    virtual ~ReaderHandleAbstract() = default;
};
