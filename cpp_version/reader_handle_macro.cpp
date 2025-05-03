// reader_handle_macro.cpp

#include <iostream>
#include <string>
#include <regex>
#include <vector>

#include "reader_handle_macro.h"
#include "project.h"
#include "reader.h"

void ReaderHandleMacro::handle(
    Project& project, 
    Reader& reader, 
    const std::string tag, 
    const std::string line
){
    std::smatch match;

    auto it = reader.regex_patterns.find("MACRO");
    if (it != reader.regex_patterns.end()){
        const std::regex& pattern = it->second;
        if (std::regex_search(line, match, pattern)){
        // NOTE : [MACRO] [type] [index] [loop] [release] [setting] : [macro]
        std::string key;
        int macro_type;
        int macro_index;
        int macro_loop;
        int macro_release;
        int macro_setting;
        std::vector<int> macro_sequence;
       
        // TODO : 
        // create macro object, load it with data
        // add macro object to Project map

        } else {
            std::cout << "Macro: Did not match!" << std::endl;
        }
    } else {
        std::cerr << "[E] No regex pattern found for tag: " << tag << std::endl;
    }

}
