import sys

# Modes
REPEAT_MODE = 1
COPY_MODE = 2

castle_offset = 0x1539
castle_length = 0x066D # Found at 0x42 in VOLUME_4.CA1
output_length = 0xAFC8 # stop with error if we exceed this length

input_filename = "working/VOLUME_4.CA1"
output_filename = "extracted/CASTLE_STR.DAT"

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    input_file.seek(castle_offset)
    data = input_file.read(castle_length)

    input_idx = 0
    output_idx = 0
    mode = REPEAT_MODE

    # Open the output file in write binary mode
    with open(output_filename, "wb") as output_file:
        mode = data[input_idx]
        input_idx += 1

        while input_idx < castle_length:
            # Check if we have reached the end of the compressed data
            if input_idx >= castle_length:
                break
            
            # Check if we have reached the end of the output data
            if output_idx >= output_length:
                raise ValueError(f"Output length exceeded (only read %d of %d input bytes)" % (input_idx, castle_length))

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