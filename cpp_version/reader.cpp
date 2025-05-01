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
