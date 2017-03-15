import utils
import features
import cv
import operator
import glob
import json
import numpy


def test(file):
    img = cv.LoadImageM(file.name)
    slant = getslant(img)

    result = test_second_stage()
    return result


def getslant(img):
    BiImg = utils.toBinary(img)

    slantFeature = features.slantFeature(BiImg)
    sorted_slant = sorted(slantFeature.iteritems(), key=operator.itemgetter(1))
    slantness = sorted_slant[len(sorted_slant)-1]
    slant = slantness[0]
    return slant


def second_stage_classification(subfolder, img):

    dests = {}
    fv = utils.calculateGloablFeatureVector(img)
    for x in range(1,13):
        toAdd = '00'
        if x >= 10:
            toAdd = '0'
        files = glob.glob(subfolder + toAdd + str(x) +toAdd + str(x) + '.json')
        if len(files) == 1:
            FILE = open(files[0], 'r')
            file_contents = FILE.read()
            FILE.close()

            gmfv = json.loads(file_contents)
            dests[str(x)] = feature_space_distance(gmfv, fv)

    sorted_dests = sorted(dests.iteritems(), key=operator.itemgetter(1))
    return sorted_dests


def test_second_stage():
    folder = 'data/'

    print '-------'
    inputFile = 'johns.jpg'
    img = cv.LoadImageM(folder + inputFile)
    slant = getslant(img)
    dests = second_stage_classification(folder + slant + '/', img)
    print dests

    return dests


def feature_space_distance(gmfv, fv):
    a = numpy.array([gmfv['HtW'] ,gmfv['AtC'] ,gmfv['TtA'] ,gmfv['BtH'] ,gmfv['LtH'] ,gmfv['UtH']])
    b = numpy.array([fv['HtW'] ,fv['AtC'] ,fv['TtA'] ,fv['BtH'] ,fv['LtH'] ,fv['UtH']])

    return numpy.linalg.norm(a-b)


def pre_build(path1):
    import os
    normalized_ = 'data/normalized/'
    if not os.path.exists(normalized_):
        os.makedirs(normalized_)

    for (dirpath, dirnames, filenames) in os.walk(path1):

        for file_name in filenames:
            if file_name != '.DS_Store' and 'forged' not in file_name:
                file = os.path.join(dirpath, file_name)
                img = cv.LoadImageM(file)
                fv = utils.calculateGloablFeatureVector(img)
                data = json.dumps(fv)
                splt = file_name.split('.')[0]
                normalized_file = normalized_ + splt + '.json'
                out_file = open(normalized_file, 'w')
                out_file.write(data)
                out_file.close()


def test_image(img_path):
    dist = []
    import os
    normalized_ = 'data/normalized/'
    img = cv.LoadImageM(img_path)
    fv = utils.calculateGloablFeatureVector(img)
    for (dirpath, dirnames, filenames) in os.walk(normalized_):
        for file_name in filenames:
            if '.DS_Store' not in file_name:
                file = open(os.path.join(dirpath, file_name), 'r')
                content = file.read()
                file.close()
                gmfv = json.loads(content)
                distance = feature_space_distance(gmfv, fv)
                print (file_name, distance)
                dist.append(distance)

    return dist