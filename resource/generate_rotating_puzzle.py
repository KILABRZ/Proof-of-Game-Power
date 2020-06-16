from PIL import Image
from random import choice
import sys
import os
from base64 import b64encode

difficulty = int(sys.argv[1])
originImage = sys.argv[2]
problemName = sys.argv[3]

if difficulty not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
	print('0, 1, 2, 3, 4, 5, 6, 7, 8, 9')
	exit()

supercharset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def randomName():
	k = choice(supercharset) + choice(supercharset) + choice(supercharset) + choice(supercharset) + choice(supercharset)
	return k

im = Image.open(originImage)

s = (300, 500, 600, 640, 700, 720, 770, 800, 810, 900)[difficulty]
w = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)[difficulty]
b = (150, 125, 100, 80, 70, 60, 55, 50, 45, 45)[difficulty]
n = (4, 16, 36, 64, 100, 144, 196, 256, 324, 400)[difficulty]

im = im.resize((s, s))

try:
	os.mkdir('../static/rotating_puzzle/{}'.format(problemName))
except:
	print('OuO')

name_list = list()

for i in range(n):
	k = randomName() + '.png'
	name_list.append(k)

with open('../static/rotating_puzzle/{}/problem_description.txt'.format(problemName), 'w') as f:
	f.write(';'.join(name_list) + ';\n')


for i in range(w):
	for j in range(w):
		idx = i*w+j
		nim = im.crop((j*b, i*b, (j+1)*b, (i+1)*b))
		thename = name_list[idx]
		nim.save('../static/rotating_puzzle/{}/{}'.format(problemName, thename))

with open('../static/rotating_puzzle/problemlist.txt', 'a') as f:
	f.write('{},{}\n'.format(problemName, difficulty))