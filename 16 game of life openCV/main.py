import cv2 as cv
import numpy as np

image = cv.imread('John_H_Conway_2005_(cropped).jpg',0)
convolved = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,5)

threshed_value = (convolved/255).astype(np.uint8)

kernel = np.asarray([[1,1,1],
                     [1,10,1],
                     [1,1,1]],dtype='uint8')

for name in ['convolved']:
    cv.namedWindow(name,cv.WINDOW_NORMAL)
    cv.imshow(name,eval(name))

key = cv.waitKey(0)

mode = True

while True:

    cv.imshow('convolved',convolved)

    key = cv.waitKey(10)
    if key == 27:
        break

    convolved = cv.filter2D(src=threshed_value, ddepth=cv.CV_8U, kernel=kernel,borderType=cv.BORDER_CONSTANT)

    #populated:
    convolved[convolved==10] = 0    #solitude
    convolved[convolved==11] = 0 
    convolved[convolved>=14] = 0
    #unpopulated:
    convolved[convolved==3] = 255   #revived
    #binarize again
    convolved[convolved>10] = 255
    convolved[convolved<10] = 0

    ret,threshed_value = cv.threshold(convolved,10,1,cv.THRESH_BINARY)
