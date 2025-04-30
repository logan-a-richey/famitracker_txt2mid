// macro.h

#ifndef MACRO_H
#define MACRO_H

#include <vector>

class Macro {
public:
    int macro_type;
    int macro_index;
    int macro_loop; 
    int macro_release;
    int macro_setting;
    std::vector<int> macro_sequence;

    // constructor
    // Macro();
};

#endif // MACRO_H