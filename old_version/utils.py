# utils.py

def note_str_to_int(self, token, transpose=0):
    if not self.regex_patterns["note_on"].match(token[0:3]):
        print("[E] Bad note format: {}".format(token))
        #return None

    note_int = self.note_mapping.get(token[0], 0)
    accidental = token[1]
    octave = int(token[2]) + 1

    midi_int = (octave * 12) + note_int + transpose
    midi_int = (midi_int + 1) if (accidental == "#") \
        else (midi_int - 1) if (accidental == "b") \
        else midi_int
    
    return midi_int

def get_next_item(self, lst: List[Any], item: Any):
    # returns next item of a list
    item_index = lst.index(item)
    next_index = (item_index + 1) % len(lst)
    return lst[next_index]

def int_to_hex(value: int) -> str:
    if not (0 <= value <= 255):
        raise ValueError("Input must be an integer between 0 and 255.")
    return f"0x{value:02X}"
