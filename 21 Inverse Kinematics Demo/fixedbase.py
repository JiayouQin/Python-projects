import pygame as pg
import time
import random
import math
import sys


class Joints():
    x = 0
    y = 0
    angle = 0
    length = 0
    x_, y_ = 0,0
    color = (255,255,255)
    parent = None
    child = None
    index = 0
    total_joints = []

    def __init__(self, x, y, angle, length):
        
        self.x = x #initial point
        self.y = y
        self.x_ = 0 #endpoint
        self.y_ = 0
        self.angle = angle
        self.length = length    #given length of the arm
        self.base = (int(screen_size[0]/2),int(screen_size[1]/2))   #base of arm
        self.index = len(Joints.total_joints)
        Joints.total_joints.append(self)
        if self.index != 0:  #parent's end point is the base point of the joint
            self.parent = Joints.total_joints[self.index-1]
            self.parent.child = self    #provide link from both ends, double linked list

    def inverse(self):
        dx = self.x_ - self.x 
        dy = self.y_ - self.y
        self.angle = math.atan2(dy,dx) #calculate the angle from desired end point to base
        self.x = -self.length * math.cos(self.angle) + self.x_  
        self.y = -self.length * math.sin(self.angle) + self.y_  #project the length back and reset base
        if self.parent:
            self.parent.x_ = self.x
            self.parent.y_ = self.y
            self.parent.inverse()
        

    def foward(self):
        if self.parent:
            self.x,self.y = self.parent.x_, self.parent.y_
        else:
            self.x,self.y = self.base
        self.x_ = self.length * math.cos(self.angle) + self.x  
        self.y_ = self.length * math.sin(self.angle) + self.y  #project the length back and reset base
        self.draw()
        if self.child:
            self.child.foward()
                
    def draw(self):
        pg.draw.line(screen,self.color,(self.x,self.y),(self.x_,self.y_),3)

    @staticmethod
    def calc(x,y):
        end_joint = Joints.total_joints[-1]
        end_joint.x_, end_joint.y_ = x, y
        end_joint.inverse()
        Joints.total_joints[0].foward()


screen_size = [800,800]
grid_size = [40,40]
exit = [10,10]
tile_covered = 0
run = True
screen = pg.display.set_mode(screen_size)

pg.init()
path = [[0,0]]

pg.display.update()

Joints(100,100,0,100)
Joints(100,100,0,150)
Joints(100,100,0,50)
Joints(100,100,0,80)

while run:
    x,y = pg.mouse.get_pos()
    screen.fill((0,0,0))
    Joints.calc(x,y)
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            time.sleep(0.1)
            pg.quit()
            sys.exit()
