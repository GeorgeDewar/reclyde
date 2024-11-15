# Partial reverse-engineering of Clyde's Adventure

- orig: original game files
- working: modified game files will be stored here (untracked)
- IDA: a disassembly project in IDA 5.0
- tmp: a place to put logs, etc
- extracted: castle data, assets, etc
- disassembly: disassembled representation of the game executable
- hex: hex dumps of the game data files (for easy searching in an IDE)

## Why?

No reason really. It's fun.

## Initial goal

Decode the data files well enough to be able to produce a static image mapping each level.

### Status

- Reverse-engineered the compression algorithm (run-length-encoding based); extract-castle.py can extract the first castle
- Identified some of the features of the castle data (e.g. 0x3B is a gem)
