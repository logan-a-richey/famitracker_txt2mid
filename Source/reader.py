# reader.py

import re

from singleton import singleton
from macro import Macro
from dpcm import DPCM
from groove import Groove
from instrument import Inst2a03, InstFds, InstVrc7, InstN163
from keydpcm import KeyDpcm
from track import Track

@singleton
class Reader:
    def __init__(self, project):
        self.project = project
        self.dispatch_table = {
            "TITLE": self._handle_song_information,
            "AUTHOR": self._handle_song_information,
            "COPYRIGHT": self._handle_song_information,
            "COMMENT": self._handle_song_information,
            
            "MACHINE": self._handle_global_settings,
            "FRAMERATE": self._handle_global_settings,
            "EXPANSION": self._handle_global_settings,
            "VIBRATO": self._handle_global_settings,
            "SPLIT": self._handle_global_settings,
            "N163CHANNELS": self._handle_global_settings,

            "MACRO": self._handle_macro,
            "MACROVRC6": self._handle_macrovrc6,
            "MACRON163": self._handle_macron163,
            "MACROS5B": self._handle_macros5b,
            
            "DPCMDEF": self._handle_dpcmdef,
            "DPCM": self._handle_dpcm,
            "GROOVE": self._handle_groove,
            "USEGROOVE": self._handle_usegroove,
            
            "INST2A03": self._handle_inst2a03,
            "INSTVRC6": self._handle_instvrc6,
            "INSTVRC7": self._handle_instvrc7,
            "INSTFDS": self._handle_instfds,
            "INSTN163": self._handle_instn163,
            "INSTS5B": self._handle_insts5b,
            
            "KEYDPCM": self._handle_keydpcm,
            "FDSWAVE": self._handle_fdswave,
            "FDSMOD": self._handle_fdsmod,
            "FDSMACRO": self._handle_fdsmacro,
            "N163WAVE": self._handle_n163wave,
            
            "TRACK": self._handle_track,
            "COLUMNS": self._handle_columns,
            "ORDER": self._handle_order,
            "PATTERN": self._handle_pattern,
            "ROW": self._handle_row
        }

    def get_quote(self, s):
        # return text between first and last double quote
        return s[s.find("\"") + 1: s.rfind("\"")]

    def _nop(self, line):
        pass

    def _handle_song_information(self, line):
        # [FIELD] [VALUE]
        k = line.split()[0]
        v = self.get_quote(line)
        self.project.song_information[k] = v

    def _handle_global_settings(self, line):
        # [FIELD] [VALUE]
        k = line.split()[0]
        v = int(line.split()[-1])
        self.project.global_settings[k] = v

    def _handle_macro(self, line, chip="blank"):
        # MACRO [type] [index] [loop] [release] [setting] : [macro]
        m_chip = chip
        m_type, m_index, m_loop, m_release, m_setting = map(int, line.split()[1:6])
        m_seq = list(map(int, line.split(":")[1].strip().split()))

        m_macro = Macro(m_chip, m_type, m_index, m_loop, m_release, m_setting, m_seq)
        m_key = "{}.{}.{}".format(m_chip, m_type, m_index)
        self.project.macros[m_key] = m_macro

    def _handle_macrovrc6(self, line):
        # MACROVRC6 [type] [index] [loop] [release] [setting] : [macro]
        self._handle_macro(line, chip="vrc6")

    def _handle_macron163(self, line):
        # MACRON163 [type] [index] [loop] [release] [setting] : [macro]
        self._handle_macro(line, chip="n163")

    def _handle_macros5b(self, line):
        # MACROS5B [type] [index] [loop] [release] [setting] : [macro]
        self._handle_macro(line, chip="s5b")

    def _handle_dpcmdef(self, line):
        # DPCMDEF [index] [size] [name]
        m_index, m_size = map(int, line.split()[1:3])
        m_name = self.get_quote(line)
        m_dpcm = DPCM(m_index, m_size, m_name)
        self.project.dpcm[m_index] = m_dpcm

        self.last_dpcm_index = m_index

    def _handle_dpcm(self, line):
        # DPCM : [data]
        
        # turn hex list into integer list
        data = list(map(lambda x: int(x, 16), line.split(":")[1].strip().split()))
        self.project.dpcm[self.last_dpcm_index].m_data.extend(data)

    def _handle_groove(self, line):
        # USEGROOVE : []
        m_index, m_sizeof = map(int, line.split()[1:3])
        m_seq = list(map(int, line.split(":")[1].split()))
        m_groove = Groove(m_index, m_sizeof, m_seq)
        self.project.grooves[m_index] = m_groove

    def _handle_usegroove(self, line):
        # USEGROOVE : []
        self.project.usegroove = list(map(int, line.split(":")[1].strip().split()))

    def _handle_inst2a03(self, line, chip="blank"):
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] [name]
        index, vol, arp, pit, hpi, dut = list(map(int, line.split()[1:7]))
        name = self.get_quote(line)
        chip = chip

        # create instrument object
        m_inst = Inst2a03(index, name, chip, vol, arp, pit, hpi, dut)
        
        # add macros to instrument if they exist
        params = [vol, arp, pit, hpi, dut]
        macro_types = ["vol", "arp", "pit", "hpi", "dut"]
        
        for i in range(5):
            macro_key = "{}.{}.{}".format(chip, i, params[i])
            macro_obj = self.project.macros.get(macro_key, None)
            if macro_obj:
                m_inst.macros[macro_types[i]] = macro_obj
        
        # add instrument to project instruments dictionary
        self.project.instruments[index] = m_inst

    def _handle_instvrc6(self, line):
        # INSTVRC6 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wid] [name]
        # note that width is the same as duty for 2a03.
        self._handle_inst2a03(line, chip="vrc6")

    def _handle_instvrc7(self, line):
        # INSTVRC7 [index] [patch] [r0] [r1] [r2] [r3] [r4] [r5] [r6] [r7] [name]
        index, patch = map(int, line.split()[1:3])
        registers = line.split()[3:11]
        name = self.get_quote(line)
        chip = "vrc7"

        m_inst = InstVrc7(index, name, chip, patch, registers)
        self.project.instruments[index] = m_inst

    def _handle_instfds(self, line):
        # INSTFDS [index] [mod_enable] [mod_speed] [mod_depth] [mod_delay] [name]
        index, mod_enable, mod_speed, mod_depth, mod_delay = map(int, line.split()[1:6])
        name = self.get_quote(line)
        chip = "fds"

        m_inst = InstFds(index, name, chip, mod_enable, mod_speed, mod_depth, mod_delay)
        self.project.instruments[index] = m_inst

    def _handle_instn163(self, line):
        # INSTN163 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wav] [w_size] [w_pos] [w_count] [name]
        # note that wave is the same as duty for 2a03. The wave data is defined later for the creation of custom waves.
        
        index, vol, arp, pit, hpi, dut, w_size, w_pos, w_count = list(map(int, line.split()[1:10]))
        name = self.get_quote(line)
        chip = "n163"

        # create instrument object
        m_inst = InstN163(index, name, chip, vol, arp, pit, hpi, dut, w_size, w_pos, w_count)
        
        # add macros to instrument if they exist
        params = [vol, arp, pit, hpi, dut]
        macro_types = ["vol", "arp", "pit", "hpi", "dut"]
        
        for i in range(5):
            macro_key = "{}.{}.{}".format(chip, i, params[i])
            macro_obj = self.project.macros.get(macro_key, None)
            if macro_obj:
                m_inst.macros[macro_types[i]] = macro_obj
        
        # add instrument to project instruments dictionary
        self.project.instruments[index] = m_inst

    def _handle_insts5b(self, line):
        # INSTS5B [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_ton] [name]
        # note that tone is the same as duty for 2a03.
        self._handle_inst2a03(line, chip="s5b")

    def _handle_keydpcm(self, line):
        # KEYDPCM [inst] [octave] [note] [sample] [pitch] [loop] [loop_point] [delta]
        inst, octave, note, sample, pitch, loop, loop_point, delta = map(int, line.split()[1:9])
        m_keydpcm = KeyDpcm(inst, octave, note, sample, pitch, loop, loop_point, delta)
        
        midi_pitch = (octave * 12) + note
        self.project.instruments[inst].dpcm_keys[midi_pitch] = m_keydpcm
        #print("{} -> {}".format(midi_pitch, m_keydpcm))

    def _handle_fdswave(self, line):
        # FDSWAVE [inst] : [data]
        inst = int(line.split()[1])
        data = list(map(int, line.split(":")[1].strip().split()))

        lookup = self.project.instruments.get(inst, None)
        if not lookup:
            return

        if isinstance(lookup, InstFds):
            lookup.fds_wave_data = data

    def _handle_fdsmod(self, line):
        # FDSMOD [inst] : [data]
        inst = int(line.split()[1])
        data = list(map(int, line.split(":")[1].strip().split()))

        lookup = self.project.instruments.get(inst, None)
        if not lookup:
            return
            
        if isinstance(lookup, InstFds):
            lookup.fds_mod_data = data

    def _handle_fdsmacro(self, line):
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        m_inst, m_type, m_loop, m_release, m_setting = \
            map(int, line.split()[1:6])
        m_seq = list(map(int, line.split(":")[1].strip().split()))

        m_macro = Macro(
            "fds", 
            m_type, 
            0,
            m_loop,
            m_release, 
            m_setting,
            m_seq
        )
         
        macro_types = ["vol", "arp", "pit", "hpi", "dut"]
        try:
            self.project.instruments[inst].macros[macro_types[m_type]] = m_macro
        except Exception as e:
            print("Failed to addd FDS Macro. Error: {}".format(e))
        
    def _handle_n163wave(self, line):
        # N163WAVE [inst] [wave] : [data]
        inst, wave = map(int, line.split()[1:3])
        data = list(map(int, line.split(":")[1].strip().split()))

        lookup = self.project.instruments.get(inst, None)
        if not lookup:
            return
        
        if isinstance(lookup, InstN163):
            lookup.waves[wave] = data            

    def _handle_track(self, line):
        # TRACK [pattern] [speed] [tempo] [name]
        num_rows, speed, tempo = map(int, line.split()[1:4])
        name = self.get_quote(line)

        m_track = Track(num_rows, speed, tempo, name)
        self.project.tracks.append(m_track)

    def _handle_columns(self, line):
        # COLUMNS : [columns]
        # get target track off of the top of the stack
        t = self.project.tracks[-1]
        
        eff_cols = list(map(int, line.split(":")[1].strip().split()))
        t.eff_cols = eff_cols
        t.num_cols = len(eff_cols)

    def _handle_order(self, line):
        # ORDER [frame] : [list]
        t = self.project.tracks[-1]
        
        k = line.split()[1]
        v = line.split(":")[1].strip().split()
        t.orders[k] = v

    # TODO
    def _handle_pattern(self, line):
        # PATTERN [pattern]
        pass

    # TODO
    def _handle_row(self, line):
        # ROW [row] : [c0] : [c1] : [c2] ...
        pass

    # TODO
    def _process_line(self, line):
        # Reads line from file.
        # Extracts and loads important data into the Project class.

        first_word = line.split()[0]
        func = self.dispatch_table.get(first_word, self._nop)
        func(line)

    def exec(self, input_file):
        # Reads Famitracker text export data line by line.
        # Calls _process_line to extract and load data into the Project class.
        
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line: 
                    continue
                if line.startswith("#"): 
                    continue
                self._process_line(line)

