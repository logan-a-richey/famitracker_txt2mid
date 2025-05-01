// reader.h

#pragma once

#include <string>
#include <unordered_map>
#include <regex>
#include <memory>

#include "project.h"
#include "reader_handle_abstract.h"

class Reader {
public:
    // constructor
    Reader();
    int read(Project* project, const std::string input_file);

private:
    std::unordered_map<std::string, std::regex> regex_patterns;
    std::unordered_map<std::string, ReaderHandleAbstract*> dispatch;

    void init_regex();
    void init_dispatch();
    int process_line(Project* project, std::string line);
};
