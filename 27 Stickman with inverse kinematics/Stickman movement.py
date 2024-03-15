#!/usr/bin/env python
# coding: utf-8

# In[243]:


'''
J.Qin 03/14/2024

Procedural movement with inverse kinematics and perlin noise
Terrain is generated in real time

Ps: sometimes there is no solution for the system and error will occur

'''
import numpy as np
import cv2 as cv
from perlin_noise import PerlinNoise
from collections import deque

noise1 = PerlinNoise(octaves=3.5)
noise2 = PerlinNoise(octaves=15)
step = 1/size[0]

def inverse_kinematics(x,y,l1,l2):
    '''
    analytical approach of 2 linkage system
    '''
    temp = (x**2+y**2-l1**2-l2**2) / (2*l1*l2)
    theta2 = np.arccos(temp)
    x_dot = x*(l1+l2*np.cos(theta2)) + y *(l2 * np.sin(theta2))
    y_dot = y*(l1+l2*np.cos(theta2)) - x *(l2 * np.sin(theta2))
    theta1 = np.arctan2(y_dot,x_dot)
    return (theta1,theta2)

def foward_kinematics(theta,l):
    return np.array([np.cos(theta)*l, np.sin(theta)*l])

def get_height():
    global current_seed
    current_seed += step
    n = noise1(current_seed)*0.3
    n += noise2(current_seed)*0.1
    height = size[1]-int(100+n*size[1]/2)
    return height

def run_leg(pos,dx,dy,l1,l2):
    #leg position
    theta1,theta2 = inverse_kinematics(dx, dy, leg_len1, leg_len2)
    d1 = pos + foward_kinematics(theta1,leg_len1) 
    d2 = d1 + foward_kinematics(theta1+theta2,leg_len2)
    cv.line(img,pos, d1.astype(int), (255,255,255),2)
    cv.line(img,d1.astype(int),d2.astype(int),(255,255,255),2)

#generate terrain
current_seed = 0
size = (512,512,3)
canvas = np.zeros(size,dtype=np.uint8)
heights = deque()

for i in range(size[0]):
    h = get_height()
    heights.append(h)
    canvas[h:,i] = [128,128,0]
#position of the runner
pause = False
moving = True
left = True
dx = 0
increment = -1
pos = np.array([int(size[0]/2),heights[int(size[1]/2)]-100] )
y_target = heights[int(size[1]/2)]-100
while True:
    img = canvas.copy()
    
    l1 = 90 #leg length
    l2 = 100
    
    if abs(dx)==50:#leg movement is a cyclic function
        increment = -increment
        left ^= True
    if pos[1]-y_target > 0:
        pos[1] -= 1
    elif pos[1]-y_target < 0:
        pos[1] += 1
    
    dx = dx + increment
    
    pos1 = pos + np.array([15,0]) #offset of the first leg
    dy1 = heights[pos1[0]+dx] - pos1[1]
    pos2 = pos + np.array([-15,0]) #offset of the right leg
    dy2 = heights[pos2[0]-dx] - pos2[1]
    
    if left:
        dy2 -= -abs(dx)/50*20+20
        y_target = heights[pos1[0]+dx]-100
    else:
        dy1 -= -abs(dx)/50*20+20
        y_target = heights[pos2[0]-dx]-100
        
    run_leg(pos1,dx,dy1,l1,l2)
    run_leg(pos2,-dx,dy2,l1,l2)
    
    #draw the body
    theta = np.pi/50*abs(dx)*0.3
    arm_base = pos + np.array([0,-80])
    d = foward_kinematics(theta,100)
    arm_pos1 = arm_base + d
    arm_pos2 = arm_pos1.copy()
    arm_pos2[0] -= d[0]*2
    
    cv.line(img,arm_base, arm_pos1.astype(int), (255,255,255),2)
    cv.line(img,arm_base, arm_pos2.astype(int), (255,255,255),2)
    cv.line(img,pos1, pos2, (255,255,255),2)
    cv.line(img,pos, pos-np.array([0,100]), (255,255,255),2)
    cv.circle(img, pos-np.array([0,130]), 30, (255,255,255), 2) 
    
    cv.imshow('canvas',img)

    #move right
    if moving:
        heights.popleft()
        h = get_height()
        canvas = np.roll(canvas, -1,axis=1)
        canvas[:,size[0]-1] = [0,0,0]
        canvas[h:,size[0]-1] = [128,128,0]
        heights.append(h)    
    
    k = cv.waitKey( 1& (not pause))
    if k == 27:
        break
    if k == 13:
        pause ^= True
        
cv.destroyAllWindows()


# In[ ]:





# In[ ]:




