import sys
from decompress import decompress_castle_data

castle_num = int(sys.argv[1])

output_length = 0xAFC8 # for castle 1, or maybe all castles

input_filename = "working/VOLUME_4.CA1"

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def extract_castle(castle_idx):
    castle_num = castle_idx + 1

    # Find castle data
    start_addr_loc = castle_idx * 4
    castle_start_loc = read_word(data, start_addr_loc)
    print(f"Reading castle data from 0x{castle_start_loc:02x}")

    # Read headers (just to get past them, don't know what they mean)
    castle_header_length = 0x14
    header1_count = read_word(data, castle_start_loc + 0x0C)
    header2_count = read_word(data, castle_start_loc + 0x0E)
    header3_count = read_word(data, castle_start_loc + 0x10)
    print(f"Header counts: {header1_count}, {header2_count}, {header3_count}")

    total_header_length = castle_header_length + (header1_count * 0xE) + (header2_count * 4) + (header3_count * 4)
    castle_data_start = castle_start_loc + total_header_length
    print(f"Castle data start: 0x{castle_data_start:02x}")

    #
    # Decompress the three parts
    #

    castle_size_offset = 0x40 + (castle_idx * 6)
    
    # Castle items - includes gems, energy, decorations
    items_offset = castle_data_start
    items_length = read_word(data, castle_size_offset)
    print(f"Items length: {items_length}")
    items_filename = f"extracted/castle{castle_num}_items.bin"
    decompress_castle_data(data[items_offset:items_offset+items_length], output_length, items_filename)

    # Castle structure - includes walls, floors
    structure_offset = items_offset + items_length
    structure_length = read_word(data, castle_size_offset + 2)
    structure_filename = f"extracted/castle{castle_num}_structure.bin"
    decompress_castle_data(data[structure_offset:structure_offset+structure_length], output_length, structure_filename)

    # Not sure what this one is yet
    unknown_offset = structure_offset + structure_length
    unknown_length = read_word(data, castle_size_offset + 4)
    unknown_filename = f"extracted/castle{castle_num}_unknown.bin"
    decompress_castle_data(data[unknown_offset:unknown_offset+unknown_length], output_length, unknown_filename)

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    extract_castle(castle_num-1)
