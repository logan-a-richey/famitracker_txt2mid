// track.h

#include <string>
#include <vector>
#include <unordered_map>

class Track {
public:
    std::string name;
    int speed;
    int num_rows;
    int num_cols;
    std::vector<int> eff_cols;

    std::unordered_map<std::string, std::vector<std::string>> orders;
    std::unordered_map<std::string, std::string> tokens;
};
