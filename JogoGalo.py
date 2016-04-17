# Jogo do galo Code
import random

gameTab = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

player = 1
winner = 0
numPlays = 1
playerSymbol = None

#Prints the current board
def currentBoard():

    print("\n", gameTab[0][0],"|", gameTab[0][1], "|",gameTab[0][2],
          "\n---+---+---\n", gameTab[1][0], "|", gameTab[1][1], "|", gameTab[1][2],
          "\n---+---+---\n", gameTab[2][0], "|", gameTab[2][1], "|", gameTab[2][2])

#Resets the board to a new one
def resetBoard():
    global gameTab
    gameTab = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

#Give the last player the ability ro replay the game
def replay():
    global player, numPlays
    print("Nice game!")
    while True:
        print("Do you want a replay? If so say 'yes' if not say 'no' ")
        reset = input(":")
        try:
            reset = str(reset)
        except ValueError:
            print("\nI am afraid '%s' is not a valid answer" % reset)
            continue
        if(reset != "yes" and reset != "no"):
            print("\nI am afraid '%s' is not a valid answer" % reset)
            continue
        elif(reset == "yes"):
            resetBoard()
            numPlays = 1
            player = (random.randint(0,1))
            readPlay()
        else:
            print("\nHave a nice day then :D")
            break

#Checks for a winner
def checkWinner():
    global winner
    i = 0

    #Check for a winning line - diagonals first
    if ((gameTab[0][0] == gameTab[1][1] and gameTab[0][0] == gameTab[2][2]) or (gameTab[0][2] == gameTab[1][1] and gameTab[0][2] == gameTab[2][0])):
        winner = 1
        return None

    #Check rows and columns for a winning line
    for i in range (0, 3):
        if gameTab[i][0] == gameTab[i][1] and gameTab[i][0] == gameTab[i][2]:
            winner = 1
            return None
        elif gameTab[0][i] == gameTab[1][i] and gameTab[0][i] == gameTab[2][i]:
            winner = 1
            return None

    if(numPlays == 9): #We have a draw
        winner = 2
    else:
        winner = 0  #The game is still not finished...

#Congratulates the winning player or both in case of a draw
def congratulate():
    currentBoard()
    if (winner == 2):
        print("\nHow boring, it is a draw\n")
        replay()
    else:
        print("\nCongratulations, player", player,"YOU ARE THE WINNER!\n")
        replay()

#Check is the position is already played
def checkPlay(row, column):
    if(gameTab[row][column]=="X" or gameTab[row][column]=="O"):
        print("\nPlease enter a valid position!")
        readPlay()
    return True

#Puts the player piece on the board
def playGame(position):
    global player, winner, numPlays

    position = position-1
    row = (position // 3)
    column =  (position % 3)

    if(checkPlay(row, column)):
        if (player == 1):
            gameTab[row][column]="X"
        else:
            gameTab[row][column]="O"

    checkWinner()
    if(winner != 0):
        congratulate()
    else:
        player = (player + 1) % 2
        numPlays += 1
        readPlay()

def readPlay(): #reads where the player wants to play and checks if is a valid number position
    global player, play

    if(player == 1):
        playerSymbol = "X"
    else:
        playerSymbol = "O"
    #checks if the player types a number
    while True:
        currentBoard()
        print("\nPlease player",player ,"enter the number of the square where you want to place your", playerSymbol)
        play = input(":")
        try:
            play = int(play)
        except ValueError:
            print("\nI am afraid '%s' is not a number" % play)
            continue
        if(play>9 or play<=0 ):
            print("\nPlease enter a valid number!")
            continue
        else:
            break

    playGame(play)


#Fucntion that starts the file! Its like 'MAIN'
if __name__ == '__main__':
    readPlay()
