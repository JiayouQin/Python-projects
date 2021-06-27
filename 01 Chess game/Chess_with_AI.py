import random

def checkwin(chess,chessplaced): #check if the game is won
    originalchess = chessplaced
    chess = chess
    #print(chessplaced)
    #check if is someone  have won
    end = (chessplaced[1-1] == chessplaced[2-1] == chessplaced [3-1]) or \
            (chessplaced[4-1] == chessplaced[5-1] == chessplaced[6-1]) or \
            (chessplaced[7-1] == chessplaced[8-1] == chessplaced[9-1]) or \
            (chessplaced[1-1] == chessplaced[4-1] == chessplaced[7-1]) or \
            (chessplaced[2-1] == chessplaced[5-1] == chessplaced[8-1]) or \
            (chessplaced[3-1] == chessplaced[6-1] == chessplaced[9-1]) or \
            (chessplaced[1-1] == chessplaced[5-1] == chessplaced[9-1]) or \
            (chessplaced[7-1] == chessplaced[5-1] == chessplaced[3-1])
    #print(end)
    
    if end == True:
        if chess == "X": #this condition is reversed
            #print("X wins one time")
            return -1
        elif chess == "O":
            #print("O wins one time")
            return 1
    else:
        return 0
    
def anotherchess(chess):
    if chess == "O":
        return "X"
    elif chess == "X":
        return "O"

def occupied(chess):
    if chess == "X": #make the AI don't want to place on the existing chess
        return 999
    elif chess == "O":
        return -999
    
    
def evluate_player(chess,chessplaced): # input should be opponent if the AI sees that the player could win the game the score will drop by 10
    #print(f"thinking about human moves, his chess would be {chess}")
    score = 0
    for i in range(len(chessplaced)):
        if chessplaced[i] != "X" and chessplaced[i] != "O":
            #print(f"thinking about human move on {i+1}")
            chessplaced[i] = chess #change the chessboard temporarily
            temp = checkwin(chess,chessplaced) 
            score += temp
            #print(f"think this score is {temp}")
            chessplaced[i] = str(i+1)   #reset the board
            if chess == "O" and temp == 1: #if O have won
                #print("the Human O will win! Not @ccept@ble!!!")
                return 1
            elif chess == "X" and temp == -1:# if X have won
                #print("the Human X will win! Not @ccept@ble!!!")
                return  -1
    return score

def evaluate(chess,chessplaced): #evaluates the current situation, should not be used seperately
    weight = [0,0,0,0,0,0,0,0,0]
    
    for i in range(len(chessplaced)):#check if AI will win after placing a chess
        score = 0
        if chessplaced[i] != "X" and chessplaced[i] != "O":
            #print(f"trying to place {chess} on {i+1}")
            chessplaced[i] = chess
            if checkwin(chess,chessplaced) == 0:# if the AI did not win, it will check for possible player move
                #print(f"will not win if placing on {i}, think about opponent move")
                score += evluate_player(anotherchess(chess),chessplaced) # consider what human player will do
                #print(f"the score will be {score}")
            else: #in this case the AI only consider if someone will win, since it is his move
                #print(f"if place chess in {i} the AI will win")
                score += checkwin(chess,chessplaced)
                #print(f"score of the move is:")
            chessplaced[i] = str(i+1)
            weight[i]= score
        else:
            weight[i] = occupied(chess)
    #print(weight)
    return weight

    
    
    
def decide(chess,chessplaced): #will eventually return a index number
    weight = evaluate(chess,chessplaced)
    temp =[]
    if chess == "X":
        for i in range(len(weight)):
            min_index = min(weight)
            if weight[i] == min_index:
                temp.append(i)
        return random.choice(temp)
    if chess == "O":
        for i in range(len(weight)):
            max_index = max(weight)
            if weight[i] == max_index:
                temp.append(i)
        return random.choice(temp)

def gameoverUI():
    print("__  __ `/  __ `/_  __ `__ \  _ \    _  __ \_ | / /  _ \_  ___/")
    print("_  /_/ // /_/ /_  / / / / /  __/    / /_/ /_ |/ //  __/  / ")
    print("_\__, / \__,_/ /_/ /_/ /_/\___/     \____/_____/ \___//_/ ")
    print("/____/")

