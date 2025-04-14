# utils/regex_patterns.py

import re

class RegexPatterns:
    patterns = {
        # [TAG] "[TEXT]"
        "song_information"  : re.compile(r'''
            ^\s*
            (?P<field>\w+)\s+
            \"(?P<value>.*)\"
            .*$
            ''', re.VERBOSE
        ),
        # [TAG] [INTEGER]
        "global_settings"   : re.compile(r'''
            ^\s*
            (?P<field>\w+)\s+
            (?P<value>\d+)
            .*$
            ''', re.VERBOSE
        ),
        # MACRO [type] [index] [loop] [release] [setting] : [macro]
        "macro"             : re.compile(r'''
            ^\s*                                # start of string
            (?P<tag>\w+)\s+                     # macro tag
            (?P<type>[0-4])\s+                  # macro type
            (?P<index>\d+)\s+                   # macro index
            (?P<loop>\-?\d+)\s+                 # macro loop
            (?P<release>\-?\d+)\s+              # macro release
            (?P<setting>\-?\d+)\s*\:\s*         # macro setting
            (?P<sequence>\-?\d+(?:\s+\-?\d+)*)  # macro sequence
            .*$                                 # end of string
            ''', re.VERBOSE
        ),
        # DPCMDEF [index] [size] [name]
        "dpcm_def"          : re.compile(r'''
            ^\s*                # ignore leading whitespace
            (?P<tag>\w+)\s+     # grab the first word
            (?P<index>\d+)\s+   # grab the first number field
            (?P<size>\d+)\s*    # grab the second number field
            \"(?P<name>.*)\"    # grab the string between first and last quote
            .*$                 # ignore rest till end of the string
            ''', re.VERBOSE),
        # DPCM : [data]
        "dpcm"              : re.compile(r'''
            ^\s*            # optional leading whitespace
            (?P<tag>\w+)    # grab the first word
            \s*\:\s*        # div
            (?P<data>.*)    # grab the data
            $               # end of string
            ''', re.VERBOSE),
        # GROOVE [index] [sizeof] : [groove_sequence]
        "groove"            : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<index>\d+)
            \s+
            (?P<sizeof>\d+)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        ),
        # USEGROOVE : []
        "use_groove"        : re.compile(r'''
            #
            ''', re.VERBOSE
        ),
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] [name]
        "inst_2a03"         : re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<vol>\-?\d+)\s+
            (?P<arp>\-?\d+)\s+
            (?P<pit>\-?\d+)\s+
            (?P<hpi>\-?\d+)\s+
            (?P<dut>\-?\d+)\s+
            \"(?P<name>.*?)\"
            .*$
            ''', re.VERBOSE
        ),
        # INSTVRC7 [index] [patch] [r0] [r1] [r2] [r3] [r4] [r5] [r6] [r7] [name]
        "inst_vrc7"         : re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<patch>\d+)\s+
            (?P<r0>[0-9a-fA-F]{2})\s+
            (?P<r1>[0-9a-fA-F]{2})\s+
            (?P<r2>[0-9a-fA-F]{2})\s+
            (?P<r3>[0-9a-fA-F]{2})\s+
            (?P<r4>[0-9a-fA-F]{2})\s+
            (?P<r5>[0-9a-fA-F]{2})\s+
            (?P<r6>[0-9a-fA-F]{2})\s+
            (?P<r7>[0-9a-fA-F]{2})\s+
            \"(?P<name>.*?)\"
            .*$
            ''', re.VERBOSE
        ),
        # INSTFDS [index] [mod_enable] [mod_speed] [mod_depth] [mod_delay] [name]
        "inst_fds"          : re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<mod_enable>\d+)\s+
            (?P<mod_speed>\d+)\s+
            (?P<mod_depth>\d+)\s+
            (?P<mod_delay>\d+)\s+
            \"(?P<name>.*?)\"
            .*$
            ''', re.VERBOSE
        ),
        # INSTN163 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wav] [w_size] [w_pos] [w_count] [name]
        "inst_n163"         : re.compile(r'''
            ^\s*
            (?P<tag>\w+)\s+
            (?P<index>\d+)\s+
            (?P<vol>\-?\d+)\s+
            (?P<arp>\-?\d+)\s+
            (?P<pit>\-?\d+)\s+
            (?P<hpi>\-?\d+)\s+
            (?P<dut>\-?\d+)\s+
            (?P<w_size>\d+)\s+
            (?P<w_pos>\d+)\s+
            (?P<w_count>\d+)\s+
            \"(?P<name>.*)\"
            .*$
            ''', re.VERBOSE
        ),
        # KEYDPCM [inst] [octave] [note] [sample] [pitch] [loop] [loop_point] [delta]
        "key_dpcm"          : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst>\d+)
            \s+
            (?P<octave>\d+)
            \s+
            (?P<note>\d+)
            \s+
            (?P<sample>\d+)
            \s+
            (?P<pitch>\d+)
            \s+
            (?P<loop>\d+)
            \s+
            (?P<loop_point>\d+)
            \s+
            (?P<delta>\-?\d+)
            .*$
            ''', re.VERBOSE
        ),
        # FDSWAVE [inst] : [data]
        "fds_wave"          : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst_index>\d+)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        ),
        # FDSMOD [inst] : [data]
        "fds_mod"           : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst_index>\d+)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        ),
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        "fds_macro"         : re.compile(r'''
            ^\s*
            (?P<tag>\w+)       # tag
            \s+
            (?P<inst>\d+)       # inst
            \s+
            (?P<type>\d+)       # type
            \s+
            (?P<loop>\-?\d+)    # loop
            \s+
            (?P<release>\-?\d+)    # release
            \s+
            (?P<setting>\d+)       # setting
            \s*\:\s*
            (?P<data>.*)$       # data
            ''', re.VERBOSE         
        ),
        # N163WAVE [inst] [wave] : [data]
        "n163_wave"         : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<inst>\d+)
            \s+
            (?P<wave>\d+)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        ),
        # TRACK [pattern] [speed] [tempo] [name]
        "track"             : re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<pattern>\d+)
            \s+
            (?P<speed>\d+)
            \s+
            (?P<tempo>\d+)
            \s*\"
            (?P<name>.*)
            \".*$
            ''', re.VERBOSE
        ),
        # COLUMNS : [columns]
        "columns": re.compile(r'''
            ^\s*
            (?P<tag>COLUMNS)
            \s*\:\s*
            (?P<data>.*)
            $
            ''', re.VERBOSE
        ),
        # ORDER [frame] : [list]
        "order": re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<frame>[0-9a-fA-F]{2})
            \s*\:\s*
            (?P<list>.*)
            $
            ''', re.VERBOSE
        ),
        # PATTERN [pattern]
        "pattern": re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<pattern>[0-9a-fA-F]{2})
            .*$
            ''', re.VERBOSE
        ),
        # ROW [row] : [c0] : [c1] : [c2] ...
        "row": re.compile(r'''
            ^\s*
            (?P<tag>\w+)
            \s+
            (?P<row>[0-9a-fA-F]{2})
            \s*\:\s*
            (?P<data>.*)$
            ''', re.VERBOSE
        )
    }

