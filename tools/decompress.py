# Modes
REPEAT_MODE = 1
COPY_MODE = 2

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
                        # Check if we have reached the end of the output data
                        if output_idx >= output_length:
                            raise ValueError(f"Output length exceeded (only read %d of %d input bytes)" % (input_idx, input_length))
                                    
                        output_file.write(bytes([byte]))
                        output_idx += 1
                elif mode == COPY_MODE:
                    # Copy N bytes from the compressed data
                    count = byte
                    for _ in range(count):
                        if input_idx >= input_length:
                            raise ValueError(f"Input length overrun during copy (only wrote %d of %d output bytes)" % (output_idx, output_length))
                        if output_idx >= output_length:
                            raise ValueError(f"Output length exceeded (only read %d of %d input bytes)" % (input_idx, input_length))

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
