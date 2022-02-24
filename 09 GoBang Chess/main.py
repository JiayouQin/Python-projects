import pygame as pg
import math
import time
import random

class Tile(): 
    def __init__(self,grid_size,screen_size,x,y): #一个坐标单位
        self.x,self.y = x,y
        self.grid_size = grid_size
        self.rectangle = (self.x*tile_size[0]+50,self.y*tile_size[1]+50,tile_size[0],tile_size[1])
        self.points = [ [(0.5+self.x)*tile_size[0]+50,self.y*tile_size[1]+50],    #upper middle
                [(0.5+self.x)*tile_size[0]+50,(self.y+1)*tile_size[1]+50],    #lower middle
                [(self.x)*tile_size[0]+50,(self.y+0.5)*tile_size[1]+50],    #middle left right
                  [(self.x+1)*tile_size[0]+50,(self.y+0.5)*tile_size[1]+50],    #middle right
                ] 
        self.chess = None

    def draw(self,color = (255,253,150),line_color = (150,175,255)): #x,y represents the tile coordinates  
        pg.draw.rect(screen,color,self.rectangle)
        pg.draw.line(screen,line_color,(self.points[0]),(self.points[1]),3)
        pg.draw.line(screen,line_color,(self.points[2]),(self.points[3]),3)
        if self.chess != None:
            screen.blit(chess[self.chess],((self.x+0.3)*tile_size[0] + 50, (self.y+0.3)*tile_size[1] + 50))
        pg.display.update()


def draw_chessboard():
    screen.fill((255,255,255))
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            matrix[y][x].draw()

def get_clicked_tile():
    x_,y_ = pg.mouse.get_pos() #pixel coordinates
    x = int((x_-50)/tile_size[0]) if int((x_-50)) >= 0 else -1
    y = int((y_-50)/tile_size[1]) if int((y_-50)) >= 0 else -1
    return x,y

def check_win(x,y):
    directions = [[(-1,0),(1,0)],[(0,-1),(0,1)],[(-1,1),(1,-1)],[(-1,-1),(1,1)]] #x,y
    for line in directions:
        depth=0 
        for dx,dy in line:
            tempx = dx
            tempy = dy
            if x+dx in range(grid_size[0]) and y+dy in range(grid_size[1]):
                while matrix[y+dy][x+dx].chess == matrix[y][x].chess and depth <= 5:
                    depth += 1
                    if depth == 4:
                        return matrix[y][x].chess
                    dx += tempx
                    dy += tempy
                    if x+dx not in range(grid_size[0]) or y+dy not in range(grid_size[1]):
                        break

def display_score():
    global turn
    player1_won_text = font.render(f': {player_won[0]}', True, (0,0,0), (255,255,255))
    player2_won_text = font.render(f': {player_won[1]}', True, (0,0,0), (255,255,255))
    turn_text = font.render(f'Turns: {turn}                                      ', True, (0,0,0), (255,255,255))
    screen.blit(player1_won_text,(1000,120))
    screen.blit(player2_won_text,(1000,220))
    screen.blit(chess_scoreboard[0],(900,100))
    screen.blit(chess_scoreboard[1],(900,200))
    screen.blit(turn_text,(900,300))
    pg.display.update()

def game_over_animation():
    for x in range(grid_size[0]+1):
        for y in range(grid_size[1]):
            if x +1 < grid_size[0]:
                matrix[y][x+1].chess = 2 if matrix[y][x+1].chess != None else None
                matrix[y][x+1].draw()
            if x < grid_size[0]:
                matrix[y][x].chess = 3
                matrix[y][x].draw()
            if x > 0:
                matrix[y][x-1].chess = None
                matrix[y][x-1].draw()
        time.sleep(0.05)

#================================initialize parameter===================================
chess_color = [(0,0,0),(255,255,255)]
screen_size = [1200,800]
chess_size = [800,800]
grid_size = [15,15]
tile_size = [(chess_size[0]-100)/grid_size[0],(chess_size[1]-100)/grid_size[1]]

run = True
game_ended = False
player_won = [0,0]
turn = 0
chess = [   pg.transform.smoothscale(pg.image.load('smiley.png'), (int(tile_size[0]/2),int(tile_size[0]/2))),   #player1
            pg.transform.smoothscale(pg.image.load('angry.png'), (int(tile_size[0]/2),int(tile_size[0]/2))),    #player2
            pg.transform.smoothscale(pg.image.load('sad.png'), (int(tile_size[0]/2),int(tile_size[0]/2))),    #sad face
            pg.transform.smoothscale(pg.image.load('fist.png'), (int(tile_size[0]/2),int(tile_size[0]/2)))]     #fist
chess_scoreboard = [   pg.transform.smoothscale(pg.image.load('smiley.png'), (80,80)),
                        pg.transform.smoothscale(pg.image.load('angry.png'), (80,80)),]

matrix = []
for y in range(grid_size[1]):
    temp = []
    for x in range(grid_size[0]):
        tile = Tile(grid_size,screen_size,x,y)
        temp.append(tile)
    matrix.append(temp)

screen = pg.display.set_mode(screen_size)
pg.init()
#================================draw board==============================================
draw_chessboard()
font = pg.font.Font('freesansbold.ttf', 32)
display_score()
#================================game loop==============================================
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                winner = (turn+1)%2
                print(f'player{(turn%2)+1} gave up')
                player_won[winner] += 1
                game_ended = True
                display_score()
        if event.type == pg.MOUSEBUTTONUP:
            if not game_ended:
                x,y = get_clicked_tile()
                if x in range(grid_size[0]) and y in range(grid_size[1]) and matrix[y][x].chess == None:
                    matrix[y][x].chess = turn%2
                    matrix[y][x].draw()
                    winner = check_win(x,y)
                    turn += 1
                    if winner != None:
                        print(f'the winner is: player{winner+1}')
                        player_won[winner] += 1
                        game_ended = True
                    display_score()
            else:
                game_over_animation()
                game_ended = False
                turn = 0
                display_score()
                for y in range(grid_size[1]):
                    for x in range(grid_size[0]):
                        matrix[y][x].chess = None
                        matrix[y][x].draw()
                
        time.sleep(1/30)