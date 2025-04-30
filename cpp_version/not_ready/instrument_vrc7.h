// instrument_vrc7.h

#include <vector>

#include "base_instrument.h"
#include "instrument_vrc7.h"

class VRC7_Instrument: public BaseInstrument {
public:
    int patch;
    std::vector<int> registers;
};

