import numpy as np
from PIL import Image

def ega_render_mode_0x0D(video_memory):
    width, height = 320, 200
    bytes_per_row = width // 8  # Each byte covers 8 pixels

    # Prepare a blank image
    image_data = np.zeros((height, width), dtype=np.uint8)

    # Divide video memory into 4 planes
    plane_size = len(video_memory) // 4
    planes = [
        video_memory[i * plane_size : (i + 1) * plane_size] for i in range(4)
    ]

    # Decode the EGA memory
    for row in range(height):
        for col_byte in range(bytes_per_row):
            # Get the offset in the plane for this byte
            offset = row * bytes_per_row + col_byte

            # Read the bits for this group of 8 pixels
            if offset < plane_size:
                plane_bits = [planes[plane][offset] for plane in range(4)]
            else:
                # Default to 0 if offset exceeds plane size
                plane_bits = [0, 0, 0, 0]

            # Extract 8 pixels from the bitplanes
            for bit in range(8):
                color = 0
                for plane in range(4):
                    color |= ((plane_bits[plane] >> (7 - bit)) & 1) << plane

                # Set the pixel in the image data
                image_data[row, col_byte * 8 + bit] = color

    return image_data


# Load the video memory (replace with your file path)
with open("extracted/castle_images_structure.bin", "rb") as f:
    video_memory = f.read()

# Render the image for mode 0x0D
ega_image = ega_render_mode_0x0D(video_memory)

# Map EGA palette (16 colors) to RGB
ega_palette = [
    (0, 0, 0),       # Black
    (0, 0, 170),     # Blue
    (0, 170, 0),     # Green
    (0, 170, 170),   # Cyan
    (170, 0, 0),     # Red
    (170, 0, 170),   # Magenta
    (170, 85, 0),    # Brown
    (170, 170, 170), # Light Gray
    (85, 85, 85),    # Dark Gray
    (85, 85, 255),   # Light Blue
    (85, 255, 85),   # Light Green
    (85, 255, 255),  # Light Cyan
    (255, 85, 85),   # Light Red
    (255, 85, 255),  # Light Magenta
    (255, 255, 85),  # Yellow
    (255, 255, 255), # White
]

# Convert to RGB image
height, width = ega_image.shape
rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
for color_index, (r, g, b) in enumerate(ega_palette):
    rgb_image[ega_image == color_index] = (r, g, b)

# Save and display the image
img = Image.fromarray(rgb_image)
img.save("tmp/ega_render_mode_0x0D.png")
img.show()