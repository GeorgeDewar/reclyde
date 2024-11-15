import sys

input_filename = sys.argv[1]
#output_filename = "CASTLE_RENDER.HEX"

width=250
height=180
data_len = width * height

with open(input_filename, "rb") as input_file:
    # Read the castle data
    data = input_file.read()
    input_idx = 0

    while input_idx < data_len:
        byte = data[input_idx]
        input_idx += 1

        if byte > 1:
            print(f"{byte:02X} ", end="")
        else:
            print("   ", end="")

        if input_idx % width == 0:
            print("")
        