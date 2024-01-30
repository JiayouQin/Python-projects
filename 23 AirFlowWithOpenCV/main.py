'''
01/29/2024 Jiayou Qin
with a 0.5 kernel the value will be exchanged which creates an oscillation of values that 
causes some values to grow exponentially, after overflow it becomes 0 so anihilates
smaller value will decrease oscillation strength with 4 it will be completely stopped.
'''

import numpy as np
import cv2 as cv


image = np.random.rand(512,512,1)
# image = np.ones((1024,1024,1))
propagation = 4	#higher number means slower propagation, under 4 might cause issues
kernel_up = np.array([[0,1,0],[0,-1,0],[0,0,0]],np.float32)/propagation
kernel_down = np.array([[0,0,0],[0,-1,0],[0,1,0]],np.float32)/propagation
kernel_left = np.array([[0,0,0],[1,-1,0],[0,0,0]],np.float32)/propagation
kernel_right = np.array([[0,0,0],[0,-1,1],[0,0,0]],np.float32)/propagation

moveUp = np.float32([[1, 0, 0],[0, 1, -1]])
moveDown = np.float32([[1, 0, 0],[0, 1, 1]])
moveLeft = np.float32([[1, 0, -1],[0, 1, 0]])
moveRight = np.float32([[1, 0, 1],[0, 1, 0]])

cv.namedWindow('img', cv.WINDOW_NORMAL )
residue = True

shifted1 = np.random.rand(512,512,1)*0.25
shifted2 = np.random.rand(512,512,1)*0.25
shifted3 = np.random.rand(512,512,1)*0.25
shifted4 = np.random.rand(512,512,1)*0.25

h,w = image.shape[:2]
friction=0.3 #set this to 0-1 
cv.imshow('img',image)
cv.waitKey(0)

while True:
	cv.imshow('img',image)
	# print(np.mean(image))	#sanity check, see if particles disappear
	# print(np.max(image))
	grad1 = cv.filter2D(image, -1, kernel_up)	#gradient up\
	grad2 = cv.filter2D(image, -1, kernel_down)	#gradient down
	grad3 = cv.filter2D(image, -1, kernel_left)	#gradient down
	grad4 = cv.filter2D(image, -1, kernel_right)	#gradient down
	if residue:
		grad1 = cv.add(grad1, shifted1 * (1-friction) )
		grad2 = cv.add(grad2, shifted2 * (1-friction) )
		grad3 = cv.add(grad3, shifted3 * (1-friction) )
		grad4 = cv.add(grad4, shifted4 * (1-friction) )

	grad_max = np.maximum(grad1, grad2)
	grad_max = np.maximum(grad_max, grad3)
	grad_max = np.maximum(grad_max, grad4) 

	#take only max gradient
	mask = grad1 !=grad_max
	grad1[mask] = 0
	mask = grad2 !=grad_max
	grad2[mask] = 0	
	mask = grad3 !=grad_max
	grad3[mask] = 0 
	mask = grad4 !=grad_max
	grad4[mask] = 0

	grad1 = cv.rectangle(grad1, (0,0),(h-1,w-1), 0, 1)
	grad2 = cv.rectangle(grad2, (0,0),(h-1,w-1), 0, 1)
	grad3 = cv.rectangle(grad3, (0,0),(h-1,w-1), 0, 1)
	grad4 = cv.rectangle(grad4, (0,0),(h-1,w-1), 0, 1)

	shifted1 = cv.warpAffine(grad1, moveUp, (grad1.shape[1], grad1.shape[0]))
	shifted2 = cv.warpAffine(grad2, moveDown, (grad2.shape[1], grad2.shape[0]))
	shifted3 = cv.warpAffine(grad3, moveLeft, (grad3.shape[1], grad3.shape[0]))
	shifted4 = cv.warpAffine(grad4, moveRight, (grad4.shape[1], grad4.shape[0]))
	
	residue = [shifted1,shifted2,shifted3,shifted4]

	image = cv.add(image,grad1)
	image = cv.subtract(image,shifted1)
	image = cv.add(image,grad2)
	image = cv.subtract(image,shifted2)
	image = cv.add(image,grad3)
	image = cv.subtract(image,shifted3)
	image = cv.add(image,grad4)
	image = cv.subtract(image,shifted4)

	if cv.waitKey(5) == ord('x'):
		image[200:250, 200:250] = 0
		# break