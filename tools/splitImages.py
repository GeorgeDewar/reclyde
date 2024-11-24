import cv2

img_width = 16
img_height = 16

rows = 10
cols = 20

def split_images(input_filename, output_prefix):
    input_img = cv2.imread(input_filename)
    for row in range(rows):
        for col in range(cols):
            x = row * img_width
            y = col * img_height
            output_img = input_img[x:x+img_width, y:y+img_height]
            index = row * cols + col
            filename = f"{output_prefix}{index:03}.png"
            print(f"Writing {filename}")
            cv2.imwrite(filename, output_img)
