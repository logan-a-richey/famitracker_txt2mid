# conatiners/macro.py

from typing import List
from utils.printable import Printable

class Macro(Printable):
    def __init__(
        self, 
        macro_tag: str, 
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
        
        self.loop = macro_loop
        self.release = macro_release
        self.setting = macro_setting
        self.sequence = macro_sequence
        
        self.arp_formulas = {
            0: self.arp_absolute_formula,
            2: self.arp_relative_formula,
            3: self.arp_fixed_formula,
            4: self.arp_scheme_formula
        }

    # =========================================================================
    
    def volume_formula(self, value, macro_value) -> int:
        return int(value * (macro_value / 16))

    def arp_absolute_formula(self, value, macro_value) -> int:
        return value + macro_value

    def arp_fixed_formula(self, value, macro_value) -> int:
        return macro_value

    def arp_relative_formula(self, value, macro_value) -> int:
        # TODO : need to study the format
        return value + macro_value

    def arp_scheme_formula(self, value, macro_value) -> int:
        # TODO : need to study the format
        return value + macro_value
    
    # =========================================================================
    
    def get_volume_value(self, value: int, tick: int, release_tick: int) -> int:
        ''' Returns new volume. Assumes that `value` is an integer between 0-15'''
        
        if value < 0 or value > 15:
            raise ValueError("Volume value should be between 0 and 15. You used {}".format(value))

        if len(self.sequence) == 0:
            return value

        # If release_tick is >= 0, handle release logic
        if release_tick != -1:
            if self.release == -1:
                # No release, return the last value of the sequence
                macro_value = self.sequence[-1]
                return self.volume_formula(value, macro_value)

            # Release sequence is defined, calculate the index within the release range
            index = min(self.release + release_tick, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return self.volume_formula(value, macro_value)

        # If no release_tick, handle the loop and normal sequence logic
        if self.loop != -1:
            # The loop starts at `self.loop` and ends at `self.release` (or the end of sequence if no release)
            loop_end = self.release if self.release != -1 else len(self.sequence) - 1
            
            # TODO : check off by 1 offset?
            # loop_range = loop_end - self.loop + 1
            loop_range = loop_end - self.loop

            # Loop index calculation, using modulo to wrap around
            index = (tick - self.loop) % loop_range + self.loop
            index = min(index, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return self.volume_formula(value, macro_value)

        # If no loop, just return the value at the tick
        return value

    def get_arpeggio_value(self, value: int, tick: int, release_tick: int) -> int:
        ''' Returns new pitch. Assumes value can be any integer 0-127 '''
        
        if value < 0 or value > 127:
            raise ValueError("Volume value should be between 0 and 127. You used {}".format(value))

        # Default to arp_absolute_formula if setting is invalid
        my_formula = self.arp_formulas.get(self.setting, self.arp_absolute_formula)
        
        if len(self.sequence) == 0:
            return value

        # If release_tick is >= 0, handle release logic
        if release_tick != -1:
            if self.release == -1:
                # No release, return the last value of the sequence
                macro_value = self.sequence[-1]
                return my_formula(value, macro_value)

            # Release sequence is defined, calculate the index within the release range
            index = min(self.release + release_tick, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return my_formula(value, macro_value)

        # If no release_tick, handle the loop and normal sequence logic
        if self.loop != -1:
            # The loop starts at `self.loop` and ends at `self.release` (or the end of sequence if no release)
            loop_end = self.release if self.release != -1 else len(self.sequence) - 1
            
            # TODO : check off by 1 offset?
            # loop_range = loop_end - self.loop + 1
            loop_range = loop_end - self.loop
            
            # Loop index calculation, using modulo to wrap around
            index = (tick - self.loop) % loop_range + self.loop
            index = min(index, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return my_formula(value, macro_value)
        
        return value




