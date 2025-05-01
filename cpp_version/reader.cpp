// reader.cpp

#include <iostream>
#include <fstream>
#include <string>
#include <memory>

#include "reader.h"
#include "reader_handle_abstract.h"
#include "reader_handle_song_information.h"
#include "reader_handle_global_settings.h"

void Reader::init_regex(){
   // load regex patterns 
   regex_patterns["SONG_INFORMATION"] = std::regex("^\\s*(\\w+)\\s+\"(.*)\"$"); 
   regex_patterns["GLOBAL_SETTINGS"] = std::regex("^\\s*(\\w+)\\s+(\\d+)$"); 
   regex_patterns["MACRO"] = std::regex("^\\s*(\\w+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["DPCMDEF"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["DPCM"] = std::regex("^\\s*(\\w+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["GROOVE"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["USEGROOVE"] = std::regex("^\\s*(\\w+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["INST2A03"] = std::regex("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["INSTVRC6"] = std::regex("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["INSTVRC7"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s+([0-9A-F]{2})\\s*\"(.*)\"$"); 
   regex_patterns["INSTFDS"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["INSTN163"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["INSTS5B"] = std::regex("^\\s*(\\w+)(\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["KEYDPCM"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\-?\\d+)\\s+$"); 
   regex_patterns["FDSWAVE"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["FDSMOD"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["FDSMACRO"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+([012])\\s+(\\-?\\d+)\\s+(\\-?\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["N163WAVE"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["TRACK"] = std::regex("^\\s*(\\w+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*\"(.*)\"$"); 
   regex_patterns["COLUMNS"] = std::regex("^\\s*(\\w+)\\s*\\:\\s*(.*)$"); 
   regex_patterns["ORDER"] = std::regex("^\\s*(\\w+)\\s+([0-9A-F]{2})\\s*\\:\\s*(.*)$"); 
   regex_patterns["PATTERN"] = std::regex("^\\s*(\\w+)\\s+([0-9A-F]{2})$"); 
   regex_patterns["ROW"] = std::regex("^\\s*(\\w+)\\s+([0-9A-F]{2})\\s*\\:\\s*(.*)$"); 
   regex_patterns["hex2d"] = std::regex("[0-9A-F]{2}"); 
   regex_patterns["integer"] = std::regex("\\-?\\d+"); 
}

void Reader::init_dispatch(){
    // TODO
    // statically allocate
    static ReaderHandleSongInformation handle_song_information;
    static ReaderHandleGlobalSettings handle_global_settings;

    // load dispatch table
    // song information block
    dispatch["TITLE"] = &handle_song_information;
    dispatch["AUTHOR"] = &handle_song_information;
    dispatch["COPYRIGHT"] = &handle_song_information;
    dispatch["COMMENT"] = &handle_song_information;

    // global setting block
    dispatch["MACHINE"] = &handle_global_settings;
    dispatch["FRAMERATE"] = &handle_global_settings;
    dispatch["EXPANSION"] = &handle_global_settings;
    dispatch["VIBRATO"] = &handle_global_settings;
    dispatch["SPLIT"] = &handle_global_settings;
    dispatch["N163CHANNELS"] = &handle_global_settings;
}

Reader::Reader() {
    init_regex();
    init_dispatch();
}

int Reader::read(Project* project, const std::string input_file) {
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
                
                if (dispatch.find(first_word) != dispatch.end()) {
                    dispatch[first_word]->handle(*project, *this, first_word, line);
                } else {
                    std::cout << "[W] Key \'" << first_word << "\' not found" << line << std::endl;
                }
            } else {
                // std::cout << "First word: No match found:" << line << std::endl;
                continue;
            }
            if (first_word == "SPLIT") break;
        }
    } else {
        std::cout << "[E] Could not open file." << std::endl;
    }

    return 0;
}
