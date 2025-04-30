// reader.cpp

#include "reader.h"

#include <iostream>
#include <fstream>
#include <string>

Reader::Reader() {
    // load regex patterns
    // 'TITLE "ASDF"
    std::regex song_information_pattern("^\\s*(\\w+)\\s+\"(.*)\"");
    regex_patterns["SONG_INFORMATION"] = song_information_pattern;

    std::regex global_settings_pattern("^\\s*(\\w+)\\s+(\\d+)");
    regex_patterns["GLOBAL_SETTINGS"] = global_settings_pattern;
}

int Reader::read(Project* project, std::string input_file){
    // Read file line by line, extract useful information
    std::string line;
    std::ifstream file(input_file);

    std::regex first_word_pattern("^\\s*(\\w+)");
    std::smatch match;
    std::string first_word;

    if (file.is_open()){
        while (std::getline(file, line)){
            // std::cout << line << std::endl; 
            if (std::regex_search(line, match, first_word_pattern)) {
                first_word = match[1];
                // std::cout << "First word: " << first_word << std::endl;
                std::cout << first_word << " | " << line << std::endl;
            } else {
                // std::cout << "First word: No match found." << std::endl;
                continue;
            }
        }
    } else {
        std::cout << "[E] Could not open file." << std::endl;
    }

    return 0;
}

int default_line_handler(Project* project, std::string line){
    std::cout << "[W] DefaultHandler: " << line << std::endl;
    return 0;
}

int handle_song_information(Project* project, std::string line){
    
    return 0;
}

int handle_global_settings(Project* project, std::string line){
    return 0;
}
    