# example.py

import re

# from stages.reader_handlers.SongInformationHandler import SongInformationHandler
# from stages.reader_handles.GlobalSettingsHandler import GlobalSettingsHandler

# --- Project class to store results ---
class Project:
    def __init__(self):
        self.song_information = {}
        self.global_settings = {}

# --- Base handler class ---
class BaseLineHandler:
    def __init__(self, tags):
        self.tags = tags  # tags that this handler will handle

    def try_handle(self, line: str, project) -> bool:
        raise NotImplementedError

# --- Song Information Handler ---
class SongInformationHandler(BaseLineHandler):
    def __init__(self):
        super().__init__(tags=[
            "TITLE", "AUTHOR", "COPYRIGHT", "COMMENT"
        ])
        self.pattern = re.compile(
            r'^\s*(TITLE|AUTHOR|COPYRIGHT|COMMENT)\s+"(.*?)"\s*$'
        )

    def try_handle(self, line: str, project) -> bool:
        match = self.pattern.match(line)
        if match:
            key, value = match.group(1), match.group(2)
            project.song_information[key] = value
            print(f"Handled song info: {key} = {value}")
            return True
        return False

# --- Global Settings Handler ---
class GlobalSettingsHandler(BaseLineHandler):
    def __init__(self):
        super().__init__(tags=[
            "MACHINE", "FRAMERATE", "EXPANSION", 
            "VIBRATO", "SPLIT", "N163CHANNELS"
        ])
        self.pattern = re.compile(
            r'^\s*(MACHINE|FRAMERATE|EXPANSION|VIBRATO|SPLIT|N163CHANNELS)\s+(\d+)\s*$'
        )

    def try_handle(self, line: str, project) -> bool:
        match = self.pattern.match(line)
        if match:
            key, value = match.group(1), int(match.group(2))
            project.global_settings[key] = value
            print(f"Handled global setting: {key} = {value}")
            return True
        return False

# --- Dispatcher with hashed lookup ---
class LineHandler:
    def __init__(self, project):
        self.project = project
        self.dispatch_table = self.build_dispatch_table()

    def build_dispatch_table(self):
        handlers = [SongInformationHandler(), GlobalSettingsHandler()]
        dispatch_table = {}
        for handler in handlers:
            for tag in handler.tags:
                dispatch_table[tag] = handler
        return dispatch_table

    def handle_line(self, line: str):
        if not line.strip() or line.startswith("#"):
            return
        keyword = line.split()[0].upper()
        handler = self.dispatch_table.get(keyword)
        if handler:
            handled = handler.try_handle(line, self.project)
            if not handled:
                print(f"Handler found but failed to parse: {line}")
        else:
            print(f"No handler for line: {line}")

# --- Main driver ---
def main():
    project = Project()
    handler = LineHandler(project)

    lines = [
        "TITLE \"Awesome Track\"",
        "AUTHOR \"Logan Richey\"",
        "COPYRIGHT \"2025 (c)\"",
        "MACHINE 0",
        "FRAMERATE 60",
        "SPLIT 1",
        "UNKNOWN \"no one handles this\"",
    ]

    for line in lines:
        handler.handle_line(line)
    
    print()
    print("Parsed Data:")
    print("Song Info:", project.song_information)
    print("Global Settings:", project.global_settings)

if __name__ == "__main__":
    main()

