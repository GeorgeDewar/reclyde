# Modes
REPEAT_MODE = 1
COPY_MODE = 2

def compress_data(data, output_stream):
    input_length = len(data)
    print(f"Compressing {input_length} bytes")

    input_idx = 0
    output_idx = 0
    mode = COPY_MODE

    # The first byte specifies the initial mode
    output_stream.write(bytes([mode]))
    output_idx += 1

    # Calculate the number of 255-bytes copies, and the remainder
    full_copies = input_length // 255
    remainder = input_length - full_copies * 255
    print(f"Writing {full_copies} x 255 bytes, and 1 x {remainder} bytes")

    for i in range(full_copies):
        print(f"Writing 255 bytes")
        output_stream.write(bytes([0xFF])) # Copy of 255 bytes
        output_idx += 1
        output_stream.write(data[input_idx:input_idx+255])
        input_idx += 255
        output_idx += 255
        output_stream.write(bytes([0])) # Keep the mode the same
        output_idx += 1

    print(f"Writing final {remainder} bytes")
    output_stream.write(bytes([remainder])) # Copy of [remainder] bytes
    output_idx += 1
    output_stream.write(data[input_idx:input_idx+remainder])
    input_idx += remainder
    output_idx += remainder

    return output_idx

