# utils/regex_patterns.py

import re

class RegexPatterns:
    """Regex patterns for parsing module data formats."""
    patterns = {
        # TITLE "[TEXT]"
        "song_information": re.compile(r'^\s*(?P<field>\w+)\s+\"(?P<value>.*)\".*$'),
        
        # MACHINE [INTEGER]
        "global_settings": re.compile(r'^\s*(?P<field>\w+)\s+(?P<value>\d+).*$'),
        
        # MACRO [type] [index] [loop] [release] [setting] : [macro]
        "macro": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<type>[0-4])\s+(?P<index>\d+)\s+(?P<loop>\-?\d+)\s+(?P<release>\-?\d+)\s+(?P<setting>\-?\d+)\s*\:\s*(?P<sequence>\-?\d+(?:\s+\-?\d+)*).*$'),
        
        # DPCMDEF [index] [size] "[name]"
        "dpcm_def": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<size>\d+)\s*\"(?P<name>.*)\".*$'),

        # DPCM : [data]
        "dpcm": re.compile(r'^\s*(?P<tag>\w+)\s*\:\s*(?P<data>.*)$'),
        
        # GROOVE [index] [sizeof] : [groove_sequence]
        "groove": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<sizeof>\d+)\s*\:\s*(?P<data>.*)$'),
        
        # USEGROOVE : []
        "use_groove": re.compile(r'^\s*(?P<tag>\w+)\s*\:\s*(?P<data>.*)$'),
        
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] "[name]"
        "inst_2a03": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<vol>\-?\d+)\s+(?P<arp>\-?\d+)\s+(?P<pit>\-?\d+)\s+(?P<hpi>\-?\d+)\s+(?P<dut>\-?\d+)\s+\"(?P<name>.*?)\".*$'),
        
        # INSTVRC7 [index] [patch] [r0] [r1] [r2] [r3] [r4] [r5] [r6] [r7] "[name]"
        "inst_vrc7": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<patch>\d+)\s+(?P<r0>[0-9a-fA-F]{2})\s+(?P<r1>[0-9a-fA-F]{2})\s+(?P<r2>[0-9a-fA-F]{2})\s+(?P<r3>[0-9a-fA-F]{2})\s+(?P<r4>[0-9a-fA-F]{2})\s+(?P<r5>[0-9a-fA-F]{2})\s+(?P<r6>[0-9a-fA-F]{2})\s+(?P<r7>[0-9a-fA-F]{2})\s+\"(?P<name>.*?)\".*$'),
        
        # INSTFDS [index] [mod_enable] [mod_speed] [mod_depth] [mod_delay] "[name]"
        "inst_fds": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<mod_enable>\d+)\s+(?P<mod_speed>\d+)\s+(?P<mod_depth>\d+)\s+(?P<mod_delay>\d+)\s+\"(?P<name>.*?)\".*$'),
        
        # INSTN163 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wav] [w_size] [w_pos] [w_count] "[name]"
        "inst_n163": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<index>\d+)\s+(?P<vol>\-?\d+)\s+(?P<arp>\-?\d+)\s+(?P<pit>\-?\d+)\s+(?P<hpi>\-?\d+)\s+(?P<dut>\-?\d+)\s+(?P<w_size>\d+)\s+(?P<w_pos>\d+)\s+(?P<w_count>\d+)\s+\"(?P<name>.*)\".*$'),

        # KEYDPCM [inst] [octave] [note] [sample] [pitch] [loop] [loop_point] [delta]
        "key_dpcm": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<inst>\d+)\s+(?P<octave>\d+)\s+(?P<note>\d+)\s+(?P<sample>\d+)\s+(?P<pitch>\d+)\s+(?P<loop>\d+)\s+(?P<loop_point>\d+)\s+(?P<delta>\-?\d+).*$'),
        
        # FDSWAVE [inst] : [data]
        "fds_wave": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<inst_index>\d+)\s*\:\s*(?P<data>.*)$'),
        
        # FDSMOD [inst] : [data]
        "fds_mod": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<inst_index>\d+)\s*\:\s*(?P<data>.*)$'),
        
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        "fds_macro": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<inst>\d+)\s+(?P<type>\d+)\s+(?P<loop>\-?\d+)\s+(?P<release>\-?\d+)\s+(?P<setting>\d+)\s*\:\s*(?P<data>.*)$'),
        
        # N163WAVE [inst] [wave] : [data]
        "n163_wave": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<inst>\d+)\s+(?P<wave>\d+)\s*\:\s*(?P<data>.*)$'),
        
        # TRACK [pattern] [speed] [tempo] "[name]"
        "track": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<pattern>\d+)\s+(?P<speed>\d+)\s+(?P<tempo>\d+)\s*\"(?P<name>.*)\".*$'),
        
        # COLUMNS : [columns]
        "columns": re.compile(r'^\s*(?P<tag>COLUMNS)\s*\:\s*(?P<data>.*)$'),
        
        # ORDER [frame] : [list]
        "order": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<frame>[0-9a-fA-F]{2})\s*\:\s*(?P<list>.*)$'),
        
        # PATTERN [pattern]
        "pattern": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<pattern>[0-9a-fA-F]{2}).*$'),
        
        # ROW [row] : [c0] : [c1] : [c2] ...
        "row": re.compile(r'^\s*(?P<tag>\w+)\s+(?P<row>[0-9a-fA-F]{2})\s*\:\s*(?P<data>.*)$')
    }

