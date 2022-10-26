import cv2 as cv
import cvsimpton as cvs
import numpy as np

def converge(image, k_size, gaussian_kernel=True):
    '''
    high pass filter via kernel convolution, low frequency signals will be merged into the average mean.
    if gaussian kernel is true then a gaussian kernel will be used, otherwise a mean kernel.
    '''
    image = image.astype(np.float32)/255
    average_color = cv.mean(image)
    if gaussian_kernel:
        blurred = cv.GaussianBlur(image,(k_size,k_size),0)
    else:
        blurred = cv.blur(image, (k_size, k_size))
    sub = blurred - average_color[:3]
    result = image - sub
    norm = cv.normalize(result, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
    return norm
