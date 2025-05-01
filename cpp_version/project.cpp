// project.cpp

#include <iostream>

#include "project.h"

// custom print function
std::ostream& operator<<(std::ostream& os, const Project& project) {
    os << "--- Song Information ---\n";
    for (const auto& [key, val] : project.song_information) {
        os << key << " -> '" << val << "'\n";
    }
    os << "\n--- Global Settings ---\n";
    for (const auto& [key, val] : project.global_settings) {
        os << key << " -> " << val << '\n';
    }
    return os;
}