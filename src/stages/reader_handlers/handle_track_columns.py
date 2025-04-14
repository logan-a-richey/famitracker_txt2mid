# handle_track_columns.py

from stages.reader_handlers.base_handler import BaseHandler
class HandleTrackColumns(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*
            (?P<tag>COLUMNS)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        )

    def handle(self, line: str) -> bool:
        return 1

