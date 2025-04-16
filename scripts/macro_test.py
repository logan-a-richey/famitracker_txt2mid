#!/usr/bin/env python3
# macro_test.py

class Macro:
    def __init__(self, sequence_attack, sequence_loop, sequence_release):
        self.sequence_attack = sequence_attack
        self.sequence_loop = sequence_loop
        self.sequence_release = sequence_release

    def get_value(self, tick: int, release_tick: int):
        # If release_tick is 0, we go to the release sequence
        if release_tick == 0 and self.sequence_release:
            # Index into release sequence starting from the beginning
            return self.sequence_release[tick % len(self.sequence_release)] if len(self.sequence_release) > 0 else 0
        
        # Otherwise, we process attack and loop sequences
        if self.sequence_attack:
            # If we're still in the attack sequence
            if tick < len(self.sequence_attack):
                return self.sequence_attack[tick]
            else:
                # After the attack sequence is finished, we loop through the loop sequence
                if self.sequence_loop:
                    return self.sequence_loop[(tick - len(self.sequence_attack)) % len(self.sequence_loop)]
                else:
                    # No loop sequence, return the last value from the attack sequence
                    return self.sequence_attack[-1]
        
        # If no attack sequence exists, we only have the loop sequence to consider
        if self.sequence_loop:
            return self.sequence_loop[tick % len(self.sequence_loop)] if len(self.sequence_loop) > 0 else 0
        
        # If no sequences exist, just return a default value (or could raise an error)
        return 0

def main():
    # Define sequences
    seq_attack = [num for num in range(5)]  # Attack sequence
    seq_loop = [num + 10 for num in range(5)]  # Loop sequence
    seq_release = [num + 20 for num in range(5)]  # Release sequence
    
    # Create macros with different combinations of sequences
    m0 = Macro(seq_attack, seq_loop, seq_release)
    m1 = Macro(seq_attack, [], seq_release)  # Only attack, no loop
    m2 = Macro([], seq_loop, seq_release)  # Only loop, no attack
    m3 = Macro([], [], seq_release)  # Only release
    m4 = Macro([], [], [])  # No sequences

    macros = [m0, m1, m2, m3, m4]
    data = []
    
    release_tick = -1  # Can be toggled to simulate a release event
    
    for macro_number, macro in enumerate(macros):
        data.clear()
        print(f"Macro {macro_number}")
        for tick in range(30):
            # Simulate release_tick by toggling it at some point
            if tick == 15:
                release_tick = 0  # Trigger release at tick 15
            elif tick == 20:
                release_tick = -1  # End release after tick 20
            
            # Get value from macro
            value = macro.get_value(tick, release_tick)
            data.append(value)
        print(data)

if __name__ == "__main__":
    main()
