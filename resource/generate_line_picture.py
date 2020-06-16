from PIL import Image
from random import choice
W = 500
H = 500

lineW = 2
lineColor = (255, 0, 0)
backColor = (255, 255, 255)

im = Image.new('RGB', (W, H), backColor)

iW_range = range(10, 490)
iH_range = range(10, 490)

def randomPoint(wrange, hrange):
	x, y = choice(wrange), choice(hrange)
	return x, y

def pointDistance(pa, pb):
	return ((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2) ** 0.5

def drawPoint(im, x, y, r):
	for i in range(x-r, x+r+1):
		for j in range(y-r, y+r+1):
			if i < 0 or j < 0 or i >= W or j >= H:
				continue
			if pointDistance((i, j), (x, y)) <= r:
				im.putpixel((i, j), lineColor)
	return im

def drawLine(im, nowPoint, nextPoint):
	tr = 2000
	dx = nextPoint[0] - nowPoint[0]
	dy = nextPoint[1] - nowPoint[1]

	sx = nowPoint[0]
	sy = nowPoint[1]

	for r in range(tr):
		nx, ny = sx + dx * r / tr, sy + dy * r / tr
		nx, ny = int(nx), int(ny)
		im = drawPoint(im, nx, ny, lineW)

	return im


N = 25

nowPoint = randomPoint(iW_range, iH_range)
target_Length = 300

for i in range(N):

	print('[{}/{}]'.format(i+1, N))
	nextPoint = randomPoint(iW_range, iH_range)
	while pointDistance(nowPoint, nextPoint) <= target_Length:
		nextPoint = randomPoint(iW_range, iH_range)
	drawLine(im, nowPoint, nextPoint)
	nowPoint = nextPoint

lineColor = (0, 255, 0)

nowPoint = randomPoint(iW_range, iH_range)
target_Length = 300

for i in range(N):

	print('[{}/{}]'.format(i+1, N))
	nextPoint = randomPoint(iW_range, iH_range)
	while pointDistance(nowPoint, nextPoint) <= target_Length:
		nextPoint = randomPoint(iW_range, iH_range)
	drawLine(im, nowPoint, nextPoint)
	nowPoint = nextPoint

lineColor = (0, 0, 255)

nowPoint = randomPoint(iW_range, iH_range)
target_Length = 300

for i in range(N):

	print('[{}/{}]'.format(i+1, N))
	nextPoint = randomPoint(iW_range, iH_range)
	while pointDistance(nowPoint, nextPoint) <= target_Length:
		nextPoint = randomPoint(iW_range, iH_range)
	drawLine(im, nowPoint, nextPoint)
	nowPoint = nextPoint

im.save('linePicture.png')