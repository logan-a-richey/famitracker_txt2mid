// reader.h

#ifndef READER_H
#define READER_H

#include <string>

#include "project.h"
#include "macro.h"
#include "instrument.h"
#include "track.h"

class Reader{
public:
    void read(std::string input_file);

private:
    void handle_song_information(std::string line);
    void handle_global_settings(std::string line);
    void handle_macro(std::string line);
};

#endif // READER_H
