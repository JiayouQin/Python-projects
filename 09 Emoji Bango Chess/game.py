"""
created for jupyter note book, just a simple bango chess with emojis
"""

from IPython.display import clear_output
import time

def gameover():
    for y in range(chessboard_length):
        for x in range (chessboard_length):
            if y<8:
                chessboard[x][y+1]="🤜🏻"
                if  y<7 and  chessboard[x][y+2] != " ":
                    
                    chessboard[x][y+2]="😫"
            chessboard[x][y]=" "
        time.sleep(0.3)
        clear_output()
        printUI(chessboard)
        time.sleep(0.3)

def printUI(chessboard):
    print(" /|\tA\tB\tC\tD\tE\tF\tG\tH\tI")
    for i in range(len(chessboard)):
        print(f"{i+1}/|\t{chessboard[i][0]}\t{chessboard[i][1]}\t{chessboard[i][2]}\t{chessboard[i][3]}\t{chessboard[i][4]}\t{chessboard[i][5]}\t{chessboard[i][6]}\t{chessboard[i][7]}\t{chessboard[i][8]}")
        print(" /|-----------------------------------------------------------------------")
    print(f"Current Player: {currentplayer}")
    print(f"Winner: {winner}")

def checkwin(chessboard,axisX,axisY):
    axisY -= 1
    chess = chessboard[axisY][axisX]
    #print(chess)
    #print(chr(64+axisX+1),axisY+1)
    directions = [[(-1,0),(1,0)],[(0,-1),(0,1)],[(-1,1),(1,-1)],[(-1,-1),(1,1)]] #x,y
    for line in directions:
        depth=0 #depth means the samme chess that has been checked
        for x,y in line:
            #print(f"checking on vector {x},{y}")
            tempx = x
            tempy = y
            while chessboard[axisY+y][axisX+x] == chess and depth <= 5:
                #print(f"chess is the same on vector {x},{y}")
                #print(chessboard[axisY+y][axisX+x])
                depth+=1
                #print(f"depth: {depth}")
                x +=tempx
                y +=tempy
                #print(f"next chess is {chessboard[axisY+y][axisX+x]}")
                if depth == 4:
                    return chess
        #print("-------checking another line---------")
    return " "
def placechess(x,y,chess,chessboard):
    #print(chessboard[int(y)][int(x)])
    if chessboard[int(y)-1][int(x)] == " ":
        chessboard[int(y)-1][int(x)]= chess
        return chessboard

    
def changeplayer(player):
    if player == "😠":
        return "😅"
    else:
        return "😠"
        
    
chessboard = []
axisX=[]

chessboard_length = 9
for y in range(chessboard_length):
    for x in range(1,chessboard_length+1):
        axisX.append(" ")
    chessboard.append(axisX)
    axisX = []
    
winner = " "
player1 = "😠"
player2 = "😅"
currentplayer = "😠" #
playagain = ""

while playagain != "n":
    playagain = ""
    validinput = False
    printUI(chessboard)
    #----------------------------------- main game loop
    while validinput == False:
        try:
            playerinput = input("输入棋盘坐标")
            xmap = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8}
            axisX=xmap[playerinput[0]]
            axisY=int(playerinput[1:])
            if playerinput[0] in xmap:
                if 1<= axisY <= chessboard_length:
                    #print(f"Trying to put {currentplayer} onto:{axisX}，{axisY}")

                    if chessboard[axisY-1][axisX] == " ":
                        # I know this is messy, but it sort of works
                        chessboard = placechess(axisX,axisY,currentplayer,chessboard) #x,y,playerchess
                        validinput = True
        except:
            pass
        winner = checkwin(chessboard,axisX,axisY)
        if winner != " ":
            print(f"{winner} 赢了")
            playagain = input("再来一把吗？(y/n)")
            while playagain not in ["y","n"]:
                print("请输入有效数据")
                playagain = input("再来一把吗？(y/n)")
            gameover()
            break
        
    clear_output()
    currentplayer = changeplayer(currentplayer)
    
    #----------------------------------- game over
