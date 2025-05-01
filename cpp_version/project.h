// project.h

#pragma once

#include <unordered_map>
#include <vector>
#include <string>

/*
#include "macro.h"
#include "instrument.h"
#include "track.h"
*/

// class Macro;
// class BaseInstrument;
// class Track;

class Project {
public:
    std::unordered_map<std::string, std::string> song_information;
    std::unordered_map<std::string, int> global_settings;

    // TODO continue the other attributes
    // std::unordered_map<std::string, Macro> macros; 
    // std::unordered_map<std::string, BaseInstrument> instruments;
    // std::vector<Track> tracks;

    // print self method
    friend std::ostream& operator<<(std::ostream& os, const Project& project);
};