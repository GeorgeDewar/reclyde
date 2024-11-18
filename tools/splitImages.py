import sys

from PIL import Image
input_filename = "extracted/castle_images.bin"
output_dir = "tmp/img"

num_images = 250
img_size = 128

img_width = 16
img_height = 16

# Define the CGA palette (RGB tuples)
CGA_PALETTE = [
    (0, 0, 0),       # Black
    (0, 0, 170),     # Blue
    (0, 170, 0),     # Green
    (0, 170, 170),   # Cyan
    (170, 0, 0),     # Red
    (170, 0, 170),   # Magenta
    (170, 85, 0),    # Brown
    (170, 170, 170), # Light gray
    (85, 85, 85),    # Dark gray
    (85, 85, 255),   # Light blue
    (85, 255, 85),   # Light green
    (85, 255, 255),  # Light cyan
    (255, 85, 85),   # Light red
    (255, 85, 255),  # Light magenta
    (255, 255, 85),  # Yellow
    (255, 255, 255), # White
]

with open(input_filename, "rb") as input_file:
    # Read the castle data
    data = input_file.read()
    input_idx = 0

    for i in range(num_images):
        start = i*img_size
        end = start + img_size
        raw_data = data[start:end]

        # Create an empty RGB image
        img = Image.new("RGB", (img_width, img_height))
        pixels = img.load()

        # Convert 4bpp data to RGB using the CGA palette
        for y in range(img_height):
            for x in range(0, img_width, 2):
                byte_index = (y * img_width + x) // 2
                byte = raw_data[byte_index]

                # Extract two 4-bit values from the byte
                high_nibble = (byte >> 4) & 0xF
                low_nibble = byte & 0xF

                # Map to the CGA palette
                pixels[x, y] = CGA_PALETTE[high_nibble]
                pixels[x + 1, y] = CGA_PALETTE[low_nibble]

        # Save the image as a PNG
        output_file = f"{output_dir}/{i:02x}.png"
        img.save(output_file)
       