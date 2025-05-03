// reader.cpp

#include <iostream>
#include <fstream>
#include <string>
#include <memory>
#include <algorithm>
#include <cctype>

#include "reader.h"
#include "reader_handle_abstract.h"
#include "reader_handle_song_information.h"
#include "reader_handle_global_settings.h"
#include "reader_handle_macro.h"

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
    static ReaderHandleMacro handle_macro;

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
    
    // macro block:
    dispatch["MACRO"] = &handle_macro;
    dispatch["MACROVRC6"] = &handle_macro;
    dispatch["MACRON163"] = &handle_macro;
    dispatch["MACROS5B"] = &handle_macro;

    // TODO - groove block
    // TODO - dpcm block
    // TODO - instrument block
    // TODO - special block
    // TODO - track block

}

Reader::Reader() {
    init_regex();
    init_dispatch();
}

std::string clean_line(std::string input) {
    std::string output;
    std::copy_if(input.begin(), input.end(), std::back_inserter(output),
        [](unsigned char c) {
            return c == '\n' || (c >= 32 && c <= 126);
        });
    return output;
}
    /*
    // Convert all tabs to spaces
    std::replace(line.begin(), line.end(), '\t', ' ');

    // Remove all '\r' and '\n' characters
    line.erase(std::remove(line.begin(), line.end(), '\r'), line.end());
    line.erase(std::remove(line.begin(), line.end(), '\n'), line.end());

    // Trim leading and trailing whitespace
    auto start = line.begin();
    while (start != line.end() && std::isspace(*start)) ++start;

    auto end = line.end();
    do {
        --end;
    } while (end != start && std::isspace(*end));

    return std::string(start, end + 1);
}
*/

int Reader::read(Project* project, const std::string input_file) {
    // Read file line by line, extract useful information
    std::string line;
    std::ifstream file(input_file);

    std::regex first_word_pattern("^\\s*(\\w+)");
    std::smatch match;
    std::string first_word;
    
    while (std::getline(file, line)) {
        // trim leading space, trailing spcae, \n, \r
        line = clean_line(line);

        if (std::regex_search(line, match, first_word_pattern)) {
            first_word = match[1];

            if (dispatch.find(first_word) != dispatch.end()) {
                dispatch[first_word]->handle(*project, *this, first_word, line);
            } else {
                std::cout << "[W] Key \'" << first_word << "\' not found: " << line << std::endl;
            }
        }
    }
    return 0;
}

