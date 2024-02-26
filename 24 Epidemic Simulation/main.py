'''
jiayou Qin 02/26/2024
Using openCV to simulate epidemic spread in celluar automata with SIRV model
0,1 represent vaccinated and recovered respectively, 2 represents susceptible and value over 100
represents infected with the tenth digit used as timer(10 per step)
the value should not go above 190
'''

import cv2 as cv
import numpy as np


infection_time = 3 # Do ausolutely not exceed 9
pixVal = int(100+10*infection_time)
SIZE = (1024,960,3)
density = 0.3 #vaccinated density
#generate random initial value
image = np.random.choice([0,2],size=SIZE[:2],p=[density,1-density]).astype(np.uint8)
image[120:150, 200:210] = pixVal
image = cv.rectangle(image, (100,180), (160,220), 0, 2) #fire wall test

kernel = np.asarray([[1,1,1],
                     [1,100,1],
                     [1,1,1]],dtype='uint8')

outputBuffer = np.zeros(SIZE,dtype=np.uint8)
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.waitKey(0)
while True:
    convolved = cv.filter2D(src=image, ddepth=cv.CV_16U, kernel=kernel,borderType=cv.BORDER_CONSTANT)
    #populated:
    mask1 = convolved>=400      #susceptible person that would get infected
    mask2 = convolved<=10000    #if value is larger, cell is already infected
    mask3 = image >= 2          #pixel value must be greater or equal to 2 (igore 0 and 1)
    mask = np.logical_and(mask2,mask1)
    mask = np.logical_and(mask,mask3)

    image[mask]=pixVal
    image[image>=100] -= 10           #decrement timer
    image[image==90] = 1              #recovered

    #for better visialization:
    outputBuffer[image==0] = [0,255,0]          #vaccinated
    outputBuffer[image==1] = [0,255,255]        #recovered
    outputBuffer[image==2] = [255,255,255]      #susceptible
    outputBuffer[image>=100] = [0,0,255]        #infected

    cv.imshow('image',outputBuffer)

    key = cv.waitKey(10)
    if key == 27:
        break