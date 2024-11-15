import sys

def find_offsets(haystack, needle):
    """
    Find the start of all (possibly-overlapping) instances of needle in haystack
    """
    offs = -1
    while True:
        offs = haystack.find(needle, offs+1)
        if offs == -1:
            break
        else:
            yield offs

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def replace_byte(filename, start_offset, end_offset, old_byte, new_byte):
    # Convert hex string to byte
    old_byte = bytes.fromhex(old_byte)
    new_byte = bytes.fromhex(new_byte)

    # Open the file in read+write binary mode
    with open(filename, "r+b") as file:
        # Read the content of the specified range
        file.seek(start_offset)
        data = file.read(end_offset - start_offset)

        #print(data.find(old_byte))

        for idx in find_all(data, old_byte):
            print(hex(start_offset + idx))

        # Replace occurrences of the old_byte with new_byte
        modified_data = data.replace(old_byte, new_byte)

        # Write the modified data back to the file
        file.seek(start_offset)
        file.write(modified_data)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: replacebyte.py <filename> <start_offset> <end_offset> <old_byte> <new_byte>")
        sys.exit(1)

    filename = sys.argv[1]
    start_offset = int(sys.argv[2], 16) if sys.argv[2].startswith("0x") else int(sys.argv[2])
    end_offset = int(sys.argv[3], 16) if sys.argv[3].startswith("0x") else int(sys.argv[3])
    old_byte = sys.argv[4]
    new_byte = sys.argv[5]

    replace_byte(filename, start_offset, end_offset, old_byte, new_byte)
