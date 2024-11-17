import sys

# Modes
REPEAT_MODE = 1
COPY_MODE = 2

castle_num = sys.argv[1]

castle_offset = 0x0958 # Offset to first castle data - the rest follow contiguously
output_length = 0xAFC8 # for castle 1, or maybe all castles

input_filename = "working/VOLUME_4.CA1"

def decompress_castle(data, output_length, output_filename):
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

        print("Extraction complete; wrote %d bytes to %s" % (output_idx, output_filename))

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    # Castle items - includes gems, energy, decorations
    items_offset = castle_offset
    items_length = int.from_bytes(data[0x40:0x42], 'little')
    items_filename = f"extracted/castle{castle_num}_items.bin"
    decompress_castle(data[items_offset:items_offset+items_length], output_length, items_filename)

    # Castle structure - includes walls, floors
    structure_offset = castle_offset + items_length
    structure_length = int.from_bytes(data[0x42:0x44], 'little')
    structure_filename = f"extracted/castle{castle_num}_structure.bin"
    decompress_castle(data[structure_offset:structure_offset+structure_length], output_length, structure_filename)

    # Not sure what this one is yet
    unknown_offset = structure_offset + structure_length
    unknown_length = int.from_bytes(data[0x44:0x46], 'little')
    unknown_filename = f"extracted/castle{castle_num}_unknown.bin"
    decompress_castle(data[unknown_offset:unknown_offset+unknown_length], output_length, unknown_filename)
