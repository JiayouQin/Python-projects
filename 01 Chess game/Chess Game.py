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
                while True:
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
                    chessplaced[placechessindex] = player2
                    whosturn = 1
                    gameturn += 1
        if winner == 1 or winner == 2:
            print(f"The winner is: Player{winner}")
        while playagain != "y" and playagain != "n":
            gameoverUI()
            playagain = input("Would you like to Play again? y/n")
            playagain = playagain.lower()

Playerplacechess()