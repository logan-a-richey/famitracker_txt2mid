//  track.h

#ifndef TRACK_H
#define TRACK_H

#include <vector>
#include <map>
#include <string>

class Track {
public:
    int num_rows;
    int num_cols;
    std::vector<int> eff_cols;
    int tempo;
    int speed;
    std::string track_name;

    std::map<std::string, std::vector<std::string>> orders;
    std::map<std::string, std::string> tokens;

    // Track();

};

#endif // TRACK_H
