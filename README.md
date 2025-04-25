# famitracker_txt2mid
- Famitracker is a popular tool for creating authentic NES-style music. Famitracker contains an option for text export.
- This is a tool for converting FamiTracker text exports into MIDI files, enabling integration with modern music production workflows and tools.
- Significantly reduces music production and transcription time while using Famitracker.
- I created this project as a way to deepen my understanding of Python. Over the course of several iterations, I explored different architectural approaches — including a version that relied heavily on design patterns and inheritance. Ultimately, I found that a simpler, more pragmatic approach yielded better results and was easier to work with. Sometimes, simpler is better.

---

## Overview

- `famitracker_txt2mid` is a Python-based CLI tool designed to parse and interpret FamiTracker `.txt` exports and convert them into usable MIDI files.
- It supports many key FamiTracker features and is designed with extensibility and future upgrades (GUI, C++ backend, advanced MIDI mapping) in mind.

---

## Table of Contents

- [Features](#features)
- [Planned Features](#planned-features)
- [Installation](#installation)
  - [Python Version](#python-version)
  - [C++ Version (Coming Soon)](#c-version-coming-soon)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Python CLI tool to convert `.txt` exports from FamiTracker to `.mid` files.
- Parses key elements like patterns, notes, instruments, and effects
- Built with extensibility in mind — ideal for musicians and developers alike
- Lightweight and dependency-minimal
- I created a script called `run_all.sh` which recursively runs all of my input test files. Doing this revealed the program can generate 200 midi files in less then 10 seconds. Further optimizations in Python and implementations in C++ will further increase the performance.

---

## Planned Features

- Flask GUI interface for drag-and-drop file conversion
- C++ backend for faster processing of large files and integration with DAWs
- Smart Drum Mapping:
  - Auto-detect drum patterns based on instrument names (e.g. "kick", "snare")
  - Map patterns to General MIDI drum keys
- Support for Gxx and Sxx FamiTracker effects (note delay/offset)

---

## Installation

### Python Version

1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/famitracker_txt2mid.git
   cd famitracker_txt2mid
   ```

2. (Optional) Create a virtual environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Set PYTHONPATH:
- `cd` to famitracker_ftm2mid/python_version
- get path using `pwd`, copy this path
- set environment variable `PYTHONPATH=<path>` (paste the python_version path)

5. Run the tool  
   ```bash
   cd src
   ./main.py path/to/input.txt
   ```

---

### C++ Version (Coming Soon)

1. Build using:
   ```bash
   make
   ```

2. Run:
   ```bash
   ./main path/to/input.txt
   ```

---

## Usage

```bash
./main.py <input.txt>
```

An output midi file is automatically created in an `exports/` directory at the same level the script is run.

---

## Contributing

Bug reports, feature requests, and pull requests are all appreciated.

---

## License

MIT License — see `LICENSE.md` for details.

