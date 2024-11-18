import sys

# Modes
REPEAT_MODE = 1
COPY_MODE = 2

castle_num = int(sys.argv[1])

castle_offset = 0x0958 # Offset to first castle data - the rest follow contiguously
output_length = 0xAFC8 # for castle 1, or maybe all castles

input_filename = "working/VOLUME_4.CA1"

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def decompress_castle_data(data, output_length, output_filename):
    input_length = len(data)
    print(f"Decompressing {input_length} bytes to {output_length} bytes")

    input_idx = 0
    output_idx = 0
    mode = REPEAT_MODE

    # Open the output file in write binary mode
    with open(output_filename, "wb") as output_file:
        mode = data[input_idx]
        input_idx += 1

        while input_idx < input_length:
            # Check if we have reached the end of the compressed data
            if input_idx >= output_length:
                break
            
            # Check if we have reached the end of the output data
            if output_idx >= output_length:
                raise ValueError(f"Output length exceeded (only read %d of %d input bytes)" % (input_idx, input_length))

            # Read the next byte from the compressed data
            byte = data[input_idx]
            input_idx += 1

            if byte != 0:
                if mode == REPEAT_MODE:
                    # Repeat the byte N times
                    count = byte
                    byte = data[input_idx]
                    input_idx += 1
                    for _ in range(count):
                        output_file.write(bytes([byte]))
                        output_idx += 1
                elif mode == COPY_MODE:
                    # Copy N bytes from the compressed data
                    count = byte
                    for _ in range(count):
                        byte = data[input_idx]
                        input_idx += 1
                        output_file.write(bytes([byte]))
                        output_idx += 1
                else:
                    raise ValueError("Invalid mode: {}".format(mode))
            
            # Switch the mode
            mode = REPEAT_MODE if mode == COPY_MODE else COPY_MODE

        if output_idx != output_length:
            raise ValueError(f"Only wrote %d of %d expected output bytes)" % (output_idx, output_length))

        print("Extraction complete; wrote %d bytes to %s" % (output_idx, output_filename))

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
