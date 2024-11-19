import sys

from PIL import Image
input_filename = "extracted/castle_images.bin"
output_dir = "tmp/img"

img_width = 16
img_height = 16
bpp = 1
img_size = int(img_width * img_height * bpp / 8)
num_images = int(32000/img_size)

print(f"Extracting {img_width}x{img_height}x{bpp}bpp images of {img_size} bytes each")
print(f"{num_images} images total")

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
        img = Image.new("L", (img_width, img_height))
        pixels = img.load()

        # Convert 4bpp data to RGB using the CGA palette
        for y in range(img_height):
            for x in range(0, img_width, 8):
                print(f"[{y}, {x}]")
                byte_index = (y * img_width + x) // 8
                byte = raw_data[byte_index]

                for bit in range(8):
                    color = byte >> (7 - bit) & 1
                    pixels[x + bit, y] = color * 255

                # # Extract 2-bit pieces
                # piece1 = (byte >> 6) & 0b11  # Extract bits 7–6
                # piece2 = (byte >> 4) & 0b11  # Extract bits 5–4
                # piece3 = (byte >> 2) & 0b11  # Extract bits 3–2
                # piece4 = byte & 0b11         # Extract bits 1–0

                # # high_nibble = (byte >> 4) & 0xF
                # # low_nibble = byte & 0xF

                # # Map to the CGA palette
                # pixels[x, y] = piece1 * 85
                # pixels[x + 1, y] = piece2 * 85
                # pixels[x + 2, y] = piece3 * 85
                # pixels[x + 3, y] = piece4 * 85

        # Save the image as a PNG
        output_file = f"{output_dir}/{i:02x}.png"
        img.save(output_file)
       