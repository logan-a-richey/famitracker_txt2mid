// macro.h

#ifndef MACRO_H
#define MACRO_H

#include <string>
#include <vector>

class Macro {
public:
    int type;
    int index;
    int loop;
    int release;
    int setting;
    std::vector<int> sequence;
};

#endif // MACRO_H

