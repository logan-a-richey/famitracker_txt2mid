// project.h

#include <string>
#include <map>
#include <vector>

// #include <macro.h>
// #include <base_instrument.h>
// #include <track.h>

class Project {
public:
    std::map<std::string, std::string> song_information;
    std::map<std::string, int> global_settings;
    // std::map<std::string, Macro> macros;
    // std::map<std::string, BaseInstrument> instruments;
    // std::vector<Track> tracks;
};
