import sys
from decompress import decompress_castle_data

output_length = 0x7D00 # 32,000 bytes

input_filename = "working/VOLUME_5.CA1"

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def extract_volume5():
    # Skip the header data (0x16 + 0xE + 0x200 + 0x200)
    image_data_start = read_word(data, 0)
    print(f"Image data start: 0x{image_data_start:02x}")

    # Decompress the data
    offset = image_data_start
    input_length = read_word(data, 0xC)
    output_filename = f"extracted/castle_background1.bin"
    decompress_castle_data(data[offset:offset+input_length], output_length, output_filename)

    offset = offset + input_length
    input_length = read_word(data, 0xE)
    output_filename = f"extracted/castle_background2.bin"
    decompress_castle_data(data[offset:offset+input_length], output_length, output_filename)

    offset = offset + input_length
    input_length = read_word(data, 0x10)
    output_filename = f"extracted/castle_background3.bin"
    decompress_castle_data(data[offset:offset+input_length], output_length, output_filename)

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    extract_volume5()
