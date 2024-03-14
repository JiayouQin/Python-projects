'''
03/12/2024 Jiayou Qin
Density based particle simulation, currently collision has not yet been implemented
for acceleration the same method could be used with GPU
'''

import numpy as np
import cv2 as cv

grid_size = (500, 500)
density = np.random.rand(grid_size[0],grid_size[1])
tempreture = np.ones(grid_size,dtype=np.float32)
# density[300:512,0:512] = 0

# image = np.ones((1024,1024,1))
propagation = 5 #higher number means slower propagation, must be higher than 4
kernel_up = np.array([[0,1,0],[0,-1,0],[0,0,0]],np.float32)*0.5/propagation #constant 0.5 due to duplicated operation
kernel_down = np.array([[0,0,0],[0,-1,0],[0,1,0]],np.float32)*0.5/propagation
kernel_left = np.array([[0,0,0],[1,-1,0],[0,0,0]],np.float32)*0.5/propagation
kernel_right = np.array([[0,0,0],[0,-1,1],[0,0,0]],np.float32)*0.5/propagation

moveUp = np.float32([[1, 0, 0],[0, 1, -1]])
moveDown = np.float32([[1, 0, 0],[0, 1, 1]])
moveLeft = np.float32([[1, 0, -1],[0, 1, 0]])
moveRight = np.float32([[1, 0, 1],[0, 1, 0]])

cv.namedWindow('img', cv.WINDOW_NORMAL )
residue = False

friction = 0.5 - 0.005 #do not edit the 0.5 constant,small number for friction recommended


cv.imshow('img',density)
cv.waitKey(0)
pistonY = 400

flow1 = np.zeros(grid_size)
flow2 = np.zeros(grid_size)
flow3 = np.zeros(grid_size)
flow4 = np.zeros(grid_size)


wall_mask = np.zeros(grid_size,dtype=np.bool)

pt1,pt2,pt3,pt4 = (200,100),(500,100),(200,300),(500,100)


wall_mask[200:480, 10:15] = 1 #left wall
wall_mask[200:310, 210:215] = 1 #right wall 1
wall_mask[320:475, 210:215] = 1 #right wall 2
wall_mask[475:480, 210:215] = 1 #right wall 3
wall_mask[475:480, 10:215] = 1

while True:

    outImage = density.copy()
    outImage[int(pistonY), 10:215] = 255
    outImage[wall_mask] = 255
    cv.imshow('img',outImage)

    temp = density*tempreture
    grad1 = cv.filter2D(temp, -1, kernel_up)    #gradient up\
    grad2 = cv.filter2D(temp, -1, kernel_down)  #gradient down
    grad3 = cv.filter2D(temp, -1, kernel_left)  #gradient down
    grad4 = cv.filter2D(temp, -1, kernel_right) #gradient down

    grad1 += flow1 *friction
    grad2 += flow2 *friction
    grad3 += flow3 *friction
    grad4 += flow4 *friction
    # else:
        # grad2[0:300,0:512] += 0.2
        # continue
    #wall
    pressure = np.mean(flow1[int(pistonY)+2, 110:415]) - np.mean(flow2[int(pistonY)-2, 110:415])

    movement = pressure*5
    if movement < 0.1:
        movement = 0
    if movement > 1:
        movement = 1
    if movement < -1:
        movement = -1
    
    if pistonY + movement <280: #
        pistonY = 280

    if pistonY < 400 and abs(movement) <0.1:
        pistonY +=0.5

    pistonY -= movement
    

    for g in [grad1,grad2,grad3,grad4]:
        g[int(pistonY-2):int(pistonY+2), 10:215] = 0
        g[wall_mask] = 0



    shifted1 = cv.warpAffine(grad1, moveUp, (grad1.shape[1], grad2.shape[0]))
    shifted2 = cv.warpAffine(grad2, moveDown, (grad1.shape[1], grad1.shape[0]))
    shifted3 = cv.warpAffine(grad3, moveLeft, (grad1.shape[1], grad3.shape[0]))
    shifted4 = cv.warpAffine(grad4, moveRight, (grad1.shape[1], grad4.shape[0]))

    flow1 = cv.subtract(grad1,shifted2)
    flow2 = cv.subtract(grad2,shifted1)

    flow1_shifted = cv.warpAffine(flow1, moveUp, (grad2.shape[1], grad2.shape[0]))
    flow2_shifted = cv.warpAffine(flow2, moveDown, (grad1.shape[1], grad1.shape[0]))
    
    flow3 = cv.subtract(grad3,shifted4)
    flow4 = cv.subtract(grad4,shifted3)
    flow3_shifted = cv.warpAffine(flow3, moveLeft, (grad2.shape[1], grad2.shape[0]))
    flow4_shifted = cv.warpAffine(flow4, moveRight, (grad1.shape[1], grad1.shape[0]))


    density = cv.add(density,flow1)
    density = cv.subtract(density,flow1_shifted)
    density = cv.add(density,flow2)
    density = cv.subtract(density,flow2_shifted)
    density = cv.add(density,flow3)
    density = cv.subtract(density,flow3_shifted)
    density = cv.add(density,flow4)
    density = cv.subtract(density,flow4_shifted)

    tempreture = np.ones(grid_size,dtype=np.float32)

    k = cv.waitKey(5)
    if k == ord('x'):
        tempreture[410:470, 15:210] = 500
        # break
    if k == 27:
        break