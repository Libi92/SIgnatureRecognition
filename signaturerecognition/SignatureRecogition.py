import numpy
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy import misc


def convertGrayscale(img):
    imgBW = img.convert('L')
    imgBW.show()
    return imgBW


def scaleImage(img):
    imgResize = img.resize((100, 100))
    imgResize.show()
    return imgResize


def denoiseImage(img):
    med_denoised = ndimage.median_filter(img, 2)

    misc.imsave('denoised.png', med_denoised)
    plt.imshow(med_denoised)
    plt.show()
    return med_denoised


def backgroundEliminate(img):
    imgBackgroundEliminated = numpy.array(img)

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i, j] < 180:
                imgBackgroundEliminated[i, j] = 0
            else:
                imgBackgroundEliminated[i, j] = 255

    misc.imsave('background_eliminated.png', imgBackgroundEliminated)
    plt.imshow(imgBackgroundEliminated)
    plt.show()
    return imgBackgroundEliminated


def normalizeImage(img):
    minX = len(img)
    minY = len(img)
    maxX = 0
    maxY = 0

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i, j] == 0 and j < minX:
                minX = j
            if img[i, j] == 0 and i < minY:
                minY = i

            if img[i, j] == 0 and j > maxX:
                maxX = j
            if img[i, j] == 0 and i > maxY:
                maxY = i

    print minX, minY, maxX, maxY

    imNormal = img[minY:maxY, minX:maxX]

    misc.imsave('normalized.png', imNormal)
    plt.imshow(imNormal)
    plt.show()
    return imNormal


def thinImage(img):
    imThin = zhangSuen_vec(img, 100)
    misc.imsave('thinned.png', imThin)
    plt.imshow(imThin)
    plt.show()
    return imThin


def neighbours_vec(image):
    return image[2:,1:-1], image[2:,2:], image[1:-1,2:], image[:-2,2:], image[:-2,1:-1],     image[:-2,:-2], image[1:-1,:-2], image[2:,:-2]


def transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9):
    return ((P3-P2) > 0).astype(int) + ((P4-P3) > 0).astype(int) + \
    ((P5-P4) > 0).astype(int) + ((P6-P5) > 0).astype(int) + \
    ((P7-P6) > 0).astype(int) + ((P8-P7) > 0).astype(int) + \
    ((P9-P8) > 0).astype(int) + ((P2-P9) > 0).astype(int)


def zhangSuen_vec(image, iterations):
    for iter in range (1, iterations):
        print iter
        # step 1
        P2,P3,P4,P5,P6,P7,P8,P9 = neighbours_vec(image)
        condition0 = image[1:-1,1:-1]
        condition4 = P4*P6*P8
        condition3 = P2*P4*P6
        condition2 = transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
        condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
        cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * (condition2 == 1) * (condition1 == 1)
        changing1 = numpy.where(cond == 1)
        image[changing1[0]+1,changing1[1]+1] = 0
        # step 2
        P2,P3,P4,P5,P6,P7,P8,P9 = neighbours_vec(image)
        condition0 = image[1:-1,1:-1]
        condition4 = P2*P6*P8
        condition3 = P2*P4*P8
        condition2 = transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
        condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
        cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * (condition2 == 1) * (condition1 == 1)
        changing2 = numpy.where(cond == 1)
        image[changing2[0]+1,changing2[1]+1] = 0
    return image


if __name__ == '__main__':
    img = Image.open('data/Signature2602e.jpg')

    # Grayscale convertion
    imgBW = convertGrayscale(img)

    # Scaling to 100x100
    imgResize = scaleImage(imgBW)

    # Denoising using median filtering
    imgDenoised = denoiseImage(imgResize)

    # Background elimination
    imgBackgroundEliminated = backgroundEliminate(imgDenoised)

    # Signature Normalization
    imgNormal = normalizeImage(imgBackgroundEliminated)

    # Thinning Image
    imgThin = thinImage(imgNormal)
