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
        std::string match_key = match[1];
        std::string match_type = match[2];
        std::string match_index = match[3];
        std::string match_loop = match[4];
        std::string match_release = match[5];
        std::string match_setting = match[6];
        std::string match_sequence = match[7];

        int macro_type = std::atoi(match_type.c_str());
        int macro_index = std::atoi(match_index.c_str());
        int macro_loop = std::atoi(match_loop.c_str());
        int macro_release = std::atoi(match_release.c_str());
        int macro_setting = std::atoi(match_setting.c_str());
        
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
