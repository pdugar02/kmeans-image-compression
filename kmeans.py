import urllib.request
import io
import random
import sys
import time
from PIL import Image

start = time.perf_counter()
# URL, k = sys.argv[1], int(sys.argv[2])

k = 8
means = {}
# URL = 'https://i.pinimg.com/originals/77/a5/60/77a560fea9b616d5882d2d8f8c673c8d.jpg'
# URL = "https://i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg"
# f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
# img = Image.open(f)
img = Image.open("old_trafford.jpg")  # You can also use this on a local file; just put the local filename in quotes
# in place of f.
width, height = img.size
pix = img.load()  # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.


def squared_error(pixel, means_list):
    r, g, b = pixel
    min_error = ((-1, -1), 255 ** 2 + 255 ** 2 + 255 ** 2)
    for m in means_list.keys():
        r1, g1, b1 = m
        s_error = (r - r1) ** 2 + (g - g1) ** 2 + (b - b1) ** 2 # Squared error between the pixel and the mean m
        if min_error[1] >= s_error:
            min_error = (m, s_error) # tuple with the mean and the
    return min_error[0]

def min_mean_error(means_list):
    min_mean_squared_error = {}
    for mean in means_list:
        min_distance = (255**2)*3
        for m in means_list:
            if mean!=m:
                r,g,b = mean
                r1, g1, b1 = m
                s_error = (r - r1) ** 2 + (g - g1) ** 2 + (b - b1) ** 2
                if s_error<min_distance:
                    min_distance = s_error
        min_mean_squared_error[mean] = min_distance
    return min_mean_squared_error

def avg(pixel_list):
    return sum(pixel_list) / len(pixel_list)

# Pick k random pixels from the image as the initial "means"
while len(means)<k:
    x = random.randrange(width)
    y = random.randrange(height)
    means[pix[x, y]] = []

pixels = {}
min_distances = {}
# Add each pixel to one of the means' lists, based on squared error
for x in range(width):
    for y in range(height):
        p = pix[x, y]
        if p not in pixels:
            pixels[p] = [(x,y)]
            closest_mean = squared_error(p, means)
            min_distances[p] = closest_mean
            means[closest_mean].append((x, y))
        else:
            pixels[p].append((x,y))
            means[min_distances[p]].append((x, y))

# Find the real average of each list, then replace the old mean with the new average
new_means = {}
for m, l in means.items():
    real_mean = map(avg, zip(*[pix[x, y] for (x, y) in l]))
    real_mean = tuple([round(color) for color in real_mean])
    new_means[real_mean] = means[m]
means = new_means
min_mean_distance = min_mean_error(means)
differences = {}
generation=1
while [a for a in differences.values()]!=[0]*k:
    differences = {m:0 for m in means}
    already_moved = []
    # Add each pixel to one of the means' lists, based on squared error
    for m, l in means.items():
        r1, g1, b1 = m
        for (x, y) in l:
            # if (x, y) not in already_moved:
            p = pix[x, y]
            threshold = min_mean_distance[m]
            r,g,b = p
            s_error = (r - r1) ** 2 + (g - g1) ** 2 + (b - b1) ** 2
            if s_error>= .25 * threshold:
                closest_mean = squared_error(p, means)
                if closest_mean!=m:
                    # for point in pixels[p]:
                    means[closest_mean].append((x,y))
                    means[m].remove((x,y))
                    differences[closest_mean]+=1
                    differences[m]-=1
                    # already_moved.append((x,y))
    # Find the new average of each list, then replace the old mean with the new average
    new_means = {}
    for m, l in means.items():
        real_mean = map(avg, zip(*[pix[x, y] for (x, y) in l]))
        real_mean = tuple([round(color) for color in real_mean])
        new_means[real_mean] = means[m]
    means = new_means
    min_mean_distance = min_mean_error(means)
    print("Differences in generation %s"% generation+": %s"% [v for v in differences.values()])
    generation+=1

# # Replace every pixel with its mean
for m, l in means.items():
    for x1, y1 in l:
        pix[x1, y1] = m

# print(means)
# print(squared_errors)

img.show()
img.save("8_colors_kmeans.png") # Save the resulting image. Alter your filename as necessary.
end = time.perf_counter()
print("Time: %s"%(end-start))