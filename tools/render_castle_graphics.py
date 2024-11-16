import sys
import numpy as np
import cv2

castle_structure_filename = "extracted/castle1_structure.bin"
castle_items_filename = "extracted/castle1_items.bin"
output_filename = "render/castle1.png"

# Dimensions of the castle in blocks
blocks_width=250
blocks_height=180
blocks_len = blocks_width * blocks_height

# Size of a block in pixels
block_width=16
block_height=16

img20 = cv2.imread("extracted/images/red_block.png")

with open(castle_structure_filename, "rb") as input_file:
    # Read the castle data
    data = input_file.read()
    input_idx = 0

    # create the data behind our output image
    img = np.zeros((blocks_height * block_height, blocks_width * block_width, 3),np.uint8)

    for x in range(blocks_height):
        for y in range(blocks_width):
            byte = data[input_idx]
            input_idx += 1

            if byte == 0x20:
                img[x*block_width:x*block_width+block_width, y*block_height:y*block_height+block_height] = img20
            elif byte > 1:
                for block_x in range(block_height):
                    for block_y in range(block_width):
                        img[x*block_width + block_x,y*block_height + block_y] = [255,255,255]

    cv2.imwrite(output_filename, img)

    # Show the image
    #preview = cv2.resize(img, (blocks_width * 4, blocks_height * 4))
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions
    cv2.imshow("output", img)
    cv2.waitKey(0)
