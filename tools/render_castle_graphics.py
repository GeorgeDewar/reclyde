import sys
import numpy as np
import cv2

castle_num = sys.argv[1]
castle_structure_filename = f"extracted/castle{castle_num}_structure.bin"
castle_items_filename = f"extracted/castle{castle_num}_items.bin"
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

with open(castle_structure_filename, "rb") as structure_file:
    with open(castle_items_filename, "rb") as items_file:
        # Read the castle data
        structure_data = structure_file.read()
        items_data = items_file.read()
        input_idx = 0

        # create the data behind our output image
        img = np.zeros((blocks_height * block_height, blocks_width * block_width, 3),np.uint8)

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

                input_idx += 1

        cv2.imwrite(output_filename, img)

        # Show the image
        #preview = cv2.resize(img, (blocks_width * 4, blocks_height * 4))
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
        cv2.imshow("output", img)
        cv2.waitKey(0)
