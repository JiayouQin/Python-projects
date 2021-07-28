"""
A crappy game I create, in this game you can grab crates from a transport band and move it to another one.
you can use Q and E to rotate the crates, however it is not required
another game to waste your precious time, feel the power of jack ma
"""


import pygame
import random

class boxes():
    def __init__(self):
        self.grabbed = False
        self.rotation = 0
        self.box=pygame.image.load('box.jpg').convert()
        self.box.set_colorkey((0,0,0))
        self.size=(self.box.get_width(),self.box.get_height())
        self.geometry = [random.randint(580,640),0,40,40]
        
    def draw(self):
        if self.grabbed == True:
            self.geometry[0] = arm.arm_coordinates[0]
            self.geometry[1] = arm.arm_coordinates[1]
        box_copy = pygame.transform.rotate(self.box,self.rotation).copy()
        width,height = int(box_copy.get_width()/2),int(box_copy.get_height()/2)
        screen.blit(box_copy,(self.geometry[0]-width,self.geometry[1]-height))
        if self.geometry[0] <= 0:
            print(box_list.index(self))
            try:
                box_list.pop(box_list.index(self))
            except:
                pass
class boxes_3():
    def __init__(self):
        self.size = (140,46)
        self.geometry = [random.randint(600,620),0,140,46]
        self.grabbed = False
        self.rotation = 0
        
        self.box=pygame.image.load('3boxes.jpg').convert()
        self.box.set_colorkey((0,0,0))

        
    def draw(self):
        if self.grabbed == True:
            self.geometry[0] = arm.arm_coordinates[0]
            self.geometry[1] = arm.arm_coordinates[1]
        box_copy = pygame.transform.rotate(self.box,self.rotation).copy()
        width,height = int(box_copy.get_width()/2),int(box_copy.get_height()/2)
        screen.blit(box_copy,(self.geometry[0]-width,self.geometry[1]-height))
        if self.geometry[0] < 0:
            print(box_list.index(self))
            try:
                box_list.pop(box_list.index(self))
            except:
                print(box.geometry)
            
            
def transport_belt():
    belt1=(580, 0, 120, 360)
    pygame.draw.rect(screen, (40,200,40), belt1)
    belt2=(0, 400, 560, 120)
    pygame.draw.rect(screen, (40,200,40), belt2)
    
    
    for box in box_list:
        if belt1[0] <= box.geometry[0]<= belt1[0]+belt1[2]\
        and box.geometry[1]<= belt1[3]\
        and box.grabbed == False:
            
            box.geometry[1] += 1
            
        if 0<= box.geometry[0]<=belt2[2]\
        and belt2[1] <= box.geometry[1] <= belt2[1]+belt2[3]\
        and box.grabbed == False:
            
            box.geometry[0] -= 1

    
class mech_arm():
    def __init__(self):
        self.base_position=(640,450)
        self.r = 240 # arm length
        self.arm_width = 15
        last_pos = None
        self.arm_coordinates=(640,450)
        self.occupied = False
        self.grabbed = None
    def draw(self):
        pygame.draw.circle(screen, (255,100,120), self.base_position, 30, 5)
        x,y = pygame.mouse.get_pos()
        delta_x = x-self.base_position[0]
        delta_y = y-self.base_position[1]
        delta_length = (delta_x**2+delta_y**2)**0.5
        if delta_length <= self.r:
            self.arm_coordinates = (x,y)
        else:
            k = self.r/delta_length
            self.movement_delta=(delta_x*k+self.base_position[0]-self.arm_coordinates[0],delta_y*k+self.base_position[1]-self.arm_coordinates[1])
            self.arm_coordinates = (delta_x*k+self.base_position[0],delta_y*k+self.base_position[1])
        pygame.draw.line(screen, (200,10,200), self.base_position, self.arm_coordinates, self.arm_width)
    
def redraw():
    for box in box_list:
        box.draw()
    arm.draw()
pygame.init()
screen = pygame.display.set_mode([1280, 720])

box_list = []
cycling = 0
running = True
arm = mech_arm()

while running:
    cycling+=1
    if cycling >60:
        cycling = 0
    if len(box_list) < 3 and cycling == 0:
        box_list.append(random.choice([boxes(),boxes(),boxes_3()]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            arm.occupied = False
            arm.grabbed = None
            for box in box_list:
                box.grabbed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if arm.grabbed != None:
                    arm.grabbed.rotation -= 5
                    
            if event.key == pygame.K_e:
                if arm.grabbed != None:
                    arm.grabbed.rotation += 5
            
            
        if pygame.mouse.get_pressed()[0]:
            x,y = arm.arm_coordinates
            for box in box_list:
                if box.geometry[0]-int(box.size[0]/2) <= x <= box.geometry[0]+int(box.size[0]/2)\
                and box.geometry[1]-int(box.size[1]/2) <= y <= box.geometry[1]+int(box.size[1]/2)\
                and arm.occupied == False:
                    box.grabbed = True
                    arm.grabbed = box
                    arm.occupied = True



    # Fill the background with white
    screen.fill((255, 255, 255))

    
    transport_belt()
    redraw()
    pygame.display.flip()
    pygame.time.Clock().tick(30)
pygame.quit()
