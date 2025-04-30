// instrument_vrc7.cpp

#include <string>
#include <vector>

#include <instrument_vrc7.h>

// constructor
Instrument_VRC7::Instrument_VRC7(
    int _index, 
    std::string _name, 
    int _patch, 
    std::vector<int> 
    _registers
){
    index = _index; 
    name = _name;
    patch = _patch;
    registers = _registers;
}
