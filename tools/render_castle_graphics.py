import sys
import numpy as np
import cv2

castle_structure_filename = "extracted/castle1_structure.bin"
castle_items_filename = "extracted/castle1_items.bin"
output_filename = "render/castle1.png"

blocks_width=250
blocks_height=180
blocks_len = blocks_width * blocks_height

with open(castle_structure_filename, "rb") as input_file:
    # Read the castle data
    data = input_file.read()
    input_idx = 0

    # create the data behind our output image
    img = np.zeros((blocks_height, blocks_width, 3),np.uint8)

    for x in range(blocks_height):
        for y in range(blocks_width):
            byte = data[input_idx]
            input_idx += 1

            if byte > 1:
                img[x,y] = [255,255,255]

    cv2.imwrite(output_filename, img)
    cv2.imshow("Castle", img)
    cv2.waitKey(0)