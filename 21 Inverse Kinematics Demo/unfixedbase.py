import pygame as pg
import time
import random
import math
import sys


class joints():
    x = 0
    y = 0
    angle = 0
    length = 0
    x_, y_ = 0,0
    color = (255,255,255)
    parent = None
    def __init__(self, x, y, angle, length, parent = None):
        self.x = x #initial point
        self.y = y
        self.x_ = 0 #endpoint
        self.y_ = 0
        self.angle = angle
        self.length = length    #given length of the arm
        if parent:  #parent's end point is the base point of the joint
            self.parent = parent

    def inverse(self):
        dx = self.x_ - self.x 
        dy = self.y_ - self.y
        self.angle = math.atan2(dy,dx) #calculate the angle from desired end point to base
        self.x = -self.length * math.cos(self.angle) + self.x_  
        self.y = -self.length * math.sin(self.angle) + self.y_  #project the length back and reset base

        

    def calc(self): #calculation of inverse kinematics
        self.inverse()
        if self.parent:
            self.parent.x_ = self.x
            self.parent.y_ = self.y
            self.parent.calc()  # after finished calculate parent joint
        self.draw()

    def draw(self):
        pg.draw.line(screen,self.color,(self.x,self.y),(self.x_,self.y_),3)
        

screen_size = [800,800]
grid_size = [40,40]
exit = [10,10]
tile_covered = 0
run = True
screen = pg.display.set_mode(screen_size)

pg.init()
path = [[0,0]]

pg.display.update()
joint1 = joints(100,100,0,100)
joint2 = joints(100,100,0,150,joint1)
joint3 = joints(100,100,0,50,joint2)
joint4 = joints(100,100,0,80,joint3)

while run:
    x,y = pg.mouse.get_pos()
    screen.fill((0,0,0))
    joint4.x_,joint4.y_ = x, y
    joint4.calc()
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            time.sleep(0.1)
            pg.quit()
            sys.exit()