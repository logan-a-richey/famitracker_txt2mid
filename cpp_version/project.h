// project.h

#ifndef PROJECT_H
#define PROJECT_H

#include <map>
#include <vector>
#include <string>

#include "macro.h"
#include "instrument.h"
#include "track.h"

class Project {
public:
    std::map<std::string, std::string> song_information;
    std::map<std::string, int> global_settings;
    std::map<std::string, Macro> macros;
    std::map<std::string, Instrument> instruments;
    std::vector<Track> tracks;
};

#endif // PROJECT_H