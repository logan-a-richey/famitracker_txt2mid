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
       
        # a sequence is defined by:
        # [int list] : [int list] : [int list]
        # [attack] : [sustain] : [release]
        # the `tick` is the index into the list.
        # macro_loop, macro_release determine where in the total sequence the loop and release starts.
        # assume there is no release (it is quite a rare feature to use in Famitracker)
        # if a sequence is 10 notes long and we have:
        # 1 2 3 : 4 5 6 : 7 8 9 0
        # macro_loop = 3
        # macro_release = 6
        # macro_loop and macro_release can be -1 if there is no loop or no release

#        self.seq_len = len(self.macro_sequence)
#
#        self.seq_att: List[int] = []
#        self.seq_sus: List[int] = []
#        self.seq_rel: List[int] = []
#        self.set_sub_sequences()
#
#    def set_sub_sequences(self):
#        #self.seq_att = self.macro_sequence[0: self.macro_loop]
#        #self.seq_sus = self.macro_sequence[self.macro_loop: self.macro_release]
#        #self.seq_rel = self.macro_sequence[self.macro_release:]
#        pass
#
#    def get_vol(self, value: int, tick: int):
#        if self.seq_len == 0:
#            return value
#
#        index = min(tick, self.seq_len - 1)
#        
#        return new_value
#
#    def get_pitch(self, value: int, tick: int):
#
#        return new_value



