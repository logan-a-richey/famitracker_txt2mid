// reader_handle_song_information

#pragma once

#include "reader_handle_abstract.h"

class Project;
class Reader;

class ReaderHandleSongInformation : public ReaderHandleAbstract {
public:
    void handle(
        Project& project,
        Reader& reader, 
        const std::string tag, 
        const std::string line
    ) override;

    // Singleton method
    // static std::shared_ptr<ReaderHandleSongInformation> get_instance();
};
