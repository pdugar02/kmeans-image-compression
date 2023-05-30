import urllib.request
import io
from PIL import Image
import time

start = time.perf_counter()

# URL = 'https://i.pinimg.com/originals/77/a5/60/77a560fea9b616d5882d2d8f8c673c8d.jpg'
# f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
# img = Image.open(f)
img = Image.open("old_trafford.jpg") # You can also use this on a local file; just put the local filename in quotes
# in place of f.
pix = img.load()  # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.

width, height = img.size
# k=8
for x in range(width):
    for y in range(height):
        r,g,b = pix[x, y]
        color_list = [r,g,b]
        for i in range(3):
            c = color_list[i]
            if c < 128:
                c = 0
            else:
                c = 255
            color_list[i] = c
        pix[x, y] = tuple(color_list)

# k=27
# for x in range(width):
#     for y in range(height):
#         r,g,b = pix[x,y]
#         color_list = [r,g,b]
#         for i in range(3):
#             c = color_list[i]
#             if c<255//3:
#                 c=0
#             elif c>255*2//3:
#                 c=255
#             else:
#                 c=127
#             color_list[i] = c
#         pix[x,y] = tuple(color_list)

img.show() # Send the image to your OS to be displayed as a temporary file
# img.save("8_colors_naive.png") # Save the resulting image. Alter your filename as necessary.
# img.save("27_colors_naive.png") # Save the resulting image. Alter your filename as necessary.
end = time.perf_counter()
print("Time: %s" % (end - start))