def chessUI(chessplaced,player1,player2):
    print("(_______)(_)          _                     _                  ")
    print(" _        _   ____   | |_    ____   ____   | |_    ___    ____ ")
    print("| |      | | / ___)  |  _)  / _  | / ___)  |  _)  / _ \  / _  )")
    print("| |_____ | |( (___   | |__ ( ( | |( (___   | |__ | |_| |( (/ / ")
    print(" \______)|_| \____)   \___) \_||_| \____)   \___) \___/  \____)")

    print (f"Player1 has Chosen {player1}, Player2 will be {player2}")
    
    print("-------------------------")
    print(f"|   {chessplaced[7-1]}   |   {chessplaced[8-1]}   |   {chessplaced[9-1]}   |")
    print("-------------------------")
    print(f"|   {chessplaced[4-1]}   |   {chessplaced[5-1]}   |   {chessplaced[6-1]}   |")
    print("-------------------------")
    print(f"|   {chessplaced[1-1]}   |   {chessplaced[2-1]}   |   {chessplaced[3-1]}   |")
    print("-------------------------")

def Playerchooseside():
    player1 = ""
    print ("Welcome to the Tic Tac Toe!")
    while player1 != "X" and player1 != "O":
        player1 = input ("Player 1 please choose to be X or O: ")
        player1 = player1.upper()
    if player1 == "X":
        player2 = "O"
    else:
        player2 = "X"
    return (player1,player2)

def Playerplacechess():
    #initialize
    import random
    playagain = ""
    #main
    
    while playagain != "n":
        (player1,player2) = Playerchooseside()
        winner = 0
        gameturn = 0
        whosturn = random.randint(1,2)
        chessplaced = ["1","2","3","4","5","6","7","8","9"]
        placechessindex = 0
        while winner != 1 and winner != 2:
            #print UI
            from IPython.display import clear_output
            clear_output()
            chessUI(chessplaced,player1,player2)
            #check game state
            
            if (chessplaced[1-1] == chessplaced[2-1] == chessplaced [3-1]) or \
            (chessplaced[4-1] == chessplaced[5-1] == chessplaced[6-1]) or \
            (chessplaced[7-1] == chessplaced[8-1] == chessplaced[9-1]) or \
            (chessplaced[1-1] == chessplaced[4-1] == chessplaced[7-1]) or \
            (chessplaced[2-1] == chessplaced[5-1] == chessplaced[8-1]) or \
            (chessplaced[3-1] == chessplaced[6-1] == chessplaced[9-1]) or \
            (chessplaced[1-1] == chessplaced[5-1] == chessplaced[9-1]) or \
            (chessplaced[7-1] == chessplaced[5-1] == chessplaced[3-1]):
                if whosturn == 1:
                    winner = 2
                else:
                    winner = 1
                break
            if gameturn >= 9 and winner == 0:
                print ("The game is drawn")
                break
            else:
                while whosturn == 1:
                    print (f"Player{whosturn} will take the turn")
                    placechessindex = input (f"Player{whosturn} please place your Chess (give 1-9 to place Chess or g to give up)")
                    if placechessindex.isdigit() and int(placechessindex) in range (1,10):
                        placechessindex = int(placechessindex) - 1
                        if chessplaced[placechessindex] != "X" and chessplaced[placechessindex] != "O":
                            break
                    elif placechessindex == "g":
                        print (f"Player{whosturn} has just given up.")
                        if whosturn == 1:
                            winner == 2
                        elif whosturn == 2:
                            winner == 1
                        break
                    else:
                        continue
                if whosturn == 1 :
                    chessplaced[placechessindex] = player1
                    whosturn = 2
                    gameturn += 1
                else:
                    aiindex = decide(player2,chessplaced)
                    chessplaced[aiindex] = player2
                    whosturn = 1
                    gameturn += 1
        if winner == 1 or winner == 2:
            print(f"The winner is: Player{winner}")
        while playagain != "y" and playagain != "n":
            gameoverUI()
            playagain = input("Would you like to Play again? y/n")
            playagain = playagain.lower()

Playerplacechess()
