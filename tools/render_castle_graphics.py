import sys
import numpy as np
import cv2

MAGIC_NONE = 0x00
MAGIC_ANIM1 = 0x03
MAGIC_ANIM2 = 0x61

castle_num = sys.argv[1]
castle_structure_filename = f"extracted/castle{castle_num}_structure.bin"
castle_items_filename = f"extracted/castle{castle_num}_items.bin"
castle_magic_filename = f"extracted/castle{castle_num}_unknown.bin"
output_filename = f"render/castle{castle_num}.png"

# Dimensions of the castle in blocks
blocks_width=250
blocks_height=180
blocks_len = blocks_width * blocks_height

# Size of a block in pixels
block_width=16
block_height=16

structure = {}
for i in range(240):
    structure[i] = cv2.imread(f"extracted/images/structure/{i:02x}.png")

items = {}
for i in range(240):
    items[i] = cv2.imread(f"extracted/images/items/{i:02x}.png")

# Read the castle data
with open(castle_structure_filename, "rb") as structure_file:
    structure_data = structure_file.read()
with open(castle_items_filename, "rb") as items_file:
    items_data = items_file.read()
with open(castle_magic_filename, "rb") as magic_file:
    magic_data = magic_file.read()

# Keep track of where we are - same index for all three files
input_idx = 0

# create the data behind our output image
img = np.zeros((blocks_height * block_height, blocks_width * block_width, 3),np.uint8)

def print_byte_hex(x, y, byte):
    scale = 0.3
    color = (255, 255, 255)
    thickness = 1
    offset = 4
    cv2.putText(img, f"{byte:02x}", [y*block_width + offset, x*block_height + offset], cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

for x in range(blocks_height):
    for y in range(blocks_width):
        # Draw items
        byte = items_data[input_idx]
        if byte != 0:
            img[x*block_width:x*block_width+block_width, y*block_height:y*block_height+block_height] = items[byte]

        # Draw structure
        byte = structure_data[input_idx]
        if byte != 0:
            img[x*block_width:x*block_width+block_width, y*block_height:y*block_height+block_height] = structure[byte]

        # Draw magic
        byte = magic_data[input_idx]
        if byte not in [MAGIC_NONE, MAGIC_ANIM1, MAGIC_ANIM2]:
            print_byte_hex(x, y, byte)

        input_idx += 1

cv2.imwrite(output_filename, img)

# Show the image
cv2.namedWindow("output", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
cv2.imshow("output", img)

# Wait for 'q' key or window closed
wait_time = 100
while cv2.getWindowProperty('output', cv2.WND_PROP_VISIBLE) >= 1:
    keyCode = cv2.waitKey(wait_time)
    if (keyCode & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break
