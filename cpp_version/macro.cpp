// macro.cpp

#include <string>
#include <vector>

#include "macro.h"

// constructor 
Macro::Macro(
    int _type, 
    int _index,
    int _loop,
    int _release,
    int _setting,
    std::vector<int> _sequence
) {
    type     = _type; 
    index    = _index; 
    loop     = _loop; 
    release  = _release; 
    setting  = _setting; 
    sequence = _seq;
}

