from util import read_word, write_word
from compress import compress_data

# We use the original file to get some header data
orig_filename = "orig/VOLUME_4.CA1"
output_filename = "working/VOLUME_4.CA1"

input_dir = "extracted/volume4_castles"

with open(orig_filename, "rb") as input_file:
    orig_data = input_file.read()

with open(output_filename, "w+b") as output_file:
    # Copy overall file header(s)
    file_header_length = 0xd0
    output_file.write(orig_data[0:file_header_length])

    # Copy first castle headers
    castle_start_loc = 0xd0
    castle_header_length = 0x14
    header1_count = read_word(orig_data, castle_start_loc + 0x0C)
    header2_count = read_word(orig_data, castle_start_loc + 0x0E)
    header3_count = read_word(orig_data, castle_start_loc + 0x10)
    print(f"Header counts: {header1_count}, {header2_count}, {header3_count}")

    total_header_length = castle_header_length + (header1_count * 0xE) + (header2_count * 4) + (header3_count * 4)
    print(f"Copying all castle headers ({total_header_length} bytes)")

    output_file.write(orig_data[castle_start_loc:castle_start_loc+total_header_length])

    # Copy first castle data
    castle_data_start = castle_start_loc + total_header_length
    castle_idx = 0
    castle_size_offset = 0x40 + (castle_idx * 6)
    
    # Castle items - includes gems, energy, decorations
    with open(f"{input_dir}/castle1_items.bin", "rb") as input_file:
        uncompressed_data = input_file.read()
    compressed_length = compress_data(uncompressed_data, output_file)
    print(f"Compressed length: {compressed_length}")
    # Write the compressed length to the header
    output_file.seek(castle_size_offset)
    output_file.write(write_word(compressed_length))
    output_file.seek(0, 2) # seek back to end

    # Castle structure - includes walls, floors
    with open(f"{input_dir}/castle1_structure.bin", "rb") as input_file:
        uncompressed_data = input_file.read()
    compressed_length = compress_data(uncompressed_data, output_file)
    print(f"Compressed length: {compressed_length}")
    # Write the compressed length to the header
    output_file.seek(castle_size_offset + 2)
    output_file.write(write_word(compressed_length))
    output_file.seek(0, 2) # seek back to end

    # Animation data and magic
    with open(f"{input_dir}/castle1_magic.bin", "rb") as input_file:
        uncompressed_data = input_file.read()
    compressed_length = compress_data(uncompressed_data, output_file)
    print(f"Compressed length: {compressed_length}")
    # Write the compressed length to the header
    output_file.seek(castle_size_offset + 4)
    output_file.write(write_word(compressed_length))
    output_file.seek(0, 2) # seek back to end
