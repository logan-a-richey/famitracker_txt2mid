// reader_handle_song_information

#include <iostream>
#include <string>
#include <regex>

#include "reader_handle_song_information.h"

#include "project.h"
#include "reader.h"

void ReaderHandleSongInformation::handle(Project& project, Reader& reader, const std::string tag, const std::string line) {
    std::smatch match;
    auto it = reader.regex_patterns.find("SONG_INFORMATION");
    if (it != reader.regex_patterns.end()) {
        const std::regex& pattern = it->second;
        if (std::regex_match(line, match, pattern)) {
            std::string key = match[1];
            std::string val = match[2];
            project.song_information[key] = val;
        }
    } else {
        std::cerr << "[E] No regex pattern found for tag: " << tag << std::endl;
    }
}
