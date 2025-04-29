// instrument_2a03.cpp

#include <string>

#include <instrument_2a03.h>

// constructor
Instrument_2A03(
    int _index,
    std::string _name, 
    int _seq_vol,
    int _seq_arp,
    int _seq_pit,
    int _seq_hpi,
    int _seq_dut
){
    index   = _index;
    name    = _name;
    seq_vol = _seq_vol;
    seq_arp = _seq_arp;
    seq_pit = _seq_pit;
    seq_hpi = _seq_hpi;
    seq_dut = _seq_dut;
}
