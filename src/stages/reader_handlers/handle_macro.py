# stages/reader/handle_macro.py

import re

from stages.reader_handlers.base_handler import BaseHandler
from containers.macro import Macro

class HandleMacro(BaseHandler):
    def __init__(self, project):
        super().__init__(project)
        self.pattern = re.compile(r'''
            ^\s*                            # start of string
            (?P<tag>\w+)\s+                 # macro tag
            (?P<type>[0-4])\s+              # macro type
            (?P<index>\d+)\s+               # macro index
            (?P<loop>\-?\d+)\s+             # macro loop
            (?P<release>\-?\d+)\s+          # macro release
            (?P<setting>\d+)\s*\:\s*        # macro setting
            (?P<sequence>\d+(?:\s+\-?\d+)*) # macro sequence
            $                               # end of string
            ''', re.VERBOSE
        )

    def handle(self, line: str):
        if x := self.pattern.match(line):
            # get macro tag (first word)
            m_tag = x.group('tag')
            
            # get space separated integers
            m_type, m_index, m_loop, m_release, m_setting = map(
                int, 
                x.group('type', 'index', 'loop', 'release', 'setting')
            )
            
            # get space separeted integer list after :
            m_sequence = list(map(
                int, 
                re.findall(r'(\-?\d+)', x.group(7))
            ))

            # create macro object
            m_object = Macro(
                m_tag,
                m_type,
                m_index,
                m_loop,
                m_release,
                m_setting, 
                m_sequence
            )

            # create macro key for lookup later
            # format: 'tag.type.index' (e.g. 'MACRO2A03.1.1')
            m_key = "{}.{}.{}".format(m_tag, m_type, m_index)

            # add it to project 
            self.project.macros[m_key] = m_object
        
        else:
            print("[WARN] Did not match! \'{}\'".format(line))


