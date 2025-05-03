// reader_handle_macro.h

#pragma once
#include <string>

#include "reader_handle_abstract.h"

class Project;
class Reader;

class ReaderHandleMacro : public ReaderHandleAbstract {
public:
    void handle(Project& project, Reader& reader, const std::string tag, const std::string line) override;
};
