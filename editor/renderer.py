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

HOME=".."

class CastleRenderer:
    def __init__(self):
        self.structure_sprites = {}
        for i in range(200):
            self.structure_sprites[i] = cv2.imread(f"{HOME}/extracted/images/structure/{i:03}.png")

        self.item_sprites = {}
        for i in range(200):
            self.item_sprites[i] = cv2.imread(f"{HOME}/extracted/images/items/{i:03}.png")

    def render(self, structure_data, items_data, magic_data):
        # Keep track of where we are - same index for all three files
        input_idx = 0

        # create the data behind our output image
        img = np.zeros((blocks_height * block_height, blocks_width * block_width, 3),np.uint8)

        # Read and apply background image
        bg_image = cv2.imread(f"{HOME}/original/sky1.jpg")
        img[612:2880, 0:output_width] = bg_image[0:2268, 0:output_width]

        def print_image(x, y, image):
            img[x*block_width:x*block_width+block_width, y*block_height:y*block_height+block_height] = image

        def print_byte_hex(x, y, byte):
            scale = 0.3
            color = (255, 255, 255)
            thickness = 1
            offset = 4
            cv2.putText(img, f"{byte:02x}", [y*block_width + offset, x*block_height + offset], cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

        for x in range(blocks_height):
            row_has_content = False # if there's nothing in the row we can drop it from the output

            for y in range(blocks_width):
                # Draw items
                byte = items_data[input_idx]
                if byte not in [ITEM_HOLE, ITEM_NOTHING]:
                    row_has_content = True
                if byte == ITEM_ENERGY: # draw a different frame of the animation, otherwise it looks dull
                    print_image(x, y, self.item_sprites[byte + 2])
                elif byte not in [ITEM_HOLE]:
                    print_image(x, y, self.item_sprites[byte])

                # Draw structure
                byte = structure_data[input_idx]
                if byte not in [STRUCTURE_NONE]:
                    row_has_content = True
                    print_image(x, y, self.structure_sprites[byte])

                # Draw magic
                byte = magic_data[input_idx]
                if byte not in [MAGIC_NONE, MAGIC_ANIM_02, MAGIC_ANIM_03, MAGIC_ANIM_60, MAGIC_ANIM_61]:
                    row_has_content = True
                    print_byte_hex(x, y, byte)

                input_idx += 1

        return img
    