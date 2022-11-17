import cv2 as cv
import numpy as np
import random 
import json

with open('coords.json','r') as f:
	coords = json.loads(f.read())

image = cv.imread('kermitWithMsg.png')

btArray = bytearray()
for i in range(len(coords)):
	x,y = coords[i]
	btArray.append(image[y][x][0])

print(btArray.decode(encoding='UTF-8'))