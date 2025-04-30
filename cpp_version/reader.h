// reader.h

#pragma once

#include <string>

#include "project.h"

class Reader {
public:
    int read(Project* project, std::string input_file);

private:
    int default_line_handler(Project* project, std::string line);
    int handle_song_information(Project* project, std::string line);
    int handle_global_settings(Project* project, std::string line);
    
    /*
    int handle_dpcmdef(Project* project, std::string line);
    int handle_dpcm(Project* project, std::string line);
    int handle_groove(Project* project, std::string line);
    int handle_usegroove(Project* project, std::string line);
    int handle_inst2a03(Project* project, std::string line);
    int handle_instvrc6(Project* project, std::string line);
    int handle_instvrc7(Project* project, std::string line);
    int handle_instfds(Project* project, std::string line);
    int handle_instn163(Project* project, std::string line);
    int handle_insts5b(Project* project, std::string line);
    int handle_keydpcm(Project* project, std::string line);
    int handle_fdswave(Project* project, std::string line);
    int handle_fdsmod(Project* project, std::string line);
    int handle_fdsmacro(Project* project, std::string line);
    int handle_n163wave(Project* project, std::string line);
    int handle_track(Project* project, std::string line);
    int handle_columns(Project* project, std::string line);
    int handle_order(Project* project, std::string line);
    int handle_pattern(Project* project, std::string line);
    int handle_row(Project* project, std::string line);
    */
};
