# kmeans-image-compression
Uses k-means clustering to compress an image to reduce the size of image files.

Originally completed April 2021 for the Artificial Intelligence course at Thomas Jefferson High School for Science and Technology.

This project develops three successive k-means clustering algorithms. Viewers can compare the files 8_colors_naive, 8_colors_kmeans, and 8_colors_kmeans2 to see the differences between the three versions. In this scenario, a "mean" refers to an average (r, g, b) value to determine the color of a pixel. The runtimes for each algorithm is calculated based on processing my image of choice, a 480 x 800 pixel image of Old Trafford, Manchester United's soccer stadium.
## kmeans_naive.py
The first iteration simply iterates through each pixel in the image and assigns each r, g, and b value of a pixel to 0 or 255, based on which "mean" the value falls closer to. This gives a total of 2 'means' (0 and 255) ^ 3 values (r, g, and b) = 2^3 = 8 different means. Similarly, for k=27, each r, g, and b value of a pixel is assigned to 0, 127, and 255 for a total of 3^3 = 27 means. This version is fast (around 0.5 seconds) but produces a bad representation of the original image.

## kmeans.py
The second iteration picks k random pixels to act as the initial "means", then iterates through each pixel in the image and associates them with each of the current means using Euclidean distance/squared error between the current pixel and one of the means. Then, for each of the k groups of "similar" pixels, the real mean is computed, and the pixels are re-evaluated to see if they belong in a different group. This process repeats until no pixels change groups, and then every pixel is replaced by its mean.

This version is quite slow (around 3 minutes for k = 8) but produces a better representation of the original image.

## kmeans2.py
The third iteration functions exactly as kmeans.py does, except that the groups that associate a "mean" with its list of similar pixels is now done on a color basis, significantly reducing runtime since many pixels in an image tend to have the same color. This version is much faster than kmeans.py (around 30 seconds for k=8) and produces a much better representation of the original image.
