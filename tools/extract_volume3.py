import sys
from decompress import decompress_castle_data
from ega_render import ega_render

output_length = 0x7D00 # 32,000 bytes

input_filename = "working/VOLUME_3.CA1"

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def extract_volume3():
    # Skip the header data (0x14 + 0xE + 0x200 + 0x200)
    image_data_start = 0x422
    print(f"Image data start: 0x{image_data_start:02x}")

    # Decompress the data
    offset = image_data_start
    input_length = read_word(data, 8)
    bin_filename = f"extracted/volume3_castle_sprites/castle_items_images.bin"
    render_filename = "extracted/images/castle_items_images.png"
    decompress_castle_data(data[offset:offset+input_length], output_length, bin_filename)
    ega_render(bin_filename, render_filename)

    offset += input_length
    input_length = read_word(data, 10)
    bin_filename = f"extracted/volume3_castle_sprites/castle_structure_images.bin"
    render_filename = "extracted/images/castle_structure_images.png"
    decompress_castle_data(data[offset:offset+input_length], output_length, bin_filename)
    ega_render(bin_filename, render_filename)

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    extract_volume3()
