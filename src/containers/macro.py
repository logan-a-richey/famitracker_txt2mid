# conatiners/macro.py

from typing import List
from utils.printable import Printable

class Macro(Printable):
    def __init__(
        self, 
        macro_tag: int, 
        macro_type: int, 
        macro_index: int, 
        macro_loop: int, 
        macro_release: int, 
        macro_setting: int, 
        macro_sequence: List[int]
    ):
        self.macro_tag = macro_tag
        self.macro_type = macro_type
        self.macro_index = macro_index
        self.macro_loop = macro_loop
        self.macro_release = macro_release
        self.macro_setting = macro_setting
        self.macro_sequence = macro_sequence



