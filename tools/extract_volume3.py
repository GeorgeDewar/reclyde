import sys
from decompress import decompress_castle_data

output_length = 0x7D00 # 32,000 bytes

input_filename = "working/VOLUME_3.CA1"

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def extract_volume3():
    # Skip the header data (0x14 + 0xE + 0x200 + 0x200)
    image_data_start = 0x422
    print(f"Image data start: 0x{image_data_start:02x}")

    # Decompress the data
    input_length = read_word(data, 8)
    output_filename = f"extracted/castle_images.bin"
    decompress_castle_data(data[image_data_start:image_data_start+input_length], output_length, output_filename)

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    extract_volume3()