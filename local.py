import pygame
import time
import sys
from input import InputBox
from wordSource import wordSource


pygame.init()

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
_inputBoxes.append(InputBox(10, 30, 200, 30)) # Usernames
_inputBoxes.append(InputBox(149, 10, 200, 30)) # Input Word

_canvas = pygame.Surface((_displayWidth, _displayHeight))
_canvas.fill(_white)
_input1_bckg = pygame.Rect(151,12,196,26) # Clear Input Word


#_inputBoxes.append(InputBox(180, 42, 200, 30)) # Room number
#_inputBoxes.append(InputBox(180, 42, 200, 30)) # Room password


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
    #
    guessingWordWindow()


## Create player
def createPlayer():
    player = Player()
    player.userName = inputUsernameWindow()
    return player

# Not started 
def createServerGame():
    #
    

    #while True:
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            pygame.quit()
    #            quit()
    #        # InputBox
    #        for box in input_boxes:
    #            box.handle_event(event)
                    
    #    gameDisplay.fill(white)
    #    TextSurf, TextRect = text_objects("Create new game", mediumText)
    #    TextRect.center = ((display_width/2), (20))
    #    gameDisplay.blit(TextSurf, TextRect)

    #    ## Nickname input
    #    textSurf, textRect = text_objects("Enter nickname: ", smallText)
    #    textRect.center = (100 , 60 )
    #    gameDisplay.blit(textSurf, textRect)

    #    input_boxes[0].draw(gameDisplay)
        

    #    ## Choose type
    #    textSurf, textRect = text_objects("Choos type: ", smallText)
    #    textRect.center = (100 , 100 )
    #    gameDisplay.blit(textSurf, textRect)

    #    # Somehow get response
    #    gameType = "Private"

    #    # if type == private, password option
    #    if(gameType == "Private"):
    #        # Password input
    #        textSurf, textRect = text_objects("Create game password: ", smallText)
    #        textRect.center = (100 , 160 )
    #        gameDisplay.blit(textSurf, textRect)

    #        input_boxes[1].draw(gameDisplay)
        
    #    ## Control buttons
    #    button("Start", 50, 250, bright_green, green)
    #    button("Back", 250, 250, bright_blue, blue, menu_screen)
    #    button("Quit", 450, 250, bright_red, red, quitgame)
        
    #    pygame.display.update()
    #    clock.tick(60)

    print("Create new game")
   

# Not started    
def waitingPalyer():
    # Show: Server addr, GameID, GamePassword/Change password?
    # Show: Joined players
    # If you are game creator => Show: Start game , Cancel game , Set new owner, Kick player
    print("waiting players")

### Close game window
def quitGame():
    print("Close game")
    pygame.quit()
    quit()

### Game window
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
            _inputBoxes[1].handle_event(event)
            gameDisplay.blit(_canvas, (152,12), _input1_bckg)
            if event.type == pygame.KEYDOWN:
                if _inputBoxes[1].active:
                    if event.key == pygame.K_RETURN:
                        inputWord = _inputBoxes[1].text
                        _inputBoxes[1].text = ''
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
            _inputBoxes[1].draw(gameDisplay)
        
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
            textSurf, textRect = text_objects("Points " + str(maxPoint), _smallText, _black)
            textRect.center = ((_displayWidth+x)/2 , 300 )
            gameDisplay.blit(textSurf, textRect)

            button("Play Again", 10, 100, _brightGreen, _green, guessingWordWindow)
            button("Main", 10, 240, _brightBlue, _blue, menuWindow)


        pygame.display.update()
        clock.tick(60)
 
### Username input window
def inputUsernameWindow():

    ## Window title
    gameDisplay.fill(_white)
    TextSurf, TextRect = text_objects("Input username:", _mediumText, _black)
    TextRect.left = 10
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # InputBox
            _inputBoxes[0].handle_event(event)
            if event.type == pygame.KEYDOWN:
                if _inputBoxes[0].active:
                    if event.key == pygame.K_RETURN:
                        return _inputBoxes[0].text
        
        ## Username input field
        _inputBoxes[0].draw(gameDisplay)

        #button("Back", 450, 250, _brightRed, _red, menuWindow)

        pygame.display.update()
        clock.tick(60)

### Start window
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
        button("Create Local", 30, 250, _brightGreen, _green, createLocal)
        button("Create", 195, 220, _brightBlue, _blue, createServerGame)
        button("Join", 195, 280, _brightBlue, _blue, joinServerGame)
        button("Quit", 360, 250, _brightRed, _red, quitGame)

        pygame.display.update()
        clock.tick(60)


### Starting function call
#player1 = Player()
#player1.userName = "Name"
##guessingWordWindow(player1)
menuWindow()

### Close the game
pygame.quit()
quit()