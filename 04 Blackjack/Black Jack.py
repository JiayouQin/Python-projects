#!/usr/bin/env python
# coding: utf-8

# In[7]:


import random
from IPython.display import clear_output

class Deposit():
    def __init__(self,chip):
        self.chip = chip
    def takechip(self,betsum):
        self.chip -= betsum
    def winning(self, betsum):
        self.chip += betsum*2
    def losing(self, betsum): #unused function
        pass
    
class HoldingCards():
    def reset(self):
        self.cards = []
    def __init__(self):
        self.cards = []
    def drawcards(self,n):
        while n > 0:
            x = random.randint(0,12)
            y = random.randint(0,3)
            if carddecktemp[y][x] != ():
                self.cards.append(carddecktemp[y][x])
                carddecktemp[y][x] = ()
                n -= 1
    def checksum(self): #return True for busted
        countA = 0
        cardsum = 0
        for i in range (len(self.cards)):
            face,pattern = self.cards[i]
            if face == "A":
                countA += 1
                cardsum += 11
            elif face == ("J") or face == ("Q") or face == ("K"):
                cardsum += 10
            else:
                cardsum += int(face)
        while cardsum > 21 and countA != 0:
            cardsum -= 10
            countA -= 1
        return cardsum
    
def printui():
    clear_output()
    print("\33[1;39;40m                                                                          ")
    print("---------------------------------------dealer deck------------------------\33[1;39;42m")
    print(f"Card1 not fliped {dealercards.cards[1:]}")
    print(f"        Card value: ???                                                   ")
    print(f"        Dealer currency: {dealerchip.chip}                                             ")
    print("\33[1;39;40m                                                                          ")
    print("---------------------------------------player deck------------------------\33[1;39;42m")
    print(f"{playercards.cards}")
    print(f"        Card value: {playercards.checksum()}                                                       ")
    print(f"        Player currency: {playerchip.chip}                                                ")
    print("                                                                           ")
    print(f"                    current bet: {betsum}                                        ")
def printui_result():
    clear_output()
    print("\33[1;39;40m                                                                          ")
    print("---------------------------------------dealer deck------------------------\33[1;39;42m")
    print(f"{dealercards.cards[:]}")
    print(f"        Card value: {dealercards.checksum()}                                                   ")
    print(f"        Dealer currency: {dealerchip.chip}                                             ")
    print("\33[1;39;40m                                                                          ")
    print("---------------------------------------player deck------------------------\33[1;39;42m")
    print(f"{playercards.cards}")
    print(f"        Card value{playercards.checksum()}                                                       ")
    print(f"        Player currency: {playerchip.chip}                                                ")
    print("                                                                           ")
    print(f"                    current bet: {betsum}                                        ")

def gameover_ui():
    print("   _________    _____   ____     _______  __ ___________ ")
    print("  / ___\__  \  /     \_/ __ \   /  _ \  \/ // __ \_  __ \ ")
    print(" / /_/  > __ \|  Y Y  \  ___/  (  <_> )   /\  ___/|  | \/ ")
    print(" \___  (____  /__|_|  /\___  >  \____/ \_/  \___  >__| ")
    print(" \___  (____  /__|_|  /\___  >  \____/ \_/  \___  >__| ")
    print("/_____/     \/      \/     \/                   \/ \n")
    print("Did you lose all your money to this??? Come on this is easy!!!!!!")
    
    
carddeck = [
#note that to access the card value use carddeck[y][x].Y:0-3 clubs,spades,hearts,dimonds
#X: 0-12 A,2-9,JQK
    [("A","clubs"),("2","clubs"),("3","clubs"),("4","clubs"),("5","clubs"),("6","clubs"),("7","clubs"),("8","clubs")
     ,("9","clubs"),("10","clubs"),("J","clubs"),("Q","clubs"),("K","clubs")]
    ,[("A","spades"),("2","spades"),("3","spades"),("4","spades"),("5","spades"),("6","spades"),("7","spades"),("8","spades")
     ,("9","spades"),("10","spades"),("J","spades"),("Q","spades"),("K","spades")]
    ,[("A","hearts"),("2","hearts"),("3","hearts"),("4","hearts"),("5","hearts"),("6","hearts"),("7","hearts"),("8","hearts")
     ,("9","hearts"),("10","hearts"),("J","hearts"),("Q","hearts"),("K","hearts")]
    ,[("A","dimonds"),("2","dimonds"),("3","dimonds"),("4","dimonds"),("5","dimonds"),("6","dimonds"),("7","dimonds"),("8","dimonds")
     ,("9","dimonds"),("10","dimonds"),("J","dimonds"),("Q","dimonds"),("K","dimonds")]]

cardvaluedict = {"A":11,"J":10,"Q":10,"K":10}


# In[4]:


playerchip = Deposit(20)
dealerchip = Deposit(1000)
playagain = ""
#main logic
while playagain != "n":
    carddecktemp = carddeck
    betsum = 0
    playercards = HoldingCards()
    dealercards = HoldingCards()
    playercards.reset()
    dealercards.reset()
    printui_result()
    playagain = ""
    if dealerchip.chip == 0:
        print ("Congrates! You have won all the money the dealer has. \nUnfortunately you cant strip off his cloth as this function has not been implenmented")
        break
    elif playerchip.chip == 0:
        
        break
    while betsum not in range(1,50+1):
        try:
            betsum = int(input ("Place your bet! (maximal 50):"))
        except:
            print ("Invalid parameter, only integers are accepted")
        if playerchip.chip < betsum:
            betsum = 0
            print("No enough chips! Please wait for me to implement in game purchase function!!!")
        elif dealerchip.chip < betsum:
            betsum = 0
            print("Dealer has no enough chips, show some mercy to a brainless bot...")
    playerchip.takechip(betsum)
    dealerchip.takechip(betsum)
    playercards.drawcards(2)
    dealercards.drawcards(2)
    run = True
    while playercards.checksum() <= 21 and run:#Step 0, check player card value
        printui()
        askhit = ""
        while askhit != "h" and askhit != "s":#input check
            askhit = input ("Do you want to hit? Or do you want to stay(type h to hit /s to stay)").lower()
        
        if askhit == "h":#Step 1 player hits
            playercards.drawcards(1)
            
        elif askhit == "s": #Step 1 player stays
            if dealercards.checksum() > 21:
                printui_result()
                print(f"Dealer Busted, Player wins {betsum} chips")
                playerchip.winning(betsum)
                run = False
            while dealercards.checksum() <= playercards.checksum(): #dealer has lesser value
                dealercards.drawcards(1)
                if dealercards.checksum() > 21:
                    printui_result()
                    print(f"Dealer Busted, Player wins {betsum} chips")
                    playerchip.winning(betsum)
                    run = False
            if dealercards.checksum() <= 21 and dealercards.checksum() > playercards.checksum():
                printui_result()
                print(f"Dealer wins {betsum}")#dealer has greater value
                dealerchip.winning(betsum)
                run = False
    if playercards.checksum() > 21 and run:
        printui_result()
        print (f"Player Busted Dealer wins {betsum} chips")
        dealerchip.winning(betsum)
        run = False
    while playagain != "y" and playagain != "n":
        playagain = input("Playagain? (y/n)")

