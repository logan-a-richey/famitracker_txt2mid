// instrument_vrc7.h

#include <vector>

#include <instrument_vrc7.h>

class VRC7_Instrument: public BaseInstrument {
    int patch;
    std::vector<int> registers;
};

