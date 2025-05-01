// reader_handle_global_settings.cpp

#include <iostream>
#include <string>
#include <regex>

#include "reader_handle_global_settings.h"

#include "project.h"
#include "reader.h"

void ReaderHandleGlobalSettings::handle( Project& project, Reader& reader, const std::string tag, const std::string line) {
    std::smatch match;
    // std::string line;
    // std::string test_line = "MACHINE 456";

    auto it = reader.regex_patterns.find("GLOBAL_SETTINGS");
    if (it != reader.regex_patterns.end()) {
        const std::regex& pattern = it->second;
        if (std::regex_search(line, match, pattern)) {
        // if (std::regex_search(test_line, match, pattern)) {
            std::cout << "In SongInfo match!" << std::endl;

            std::string key = match[1];
            std::string sval = match[2];
            int val = std::atoi(sval.c_str());

            project.global_settings[key] = val;
        } else {
            std::cout << "Info: Did not match!" << std::endl;
        }
    } else {
        std::cerr << "[E] No regex pattern found for tag: " << tag << std::endl;
    }
}
