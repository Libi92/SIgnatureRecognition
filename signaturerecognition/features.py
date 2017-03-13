import cv
import math
import operator

def basicGlobalFeatures(img):
	(W, H) = cv.GetSize(img)
	A = W*H

	T = 0
	for x in range(W):
		for y in range(H):
			if img[y,x] == 0:
				T += 1
	return (W,H,A,T)


# (Ci, Srad)
def circularityFeature(img):
	(W, H) = cv.GetSize(img)
	A = W*H
	Ci = (4 * W * H) / (math.pi * (W**2 + H**2))
	Srad = math.sqrt(W**2 + H**2)/2.0
	return (Ci, Srad)


def verticalProjection(img):
	(W, H) = cv.GetSize(img)
	Pv = []

	for y in range(H):
		tB = 0
		for x in range(W):
			if img[y, x] == 0: #Black pixle
				tB += 1
		Pv.append(tB)

	return Pv


def horizontalProjection(img):
	(W, H) = cv.GetSize(img)
	Ph = []

	for x in range(W):
		tB = 0
		for y in range(H):
			if img[y, x] == 0: #Black pixle
				tB += 1
		Ph.append(tB)

	return Ph


def verticalCenter(img):
	(W, H, A, T) = basicGlobalFeatures(img)
	Pv = verticalProjection(img)

	total = 0
	for y in range(H):
		total += y * Pv[y]

	result = total/T
	return int(result)

# Just like verical center
def horizontalCenter(img):
	(W, H, A, T) = basicGlobalFeatures(img)
	Ph = horizontalProjection(img)

	total = 0
	for x in range(W):
		total += x * Ph[x]

	result = total/T
	return int(result)


def globalBaseLine(img):
	(W, H) = cv.GetSize(img)
	Pv = verticalProjection(img)
	the_y = 0
	the_value = 0

	for y in range(H):
		if Pv[y] > the_value:
			the_value = Pv[y]
			the_y = y

	return (the_y, the_value)

def upperLimit(img, GBL, Pv):
	BL, value = GBL
	UL = 0
	diff = 0
	for y in range(BL):
		smoothV = y * value / BL
		tempDiff = abs(Pv[y] - smoothV)
		if tempDiff > diff:
			UL = y
			diff = tempDiff

	return UL

def lowerLimit(img, GBL, Pv):
	BL, value = GBL
	LL = 0
	diff = 0

	W,H = cv.GetSize(img)

	for y in range(BL, H):
		smoothV = value - (y * value / ((H-1) - BL))
		tempDiff = abs(Pv[y] - smoothV)
		if tempDiff > diff:
			LL = y
			diff = tempDiff

	return LL


def connectivity(img, y, x):
	result = 0
	W, H = cv.GetSize(img)
	if y < 1 or y >= H-1:
		return -1
	if x < 1 or x >= W-1:
		return -1

	track = [img[y-1,x], img[y-1, x+1], img[y, x+1], img[y+1, x+1], img[y+1, x], img[y+1, x-1], img[y, x-1], img[y-1, x-1], img[y-1, x]]

	for z in range(len(track)):
		if track[z] == 255:
			if z < len(track) - 2 and track[z+1] == 0:
				result += 1
	return result

# Only used in slant feature
def thinning(img):
	img = cv.CloneMat(img)
	# this contains a list of CvPoints that are marked by sub iterations to be deleted
	W, H = cv.GetSize(img)
	i = 0
	while i < 1:
		i += 1
		marked = []
		# sub-iteration 1
		for y in range(H):
			for x in range(W):
				if img[y, x] == 0:
					if connectivity(img, y, x) == 1:
						neighbors = [img[y-1,x], img[y-1, x+1], img[y, x+1], img[y+1, x+1], img[y+1, x], img[y+1, x-1], img[y, x-1], img[y-1, x-1]]
						object_neighbors = 8 - int(sum(neighbors)/255)
						if object_neighbors >= 2 and object_neighbors <= 6:
							if sum([img[y-1, x], img[y, x+1], img[y+1, x]]) >= 255: #at least one background (255)
								if sum([img[y, x+1], img[y+1, x], img[y, x-1]]) >= 255: #at leat one background (255)
									marked.append((y, x))

		if len(marked) == 0:
			return img
		for (y, x) in marked:
			img[y, x] = 255

		# sub-iteration 2
		marked = []
		for y in range(H):
			for x in range(W):
				if img[y, x] == 0:
					if connectivity(img, y, x) == 1:
						neighbors = [img[y-1,x], img[y-1, x+1], img[y, x+1], img[y+1, x+1], img[y+1, x], img[y+1, x-1], img[y, x-1], img[y-1, x-1]]
						object_neighbors = 8 - int(sum(neighbors)/255)
						if object_neighbors >= 2 and object_neighbors <= 6:
							if sum([img[y-1, x], img[y, x+1], img[y, x-1]]) >= 255: #at least one background (255)
								if sum([img[y-1, x], img[y+1, x], img[y, x-1]]) >= 255: #at leat one background (255)
									marked.append((y, x))
		if len(marked) == 0:
			return img
		for (y, x) in marked:
			img[y, x] = 255

	return img
# Negatively Slanted(NS), Vertically Stalnted(VS), Positively Slanted(PS) and Horizontally Slanted (HS)
# returns a dict {'NS': int, 'VS': int, 'PS': int, 'HS': int}
def slantFeature(img):
	W, H = cv.GetSize(img)
	thinnedImage = thinning(img)
	slant = {}
	slant['NS'] = 0
	slant['VS'] = 0
	slant['PS'] = 0
	slant['HS'] = 0

	for y in range(1, H-1):
		for x in range(1, W-1):
			if img[y, x] == 0:
				if img[y-1, x-1] == 0:
					slant['NS'] += 1
				if img[y, x-1] == 0:
					slant['VS'] += 1
				if img[y+1, x-1] == 0:
					slant['PS'] += 1
				if img[y+1, x] == 0:
					slant['HS'] += 1

	return slant
