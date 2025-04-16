#!/usr/bin/env python3
# macro_test.py

class Macro:
    def __init__(self, loop, release, setting, sequence):
        self.loop = loop
        self.release = release  # e.g. 3
        self.setting = setting  # e.g. 7
        self.sequence = sequence  # e.g. [1, 2, 3, 4, 5 ... 10]
    
    # =========================================================================
    
    def volume_formula(self, value, macro_value) -> int:
        return int(value * (macro_value / 16))

    def arp_absolute_formula(self, value, macro_value) -> int:
        return value + macro_value

    def arp_fixed_formula(self, value, macro_value) -> int:
        return macro_value

    def arp_relative_formula(self, value, macro_value) -> int:
        # TODO : relative returns all of the previous macro values including the current macro index summed
        return value + macro_value

    def arp_scheme_formula(self, value, macro_value) -> int:
        # TODO: Implement once I study the format
        return value + macro_value

    # =========================================================================

    def get_volume_value(self, value: int, tick: int, release_tick: int) -> int:
        ''' Returns new volume. Assumes that `value` is an integer between 0-15'''

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
            loop_range = loop_end - self.loop + 1  # Loop length

            # Loop index calculation, using modulo to wrap around
            index = (tick - self.loop) % loop_range + self.loop
            index = min(index, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return self.volume_formula(value, macro_value)

        # If no loop, just return the value at the tick
        return value

    def get_arpeggio_value(self, value: int, tick: int, release_tick: int) -> int:
        ''' Returns new pitch. Assumes value can be any integer 0-127 '''

        arp_formulas = {
            0: self.arp_absolute_formula,
            2: self.arp_relative_formula,
            3: self.arp_fixed_formula,
            4: self.arp_scheme_formula
        }
        
        # Default to arp_absolute_formula if setting is invalid
        my_formula = arp_formulas.get(self.setting, self.arp_absolute_formula)
        
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
            loop_range = loop_end - self.loop + 1  # Loop length

            # Loop index calculation, using modulo to wrap around
            index = (tick - self.loop) % loop_range + self.loop
            index = min(index, len(self.sequence) - 1)
            macro_value = self.sequence[index]
            return my_formula(value, macro_value)
        
        return value

if __name__ == "__main__":
    # Example sequences
    seq = [i for i in range(10)]  # Sequence: [0, 1, 2, ..., 9]
    
    # Create a Macro with loop, release, and setting values
    m = Macro(loop=3, release=7, setting=2, sequence=seq)
    
    # Test with various ticks and release_ticks
    data = []
    for tick in range(30):
        release_tick = -1 if tick < 15 else 0  # Trigger release at tick 15
        value = m.get_volume_value(100, tick, release_tick)
        data.append(value)

    print(data)

