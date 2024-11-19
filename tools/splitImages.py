import cv2

input_filename = "extracted/images/castle_structure_images.png"
output_dir = "tmp/img/structure"

img_width = 16
img_height = 16

rows = 12
cols = 20

input_img = cv2.imread(input_filename)
for row in range(rows):
    for col in range(cols):
        x = row * img_width
        y = col * img_height
        output_img = input_img[x:x+img_width, y:y+img_height]
        index = row * cols + col
        filename = f"{output_dir}/{index:02x}.png"
        print(f"Writing {filename}")
        cv2.imwrite(filename, output_img)
