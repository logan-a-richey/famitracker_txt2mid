// instrument_2a03.h

#include <string>
// #include <macro.h>

class Instrument_2A03: public BaseInstrument {
public:
    // unique
    int seq_vol;
    int seq_arp;
    int seq_pit;
    int seq_hpi;
    int seq_dut;

    // reserve spots for macros 
    void* macro_vol = nullptr;
    void* macro_arp = nullptr;
    void* macro_pit = nullptr;
    void* macro_hpi = nullptr;
    void* macro_dut = nullptr;


};
