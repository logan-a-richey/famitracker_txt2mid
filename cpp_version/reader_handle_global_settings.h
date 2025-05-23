// reader_handle_song_information

#pragma once

#include <string>
#include "reader_handle_abstract.h"

class Project;
class Reader;

class ReaderHandleGlobalSettings : public ReaderHandleAbstract {
public:
    void handle(Project& project, Reader& reader, const std::string tag, const std::string line) override;
};
