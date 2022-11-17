import cv2 as cv
import numpy as np
import random 
import json

message = 'Kermit Goes KABOOM'
btArray = bytearray(message.encode(encoding='UTF-8')) 

image = cv.imread('kermit.png')
h,w = image.shape[:2]
c = 3 if len(image.shape) == 3 else 1
print(w,h,c)
coords = []
print(len(btArray))
i=0
while i < len(btArray):
	randPos = (random.randint(0,w),random.randint(0,h))
	if randPos in coords:
		continue
	coords.append(randPos)
	i += 1

for i in range(len(btArray)):
	x,y = coords[i]
	image[y][x][0] = btArray[i] 

cv.imwrite('kermitWithMsg.png',image)

with open('coords.json','w+') as f:
	f.write(json.dumps(coords))