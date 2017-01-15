import numpy
from PIL import Image
from ffnet import mlgraph, ffnet
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy import misc
from scipy.stats import stats


def showImage(img, savePath=None):
    if savePath:
        misc.imsave(savePath, img)
    plt.imshow(img)
    plt.show()


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
    showImage(med_denoised, 'denoised.png')
    return med_denoised


def backgroundEliminate(img):
    imgBackgroundEliminated = numpy.array(img)

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i, j] < 180:
                imgBackgroundEliminated[i, j] = 0
            else:
                imgBackgroundEliminated[i, j] = 255

    showImage(imgBackgroundEliminated, 'background_eliminated.png')
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
    showImage(imNormal, 'normalized.png')
    return imNormal


def thinImage(img, iterations=100):
    imThin = zhangSuen_vec(img, iterations)
    showImage(imThin, 'thinned.png')
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


def getDensityOfImage(img):
    nonZeroPixels = 0
    for row in img:
        for pixel in row:
            if pixel != 0:
                nonZeroPixels += 1
    density = nonZeroPixels / float(len(img) * len(row))
    return density


def getWidthToHeightRatio(img):
    width = len(img)
    height = len(img[0])
    return width / float(height)


def getSlope(img):
    xMax = len(img) - 1
    yMax = len(img[0]) - 1

    y2 = yMax
    for j in reversed(range(yMax)):
        if img[xMax, j] == 0:
            y2 = j
            break

    x2 = xMax
    for i in reversed(range(xMax)):
        if img[i, yMax] == 0:
            x2 = i

    print (x2, y2)
    slope = y2/float(x2)
    return slope


def train(trainData):
    print('Starting Training')
    inLength = 64
    numImages = len(images)

    inData = []
    for i in range(len(trainData)):
        row = []
        for j in range(inLength):
            row.append(trainData[i][j])
        inData.append(row)

    conec = mlgraph((inLength, 10, 10, inLength))
    net = ffnet(conec)
    input = numpy.array(inData)
    target = numpy.array(inData)
    net.train_tnc(input, target, maxfun=2000, messages=1)
    print('Training completed')


if __name__ == '__main__':
    images = ['data/paul.jpg', 'data/johns.jpg', 'data/edward.png']
    trainData = []
    for image in images:
        img = Image.open(image)

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
        imgThin = thinImage(imgNormal, 300)

        # Feature extraction
        #
        # Global Feature

        # Density feature
        density = getDensityOfImage(imgThin)
        print('Density ', density)

        # Width to height ratio
        widthHeightRatio = getWidthToHeightRatio(imgThin)
        print ('Width to height ratio', widthHeightRatio)

        # Slope feature
        slope = getSlope(imgThin)
        print ('Slope', slope)

        # Skew feature
        skew = stats.skew(imgThin)
        print('Skew', skew)

        # Constructing train data
        pattern = []
        pattern.append(density)
        pattern.append(widthHeightRatio)
        pattern.append(slope)
        pattern.extend(skew)

        trainData.append(pattern)

    # Training
    train(trainData)
