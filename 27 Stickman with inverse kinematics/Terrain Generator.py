#!/usr/bin/env python
# coding: utf-8

# In[38]:


'''
J.Qin 03/14/2024
A simple implementation to generate continuous terrain for testing purpose
'''


import numpy as np
import cv2 as cv
from perlin_noise import PerlinNoise

def get_height():
    global current_seed
    current_seed += step
    n = noise(current_seed)
    n += noise2(current_seed)*0.2
    height = size[1]-int(100+n*size[1]/2)
    return height

size = (512,512)
canvas = np.zeros(size,dtype=np.uint8)
noise1 = PerlinNoise(octaves=1)
noise2 = PerlinNoise(octaves=15)
step = 1/size[0]
current_seed = 0
heights = []

for i in range(size[0]):
    
    canvas[get_height():,i] = 255
    
while True:
    
    canvas[get_height():,size[0]-1] = 255
    canvas = np.roll(canvas, -1)
    cv.imshow('canvas',canvas)
    k = cv.waitKey(1)
    if k == 27:
        break
        
cv.destroyAllWindows()


# In[22]:


print(type(n))


# In[ ]:




