# Partial reverse-engineering of Clyde's Adventure

## Contents

- orig: original game files
- working: modified game files will be stored here (untracked)
- IDA: a disassembly project in IDA 5.0
- tmp: a place to put logs, etc
- extracted: castle data, assets, etc
- disassembly: disassembled representation of the game executable
- hex: hex dumps of the game data files (for easy searching in an IDE)

## Why?

No reason really. It's fun.

## Initial goal (mostly complete)

Decode the data files well enough to be able to produce a static image mapping each level.

### Status

- Reverse-engineered the compression algorithm (run-length-encoding based)
- Reverse-engineered the castle format (three "files" per castle, each with one byte per cell)
- Worked out how to decode the image format (EGA)
- extract_castle.py can extract the first six castles
- extract_volume3.py can extract the castle structure and item sprites
    - splitImages.py can split this into the individual sprites
- extract_volume5.py can extract the background imagery
- extract_volume6.py can extract the playing instructions imagery

## Documentation

### Data files

Filename     | Contents
------------ | --------
VOLUME_1.CA1 | Save data
VOLUME_2.CA1 | Character sprites
VOLUME_3.CA1 | Castle sprites - structure (e.g. walls) and items (e.g. gems)
VOLUME_4.CA1 | Castle data - three compressed files per castle
VOLUME_5.CA1 | Background images
VOLUME_6.CA1 | Playing instructions images
