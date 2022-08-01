import cv2 as cv
import cvsimpton as cvs
import numpy as np

path = './'
k_size = 25
kernel = np.ones((k_size, k_size))/k_size**2;
images = cvs.load_path(path)
print(images )

for i in range(len(images)):
    image = cv.imread(images[i]).astype(np.float32)/255
    # convolved = cv.filter2D(src=image, kernel=kernel, ddepth=-1)
    average_color = cv.mean(image)
    blurred = cv.blur(image, (k_size, k_size))

    sub = blurred - average_color[:3]
    result = image - sub

    cvs.imshow('image')
    for name in ['image', 'sub', 'result', 'blurred']:
        cvs.imshow(name)
    k = cv.waitKey(0)
    if k == 27:
        break
