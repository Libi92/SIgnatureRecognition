import numpy
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy import misc

img = Image.open('data/Signature2602e.jpg')

# Grayscale convertion
imgBW = img.convert('L')
imgBW.show()

# Scaling to 100x100
imgResize = imgBW.resize((100, 100))
imgResize.show()

# Denoising using median filtering
med_denoised = ndimage.median_filter(imgResize, 2)

misc.imsave('denoised.png', med_denoised)
plt.imshow(med_denoised)
plt.show()

imCopy = numpy.array(med_denoised)

# Background elimination
for i in range(len(med_denoised)):
    for j in range(len(med_denoised[i])):
        if med_denoised[i, j] < 180:
            imCopy[i, j] = 0
        else:
            imCopy[i, j] = 255

misc.imsave('background_eliminated.png', imCopy)
plt.imshow(imCopy)
plt.show()

minX = len(med_denoised)
minY = len(med_denoised)
maxX = 0
maxY = 0

for i in range(len(imCopy)):
    for j in range(len(imCopy[i])):
        if imCopy[i, j] == 0 and j < minX:
            minX = j
        if imCopy[i, j] == 0 and i < minY:
            minY = i

        if imCopy[i, j] == 0 and j > maxX:
            maxX = j
        if imCopy[i, j] == 0 and i > maxY:
            maxY = i

print minX, minY, maxX, maxY

imNormal = imCopy[minY:maxY, minX:maxX]


misc.imsave('normalized.png', imNormal)
plt.imshow(imNormal)
plt.show()
