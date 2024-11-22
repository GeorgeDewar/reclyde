import sys
from decompress import decompress_castle_data
from ega_render import ega_render

input_filename = "working/VOLUME_6.CA1"
output_length = 0x7D00 # 45,000 bytes

def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def extract_image(name, input_length):
    global offset
    bin_filename = f"extracted/volume6_playing_instructions/{name}.bin"
    render_filename = f"extracted/images/{name}.png"
    decompress_castle_data(data[offset:offset+input_length], output_length, bin_filename)
    ega_render(bin_filename, render_filename)
    offset = offset + input_length

def extract_volume6():
    global offset

    # Skip the header data (0x16)
    image_data_start = read_word(data, 4)
    print(f"Image data start: 0x{image_data_start:02x}")

    # Decompress the data
    offset = image_data_start

    for i in range(11):
        extract_image(f"volume6_{i+1:02}", read_word(data, 0x72 + 2*i))

with open(input_filename, "rb") as input_file:
    # Read the compressed castle data
    data = input_file.read()

    extract_volume6()
