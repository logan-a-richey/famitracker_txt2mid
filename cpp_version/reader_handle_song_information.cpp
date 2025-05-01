// reader_handle_song_information

#include <iostream>

#include "reader_handle_song_information.h"

class Project;
class Reader;

void ReaderHandleSongInformation::handle(
    Project& project, 
    Reader& reader, 
    const std::string tag, 
    const std::string line
) {
    std::cout << "In ReaderHandleSongInformation" << std::endl;
}
