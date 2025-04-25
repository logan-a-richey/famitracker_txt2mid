# FamiTracker Text Export Specification
This document describes the format for importing and exporting song data from FamiTracker using its text representation. Lines beginning with `#` or blank lines are ignored.

---

## Table of Contents

- [Metadata](#metadata)
- [Global Settings](#global-settings)
- [Macros](#macros)
- [DPCM](#dpcm)
- [Grooves](#grooves)
- [Instruments](#instruments)
- [Track Data](#track-data)

---

## Metadata

| Tag         | Description             | Format               |
|-------------|-------------------------|----------------------|
| `TITLE`     | Document title          | `TITLE [string]`     |
| `AUTHOR`    | Author of the document  | `AUTHOR [string]`    |
| `COPYRIGHT` | Copyright notice        | `COPYRIGHT [string]` |
| `COMMENT`   | Arbitrary comment line  | `COMMENT [string]`   |

---

## Global Settings

| Tag          | Description                                  | Format |
|---------------|----------------------------------------------|--------|
| `MACHINE`     | 0 = NTSC, 1 = PAL                            | `MACHINE [0|1]` |
| `FRAMERATE`   | Music frame rate (0 = machine default)       | `FRAMERATE [0-800]` |
| `EXPANSION`   | Bitfield for expansion chips used            | `EXPANSION [0-255]` |
| `VIBRATO`     | 0 = old style, 1 = new style                 | `VIBRATO [0|1]` |
| `SPLIT`       | Fxx effect switch point                      | `SPLIT [0-255]` |
| `N163CHANNELS`| Number of Namco 163 channels used            | `N163CHANNELS [1-8]` |

### Note about Expansion:
- the value of EXPANSION is an integer representing a bitfield of the chips used:
- 1=VRC6, 2=VRC7, 4=FDS, 8=MMC5, 16=N163, 32=S5B
- example: 17 -> 010001 -> "use VRC6 and N163"

---

## Macros

### Common Macro Format

```plaintext
MACRO [type] [index] [loop] [release] [setting] : [macro]
```

| Type     | Description       |
|----------|-------------------|
| 0        | Volume            |
| 1        | Arpeggio          |
| 2        | Pitch             |
| 3        | Hi-pitch          |
| 4        | Type-specific (e.g., Duty/Pulse/Wave) |

Each expansion chip uses its own macro command:

- `MACRO` - 2A03
- `MACROVRC6` - VRC6
- `MACRON163` - N163
- `MACROS5B` - S5B

---

## DPCM

| Tag        | Description |
|------------|-------------|
| `DPCMDEF`  | Defines DPCM sample (index, size, name) |
| `DPCM`     | Fills sample data in hex (`00` to `FF`) |

---

## Grooves

| Tag        | Description |
|------------|-------------|
| `GROOVE`   | Defines a groove pattern, a speed sequence |
| `USEGROOVE`| Lists tracks using the default groove      |

---

## Instruments

### 2A03

```plaintext
INST2A03 [index] [vol] [arp] [pit] [hpi] [dut] [name]
```

### VRC6

```plaintext
INSTVRC6 [index] [vol] [arp] [pit] [hpi] [wid] [name]
```

### VRC7

```plaintext
INSTVRC7 [index] [patch] [r0-r7] [name]
```

### FDS

```plaintext
INSTFDS [index] [mod_enable] [speed] [depth] [delay] [name]
FDSWAVE [inst] : [64 values]
FDSMOD [inst] : [32 values]
FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
```

### N163

```plaintext
INSTN163 [index] [vol] [arp] [pit] [hpi] [wav] [size] [pos] [count] [name]
N163WAVE [inst] [wave] : [data]
```

### S5B

```plaintext
INSTS5B [index] [vol] [arp] [pit] [hpi] [ton] [name]
```

### DPCM Key Mapping

```plaintext
KEYDPCM [inst] [oct] [note] [sample] [pitch] [loop] [loop_point] [delta]
```

---

## Track Data

| Tag       | Description |
|-----------|-------------|
| `TRACK`   | Starts a track (`pattern` length, speed, tempo, name) |
| `COLUMNS` | Sets the number of effect columns per channel         |
| `ORDER`   | Pattern order list per frame                          |
| `PATTERN` | Selects current pattern to write to                   |
| `ROW`     | Adds note data per channel per row                   |

### Row Data Format

```plaintext
ROW [row_index] : [c0_data] : [c1_data] : ...
```

Each channel's data format:

```
nnn ii v eee ...
```

- `nnn`: Note (`C#4`, `---`, `===`, `...`)
- `ii`: Instrument (`00`–`3F`, `..` = none)
- `v`: Volume (`0`–`F`, `..` = none)
- `eee`: Effect (e.g., `F04`, `1xx`, etc.)

For the noise channel (c3), notes begin with a hex pitch (`0`–`F`) followed by `-#`.
There are as many [eee] effects as designated by the COLUMNS tag.
The number of effects in this column is determined by the value at the corresponding index in the `eff_cols` list.

---

## Notes

- `:`, `-`, and spaces are meaningful—do not remove or replace unless parsing accordingly.
- Lists of numbers are often comma- or space-separated, and some blocks allow multiple entries.

---

## Contributing

Please update this spec in tandem with any parser or format updates to maintain consistency.

```

