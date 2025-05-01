// reader_handle_global_settings.cpp

#include <iostream>

#include "reader_handle_global_settings.h"

class Project;
class Reader;

void ReaderHandleGlobalSettings::handle(
    Project& project, 
    Reader& reader, 
    const std::string tag, 
    const std::string line
) {
    std::cout << "In ReaderHandleGlobalSettings" << std::endl;
}
