import sys
import numpy as np
import cv2

ITEM_HOLE = 0x00
ITEM_NOTHING = 0x01 # Plain blue background
ITEM_ENERGY = 0x36

STRUCTURE_NONE = 0x00

MAGIC_NONE = 0x00
MAGIC_ANIM_02 = 0x02
MAGIC_ANIM_03 = 0x03
MAGIC_ANIM_60 = 0x60
MAGIC_ANIM_61 = 0x61

castle_num = sys.argv[1]
castle_structure_filename = f"extracted/volume4_castles/castle{castle_num}_structure.bin"
castle_items_filename = f"extracted/volume4_castles/castle{castle_num}_items.bin"
castle_magic_filename = f"extracted/volume4_castles/castle{castle_num}_magic.bin"
output_filename = f"render/castle{castle_num}.png"

# Dimensions of the castle in blocks
blocks_width=250
blocks_height=180
blocks_len = blocks_width * blocks_height

# Size of a block in pixels
block_width=16
block_height=16

# Output image size
output_height=blocks_height*block_height
output_width=blocks_width*block_width

structure = {}
for i in range(200):
    structure[i] = cv2.imread(f"extracted/images/structure/{i:03}.png")

items = {}
for i in range(200):
    items[i] = cv2.imread(f"extracted/images/items/{i:03}.png")

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

# Read and apply background image
bg_image = cv2.imread("original/sky1.jpg")
img[612:2880, 0:output_width] = bg_image[0:2268, 0:output_width]

def print_image(x, y, image):
    img[x*block_width:x*block_width+block_width, y*block_height:y*block_height+block_height] = image

def print_byte_hex(x, y, byte):
    scale = 0.3
    color = (255, 255, 255)
    thickness = 1
    offset = 4
    cv2.putText(img, f"{byte:02x}", [y*block_width + offset, x*block_height + offset], cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

first_content = None
for x in range(blocks_height):
    row_has_content = False # if there's nothing in the row we can drop it from the output

    for y in range(blocks_width):
        # Draw items
        byte = items_data[input_idx]
        if byte not in [ITEM_HOLE, ITEM_NOTHING]:
            row_has_content = True
        if byte == ITEM_ENERGY: # draw a different frame of the animation, otherwise it looks dull
            print_image(x, y, items[byte + 2])
        elif byte not in [ITEM_HOLE]:
            print_image(x, y, items[byte])

        # Draw structure
        byte = structure_data[input_idx]
        if byte not in [STRUCTURE_NONE]:
            row_has_content = True
            print_image(x, y, structure[byte])

        # Draw magic
        byte = magic_data[input_idx]
        if byte not in [MAGIC_NONE, MAGIC_ANIM_02, MAGIC_ANIM_03, MAGIC_ANIM_60, MAGIC_ANIM_61]:
            row_has_content = True
            print_byte_hex(x, y, byte)

        input_idx += 1

    if row_has_content and first_content is None:
        first_content = x

img = img[first_content*block_height:blocks_height * block_height, 0:blocks_width * block_width]

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
