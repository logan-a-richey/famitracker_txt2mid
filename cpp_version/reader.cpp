// reader.cpp

#include "reader.h"

#include <iostream>
#include <fstream>
#include <string>

Reader::Reader() {
    // load regex patterns
    
    std::regex song_information_pattern("^\\s*(\\w+)\\s+\"(.*)\"");
    std::regex global_settings_pattern("^\\s*(\\w+)\\s+(\\d+)");
    std::regex macro_pattern("^\\s*(\\w+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\\:\\s*(.*)");
    std::regex dpcmdef_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"");
    std::regex dpcm_pattern("^\\s*(\\w+)\\s*\\:\\s*(.*)");
    std::regex groove_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)");
    std::regex usegroove_pattern("^\\s*(\\w+)\\s*\\:\\s*(.*)");
    std::regex inst2a03_pattern("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"");
    std::regex instvrc6_pattern("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"");
    std::regex instvrc7_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s*\"(.*)\"");
    std::regex instfds_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"");
    std::regex instn163_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"");
    std::regex insts5b_pattern("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"");
    std::regex keydpcm_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\-?\\d+)\\s+");
    std::regex fdswave_pattern("^\\s*(\\w+)\\s+(\\d+)\\s*\\:\\s*(.*)");
    std::regex fdsmod_pattern("^\\s*(\\w+)\\s+(\\d+)\\s*\\:\\s*(.*)");
    std::regex fdsmacro_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+([012])\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)");
    std::regex n163wave_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)");
    std::regex track_pattern("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"");
    std::regex columns_pattern("^\\s*(\\w+)\\s*\\:\\s*(.*)");
    std::regex order_pattern("^\\s*(\\w+)\\s+([0-9A-F]{2})\\s*\\:\\s*(.*)");
    std::regex pattern_pattern("^\\s*(\\w+)\\s+([0-9A-F]{2})");
    std::regex row_pattern("^\\s*(\\w+)\\s+([0-9A-F]{2})\\s*\\:\\s*(.*)");
    std::regex hex2d_pattern("[0-9A-F]{2}");
    std::regex integer_pattern("\\-?\\d+");

    regex_patterns["SONG_INFORMATION"] = song_information_pattern;
    regex_patterns["GLOBAL_SETTINGS"] = global_settings_pattern;
    regex_patterns["MACRO"] = macro_pattern;
    regex_patterns["DPCMDEF"] = dpcmdef_pattern;
    regex_patterns["DPCM"] = dpcm_pattern;
    regex_patterns["GROOVE"] = groove_pattern;
    regex_patterns["USEGROOVE"] = usegroove_pattern;
    regex_patterns["INST2A03"] = inst2a03_pattern;
    regex_patterns["INSTVRC6"] = instvrc6_pattern;
    regex_patterns["INSTVRC7"] = instvrc7_pattern;
    regex_patterns["INSTFDS"] = instfds_pattern;
    regex_patterns["INSTN163"] = instn163_pattern;
    regex_patterns["INSTS5B"] = insts5b_pattern;
    regex_patterns["KEYDPCM"] = keydpcm_pattern;
    regex_patterns["FDSWAVE"] = fdswave_pattern;
    regex_patterns["FDSMOD"] = fdsmod_pattern;
    regex_patterns["FDSMACRO"] = fdsmacro_pattern;
    regex_patterns["N163WAVE"] = n163wave_pattern;
    regex_patterns["TRACK"] = track_pattern;
    regex_patterns["COLUMNS"] = columns_pattern;
    regex_patterns["ORDER"] = order_pattern;
    regex_patterns["PATTERN"] = pattern_pattern;
    regex_patterns["ROW"] = row_pattern;
    regex_patterns["hex2d"] = hex2d_pattern;
    regex_patterns["integer"] = integer_pattern;
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
    