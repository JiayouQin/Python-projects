import pygame as pg
import time
import random

class Tile():
    def __init__(self,grid_size,screen_size,x,y):
        self.x,self.y = x,y
        self.connected = [0,0,0,0] # up,right,down,left 0 for not connected
        self.grid_size = grid_size
        self.tile_size = [(screen_size[0]-100)/grid_size[0],(screen_size[1]-100)/grid_size[1]]
        self.rectangle = (self.x*self.tile_size[0]+50,self.y*self.tile_size[1]+50,self.tile_size[0],self.tile_size[1])
        self.points = [ [self.x*self.tile_size[0]+50,self.y*self.tile_size[1]+50],    #uppper left
                [self.x*self.tile_size[0]+50+self.tile_size[0],self.y*self.tile_size[1]+50],    #upper right
                [self.x*self.tile_size[0]+50+self.tile_size[0],self.y*self.tile_size[1]+50+self.tile_size[1]],    #lower right
                [self.x*self.tile_size[0]+50,self.y*self.tile_size[1]+50+self.tile_size[1]],    #lower left
                ] 
        self.visited = False

    def draw(self,color = (255,253,150)): #x,y represents the tile coordinates  
        pg.draw.rect(screen,color,self.rectangle)
        for i in range(4):
            if not self.connected[i]:
                pg.draw.line(screen,(150,175,255),(self.points[i]),(self.points[((i+1)%4)]),5)


def walk_maze(path):
    global tile_covered
    x,y = path[-1]

    if x < 0 or x >= grid_size[0] or y < 0 or y >= grid_size[1]:
        print(f'index out of range at {x,y}')
        return
    matrix[y][x].draw()
    if matrix[y][x].visited:
        print(f'node already visited at {x,y}')
        
        return
    elif tile_covered <= grid_size[0]*grid_size[1]:
        tile_covered += 1
        print(x,y)
        matrix[y][x].visited = True

        path_choice = [0,1,2,3]
        random.shuffle(path_choice)
        directions = [[0,-1],[1,0],[0,1],[-1,0]] # up,right,down,left 0 for not connected


        for i in path_choice:
            x_,y_ = x+directions[i][0],y+directions[i][1]
            path.append([x_,y_])
            if walk_maze(path):
                matrix[y][x].connected[i] = 1 #walls of current node
                matrix[y_][x_].connected[(i+2)%4] = 1#reverse the vector direction
                matrix[y][x].draw()
                matrix[y_][x_].draw()

            path.pop(-1)
        pg.display.update()


        return True

    else:
        print('all node visited')
        return


screen_size = [800,800]
grid_size = [40,40]
exit = [10,10]
tile_covered = 0
run = True

screen = pg.display.set_mode(screen_size)

matrix = []
for y in range(grid_size[1]):
    temp = []
    for x in range(grid_size[0]):
        tile = Tile(grid_size,screen_size,x,y)
        temp.append(tile)
    matrix.append(temp)

matrix[0][0].connected[2] = True

pg.init()
path = [[0,0]]

screen.fill((255,255,255))
walk_maze(path)

pg.display.update()

print('======== Generation Finished ========')
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            time.sleep(0.1)
            pg.quit()
            exit()
