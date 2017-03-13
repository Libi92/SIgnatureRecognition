import cv
import glob
import operator
import numpy


def toBinary(img):
	# convert to grayscale
	if cv.GetElemType(img) == cv.CV_8UC3:
		# Create an image to store the output version on
		result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
		cv.CvtColor(img, result, cv.CV_RGB2GRAY)
	else:
		result = cv.CloneMat(img)

	# apply threshold
	# TODO: Make use of better thresholding algorithms
	thr = 230
	cv.Threshold(result, result, thr, 255, cv.CV_THRESH_BINARY)

	return result

def calculateGloablFeatureVector(img):
	import features
	(W,H,A,T) = features.basicGlobalFeatures(img)
	(Ci, Srad) = features.circularityFeature(img)
	Pv = features.verticalProjection(img)
	BSL = features.globalBaseLine(img)
	(B, t_v) = BSL
	U = features.upperLimit(img, BSL, Pv)
	L = features.lowerLimit(img, BSL, Pv)

	HtW = float(H) / W
	AtC = Ci
	TtA = float(T) / A
	BtH = float(B) / H
	LtH = float(L) / H
	UtH = float(H-U+1) / H

	return {'HtW': HtW, 'AtC': AtC, 'TtA': TtA, 'BtH': BtH, 'LtH': LtH, 'UtH': UtH}

