import pygame
import sys
import time
import pickle
from network import Network
from wordSource import wordSource
from input import InputBox

pygame.font.init()

# Windows size
_displayWidth = 510
_displayHeight = 400

# Game windows
gameDisplay = pygame.display.set_mode((_displayWidth, _displayHeight))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Colors
_black = (0,0,0)
_white = (255,255,255)
_red = (200,0,0)
_brightRed = (255,0,0)
_green = (0,200,0)
_brightGreen = (0,255,0)
_blue = (0,0,200)
_brightBlue = (0,0,255)
_yellow = (200,200,0)

# Text size
_smallText = pygame.font.SysFont("cambria", 20)
_mediumText = pygame.font.SysFont("cambria", 30)
_largeText = pygame.font.SysFont("cambria", 40)

# Button size
_btnWidth = 120
_btnHeight = 50

# Text input fields
_inputBoxes = []
_inputBoxes.append(InputBox(149, 10, 200, 30)) # Input Word

_canvas = pygame.Surface((_displayWidth, _displayHeight))
_canvas.fill(_white)
_input1_bckg = pygame.Rect(151,12,196,26) # Clear Input Word

### Format displayed text
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

### Create button
def button(msg, x, y, ac, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(gameDisplay, ac,(x,y,_btnWidth,_btnHeight))

    if x+_btnWidth > mouse[0] > x and y+_btnHeight > mouse[1] > y:
        if click[0] == 1 and action != None:
            action()
            time.sleep(0.5)
        else:
            pygame.draw.rect(gameDisplay, ic,(x,y,_btnWidth,_btnHeight))
        
    # Button text
    textSurf, textRect = text_objects(msg, _smallText, _black)
    textRect.center = ( (x+(_btnWidth/2)), (y+(_btnHeight/2)) )
    gameDisplay.blit(textSurf, textRect)

## Create local game
def createLocal():
    guessingWordWindow()
    print("Create new local game")

# Not started 
def createServerGame():
    #    ## Nickname input
    #    ## Choose type (Public/Private)
    #    ## Player count

    onlineGame()
    print("Create new game")

### Close game window
def quitGame():
    print("Close game")
    pygame.quit()
    quit()



def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

def onlineGame():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP()) ## Nestrādā: TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType'
    print("You are player", player)

    ## Struct 
    createStruct = True
    y = 50
    x = 150

    ## Guessing word
    #word = wordSource.getWord()
    word = "KOKS"
    inputWord = ""
    attemptCount = 0
    maxPoints = 0
    guessAttempt = False
    gameOver = False
    correctInput = False
    startCountdown = True

    gameDisplay.fill(_white)
    gameDisplay.blit(_canvas, (151,12), _input1_bckg)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.allEndGuessing():
            redrawWindow(gameDisplay, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            text = font.render("You Won!", 1, (255,0,0))

            gameDisplay.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if gameOver:
            if player == 0:
                if not game.p1endGuessing:
                    n.send(maxPoints)
            elif player == 1:
                if not game.p2endGuessing:
                    n.send(maxPoints)
            else:
                if not game.p3endGuessing:
                    n.send(maxPoints)

        redrawWindow(gameDisplay, game, player)


## Local game
def guessingWordWindow():
    ## Struct 
    createStruct = True
    y = 50
    x = 150

    ## Guessing word
    #word = wordSource.getWord()
    word = "KOKS"
    inputWord = ""
    attemptCount = 0
    maxPoint = 0
    guessAttempt = False
    gameOver = False
    correctInput = False
    startCountdown = True

    gameDisplay.fill(_white)
    gameDisplay.blit(_canvas, (151,12), _input1_bckg)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # InputBox
            _inputBoxes[0].handle_event(event)
            gameDisplay.blit(_canvas, (152,12), _input1_bckg)
            if event.type == pygame.KEYDOWN:
                if _inputBoxes[0].active:
                    if event.key == pygame.K_RETURN:
                        inputWord = _inputBoxes[0].text
                        _inputBoxes[0].text = ''
                        if not gameOver:
                            guessAttempt = True     

        ## Generate guessing structure
        if createStruct:
            createStruct = False
            for n in range(5):
                l = 0
                while l < len(word):
                    pygame.draw.rect(gameDisplay, _black,((x + 35*l)-2,(y+ 40*n)-2,34,34))
                    pygame.draw.rect(gameDisplay, _white,((x + 35*l),(y+ 40*n),30,30))
                    l += 1
        
        ## Attempt
        # Attempt input
        if not gameOver:
            _inputBoxes[0].draw(gameDisplay)
        
        # Attempt 
        if guessAttempt:
            guessAttempt = False
            point = 0
            inputWord = inputWord.upper()
            
            # Input word length check
            if(len(inputWord) > len(word)):
                inputWord = inputWord[:len(word)]
            # Correct input
            if(word == inputWord):
                gameOver = True
                correctInput = True
                maxPoint = len(word)*2
                maxPoint += 5- attemptCount
                textSurf, textRect = text_objects("Your input is correct.", _smallText, _black)
                textRect.center = ((_displayWidth+x)/2 , 270 )
                gameDisplay.blit(textSurf, textRect)

                l = 0
                for c in word:
                    if( l < len(word)):
                        pygame.draw.rect(gameDisplay, _green,((x + 35*l),(y + 40*attemptCount),30,30))

                        textSurf, textRect = text_objects(c, _smallText, _black)
                        textRect.center = ( ((x + 35*l)+(30/2)), ((y + 40*attemptCount)+(30/2)) )
                        gameDisplay.blit(textSurf, textRect)

                        l += 1

            # Incorrect input
            else:
                i = 0
                while i < len(inputWord):

                    if(inputWord[i] == word[i]):
                        pygame.draw.rect(gameDisplay, _green,((x + 35*i),(y + 40*attemptCount),30,30))
                        point += 2
                    elif(word.find(inputWord[i]) != -1):
                        pygame.draw.rect(gameDisplay, _yellow,((x + 35*i),(y + 40*attemptCount),30,30))
                        point += 1
                    else:
                        pygame.draw.rect(gameDisplay, _red,((x + 35*i),(y + 40*attemptCount),30,30))

                    textSurf, textRect = text_objects(inputWord[i], _smallText, _black)
                    textRect.center = ( ((x + 35*i)+(30/2)), ((y + 40*attemptCount)+(30/2)) )
                    gameDisplay.blit(textSurf, textRect)

                    i += 1
                   
                empty = 0
                while(len(word) != len(inputWord) + empty):
                    pygame.draw.rect(gameDisplay, _red,((x + 35*(empty + len(inputWord))),(y + 40*attemptCount),30,30))
                    empty += 1
            
            # Point
            if maxPoint < point:
                maxPoint = point
            # Attempt
            attemptCount += 1

        # Dont guess after all attempt
        if attemptCount >= 5:
            gameOver = True           
            if not correctInput:

                textSurf, textRect = text_objects("Your input isn't correct.", _smallText, _black)
                textRect.center = ((_displayWidth+x)/2 , 270 )
                gameDisplay.blit(textSurf, textRect)

                i = 0
                while i < len(word):
                    pygame.draw.rect(gameDisplay, _green,((x + 35*i), 360,30,30))

                    textSurf, textRect = text_objects(word[i], _smallText, _black)
                    textRect.center = ( ((x + 35*i)+(30/2)), (360 +(30/2)) )
                    gameDisplay.blit(textSurf, textRect)

                    i += 1

                textSurf, textRect = text_objects("Correct answer is:", _smallText, _black)
                textRect.center = ( (_displayWidth+x)/2 , 330 )
                gameDisplay.blit(textSurf, textRect)

        if gameOver:
            textSurf, textRect = text_objects("You earned " + str(maxPoint) + " points", _smallText, _black)
            textRect.center = ((_displayWidth+x)/2 , 300 )
            gameDisplay.blit(textSurf, textRect)

            button("Play Again", 10, 10, _brightGreen, _green, guessingWordWindow)
            #button("Main", 10, 240, _brightBlue, _blue, menuWindow)


        pygame.display.update()
        clock.tick(60)

## Menu window
def menuWindow():

    ## Window title
    gameDisplay.fill(_white)
    TextSurf, TextRect = text_objects("Guess the Word", _largeText, _black)
    TextRect.center = ((_displayWidth/2), (100))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        ## Create button (dp_w, dp_h, active_color, inactive_color, function)
        button("Local", 30, 250, _brightGreen, _green, createLocal)
        button("Online", 195, 250, _brightBlue, _blue, createServerGame)
        button("Quit", 360, 250, _brightRed, _red, quitGame)

        pygame.display.update()
        clock.tick(60)


# Programm start
menuWindow()
