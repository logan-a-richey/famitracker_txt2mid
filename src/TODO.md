# TODO
# Done
- debug macros and instruments with good testing
- handle the rest of the input file tags

## Reader
- handle track parsing

## Parser
- Use Dict[str, str] to store tokens directly in `class Track`
- Do order-pattern lookups as before with the addition of generating the `token_key`
- Handle echo buffer
- Create a poll of MIDI output events
- Handle Famitracker Ticks + Macros

## Exporter
- Loop over MIDI output events
- Handle the output file directories and output filename
- Import submodule and generate the midi

## Flask
- Create a WebGUI version of the application for ease of use
- Web-form to set output settings

## Finishing Touches
- Add good README.me
- Share to the world!

