import warnings
from random import *
import pygame
import numpy as np
import os
import math
from Background import Background
from Edge import Edge
from City import City
from Card import Card
from Player import Player
from AI import AI, randomAI
from Human import Human
from Track import Track
from GameState import GameState

pygame.init()
warnings.filterwarnings("ignore")

# dictionary for translating setting code to True or False
Translate = {'yes': True, 'no': False, '1': True, '2': False, '0': False}
SettingTranslate = {'yes': '1', 'no': '0', 'none': 'n'}
stratList = ['emptyHand', 'readBlock', 'blindDestination', 'longestFirst', 'ironEmpire']
for index in range(len(stratList)):
    SettingTranslate[stratList[index].lower()] = str(index)

commandlineFlag = input("Do you want to play the game using the Graphical User Interface or control it from "
                        "the command line? (type \'cmd\' or \'gui\'): ").lower()

AIvAIFlag = False
stratFlag1 = False
stratFlag2 = False
csvFlag = False
loopFlag = 1
numFlags = 5  # increase this with every new flag created

if commandlineFlag == 'cmd':
    print("You have chosen to control the settings from the command line, please do not change the settings from the "
          "Graphical User Interface, there could be unexpected errors/bugs.")
    settingsCode = input("Enter the settings code you wish to use or \'none\' if you don\'t know it: ").lower()
    if settingsCode == 'none':
        settingsCode = ''
        settingsCode += SettingTranslate[input("Do you want to use AI vs AI mode? (type \'yes\' or \'no\'): ").lower()]  # AIvAIFlag
        print("For reference this is the list of strategies: ", stratList)
        if Translate[settingsCode[0]]:  # aka if it is AI v AI ask user what strat player 1 will follow
            settingsCode += SettingTranslate[input("Enter the name of the strategy you want playerOne to follow "
                                                   "(type it as it is written in the code. If you don\'t care type "
                                                   "\'none\'):  ").lower()]  # stratFlag1
        else:
            settingsCode += 'n'
        settingsCode += SettingTranslate[input("Enter the name of the strategy you want playerTwo to follow "
                                               "(type it as it is written in the code. If you don\'t care type "
                                               "\'none\'):  ").lower()]  # stratFlag2
        settingsCode += SettingTranslate[input("Do you want to generate .csv files for this run? "
                                               "(type \'yes\' or \'no\'): ").lower()]  # csvFlag
        settingsCode += input("Enter the amount of times you want the game to loop: ").lower()  # loopFlag
        #loop count will always be the last setting

    #set flags based on settings code
    AIvAIFlag = Translate[settingsCode[0]]
    if settingsCode[1] == 'n':
        stratFlag1 = False
    else:
        stratFlag1 = stratList[int(settingsCode[1])]
    if settingsCode[2] == 'n':
        stratFlag2 = False
    else:
        stratFlag2 = stratList[int(settingsCode[2])]
    csvFlag = Translate[settingsCode[3]]
    loopFlag = int(settingsCode[numFlags-1:])

    print("The setting code for this setting configuration is: " + settingsCode)
print("AIvAIFlag", AIvAIFlag)
print("stratFlag1", stratFlag1)
print("stratFlag2", stratFlag2)
print("csvFlag", csvFlag)
print("loopFlag", loopFlag)

if commandlineFlag == 'cmd':
    input("Press enter to begin")
# sets the window size to 800x600px
display_width = 1920
display_height = 1080

# easy access to colors
black = (0, 0, 0)
grey = (139, 139, 139)
white = (255, 255, 255)
yellow = (255, 255, 0)
pink = (255, 102, 178)
red = (255, 0, 0)
darkRed = (139, 0, 0)
orange = (255, 128, 0)
green = (0, 255, 0)
darkGreen = (0, 139, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 139)

# makes the screen as wide and tall as above variables, makes a white background, adds TTR title, and starts a clock
screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN)
pygame.display.set_caption("Ticket To Ride")
clock = pygame.time.Clock()

# loads images to act as the static cards
whiteTrainImg = pygame.image.load('Ticket To Ride Assets\White\TrainCard_White.png')
pinkTrainImg = pygame.image.load('Ticket To Ride Assets\Pink\TrainCard_Pink.png')
redTrainImg = pygame.image.load('Ticket To Ride Assets\Red\TrainCard_Red.png')
orangeTrainImg = pygame.image.load('Ticket To Ride Assets\Orange\TrainCard_Orange.png')
yellowTrainImg = pygame.image.load('Ticket To Ride Assets\Yellow\TrainCard_Yellow.png')
greenTrainImg = pygame.image.load('Ticket To Ride Assets\Green\TrainCard_Green.png')
blueTrainImg = pygame.image.load('Ticket To Ride Assets\Blue\TrainCard_Blue.png')
blackTrainImg = pygame.image.load('Ticket To Ride Assets\Black\TrainCard_Black.png')

# loads images to act as the moving cards
whiteMovingCardImg = pygame.image.load('Ticket To Ride Assets\White\RotatedCard_White.png')
pinkMovingImg = pygame.image.load('Ticket To Ride Assets\Pink\RotatedCard_Pink.png')
redMovingImg = pygame.image.load('Ticket To Ride Assets\Red\RotatedCard_Red.png')
orangeMovingImg = pygame.image.load('Ticket To Ride Assets\Orange\RotatedCard_Orange.png')
yellowMovingImg = pygame.image.load('Ticket To Ride Assets\Yellow\RotatedCard_Yellow.png')
greenMovingImg = pygame.image.load('Ticket To Ride Assets\Green\RotatedCard_Green.png')

# loads images to act as the draw deck
whiteDeckImg = pygame.image.load('Ticket To Ride Assets\White\WhiteDeck.png')
pinkDeckImg = pygame.image.load('Ticket To Ride Assets\Pink\PinkDeck.png')
redDeckImg = pygame.image.load('Ticket To Ride Assets\Red\RedDeck.png')
orangeDeckImg = pygame.image.load('Ticket To Ride Assets\Orange\OrangeDeck.png')
yellowDeckImg = pygame.image.load('Ticket To Ride Assets\Yellow\YellowDeck.png')
greenDeckImg = pygame.image.load('Ticket To Ride Assets\Green\GreenDeck.png')
blueDeckImg = pygame.image.load('Ticket To Ride Assets\Blue\BlueDeck.png')
blackDeckImg = pygame.image.load('Ticket To Ride Assets\Black\BlackDeck.png')

#loads images of the train tracks
blankTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Blank.png')
redTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Red.png')
orangeTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Orange.png')
yellowTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Yellow.png')
greenTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Green.png')
blueTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Blue.png')
pinkTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Pink.png')
whiteTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_White.png')
blackTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Filled\Track_Black.png')

#loads images of the occupied train tracks
redTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Red.png')
orangeTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Orange.png')
yellowTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Yellow.png')
greenTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Green.png')
blueTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Blue.png')
pinkTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Pink.png')
whiteTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_White.png')
blackTrackOcc = pygame.image.load('Ticket To Ride Assets\Tracks\Occupied\Track_Black.png')


screen.blit(blackTrainImg, (display_width * 0.05, display_height * 0.9))
screen.blit(whiteTrainImg, (display_width * 0.15, display_height * 0.9))

BackGround = Background('Ticket To Ride Assets\BackGrounds\Background.png', [0, 0])
TitleScreenImg = Background('Ticket To Ride Assets\BackGrounds\TitleScreen.png', [0, 0])

cityConnection = [[-1, Edge(3, 'black'), -1, Edge(5, 'white'), Edge(2,  'black'), -1, -1],
                   [Edge(3, 'black'), -1, Edge(4, 'white'), -1, -1, -1, -1],
                   [-1, Edge(4, 'white'), -1, Edge(6, 'black'), -1, Edge(4, 'black'), -1],
                   [Edge(5, 'white'), -1, Edge(6, 'black'), -1, -1, -1, Edge(3, 'white')],
                   [Edge(2, 'black'), -1, -1, -1, -1, Edge(3, 'white'), Edge(3, 'white')],
                   [-1, -1, Edge(4, 'black'), -1, Edge(3, 'white'), -1, Edge(2, 'black')],
                   [-1, -1, -1, Edge(3, 'white'), Edge(3, 'white'), Edge(2, 'black'), -1]]

cityNames = ['Washington', 'Montana', 'New York', 'Texas', 'Colorado', 'Kansas', 'Oklahoma']
cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5, 'Oklahoma': 6}

playerMode = 'AI vs AI' if AIvAIFlag else 'Human vs AI'
playerOne = Player('playerOne')
playerTwo = Player('playerTwo')
p1Wins = 0
p2Wins = 0
def createPlayers():
    global playerOne, playerTwo, playerMode
    if playerMode == 'Human vs AI':
        playerOne = Human('playerOne')
    elif playerMode == 'AI vs AI':
        playerOne = AI('playerOne', stratFlag1 if stratFlag1 else None)

    #stratFlag will be False or the name of the strat, since strings equate to True this code works
    playerTwo = AI('playerTwo', stratFlag2 if stratFlag2 else None)
    playerOne.addDestCardToHand()
    playerTwo.addDestCardToHand()

def getEdgeValue(length):
    if length == 1:
        return 1
    elif length == 2:
        return 2
    elif length == 3:
        return 4
    elif length == 4:
        return 7
    elif length == 5:
        return 10
    elif length == 6:
        return 15
    else:
        return -1

colors = ["white", "pink", "red", "orange", "yellow", "green", "blue", "black"]
chosenColors = ["white", "black"]

def switchDeck(color):
    return {
        'white': lambda: 'whiteDeck1',
        'pink': lambda: 'pinkDeck1',
        'red': lambda: 'redDeck1',
        'orange': lambda: 'orangeDeck1',
        'yellow': lambda: 'yellowDeck1',
        'green': lambda: 'greenDeck1',
        'blue': lambda: 'blueDeck1',
        'black': lambda: 'blackDeck1',
    }.get(color, lambda: None)()
    # return color + 'Deck1'

def checkHitBoxes(color):
    return {
        'white': lambda: drawCard("white"),
        'pink': lambda: drawCard("pink"),
        'red': lambda: drawCard("red"),
        'orange': lambda: drawCard("orange"),
        'yellow': lambda: drawCard("yellow"),
        'green': lambda: drawCard("green"),
        'blue': lambda: drawCard("blue"),
        'black': lambda: drawCard("black"),
    }.get(color, lambda: None)()
    # return drawCard(color)

# Draws the surface where the text will be written
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# makes a button with message,font size,x,y,width,height,inactive and active color and the action
def button(msg, fs, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:  # changed from:    if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font('freesansbold.ttf', fs)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x + (w / 2), (y + (h / 2)))
    screen.blit(textSurf, textRect)

def displayText(text, x, y):
    largeText = pygame.font.Font('freesansbold.ttf', 25)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)


WA = City(int(display_width * 0.1), int(display_height * 0.15))
CO = City(int(display_width * 0.3), int(display_height * 0.35))
MT = City(int(display_width * 0.35), int(display_height * 0.1))
TX = City(int(display_width * 0.4), int(display_height * 0.7))
OK = City(int(display_width * 0.475), int(display_height * 0.45))
KS = City(int(display_width * 0.5), int(display_height * 0.25))
NY = City(int(display_width * 0.75), int(display_height * 0.2))

cityArray = [WA, MT, NY, TX, CO, KS, OK]

def drawDecks(color):
    return {
        'white': lambda: screen.blit(whiteDeckImg, (display_width * 0.017, display_height * 0.85)),
        'pink': lambda: screen.blit(pinkDeckImg, (display_width * 0.117, display_height * 0.85)),
        'red': lambda: screen.blit(redDeckImg, (display_width * 0.217, display_height * 0.85)),
        'orange': lambda: screen.blit(orangeDeckImg, (display_width * 0.317, display_height * 0.85)),
        'yellow': lambda: screen.blit(yellowDeckImg, (display_width * 0.417, display_height * 0.85)),
        'green': lambda: screen.blit(greenDeckImg, (display_width * 0.517, display_height * 0.85)),
        'blue': lambda: screen.blit(blueDeckImg, (display_width * 0.617, display_height * 0.85)),
        'black': lambda: screen.blit(blackDeckImg, (display_width * 0.717, display_height * 0.85)),

    }.get(color, lambda: None)()

def createBoard():
    global cityConnection
    #this is not commented out since it just sets the game over when starting a new round
    cityConnection = ([[-1, Edge(3, 'black'), -1, Edge(5, 'white'), Edge(2, 'black'), -1, -1],
                       [Edge(3, 'black'), -1, Edge(4, 'white'), -1, -1, -1, -1],
                       [-1, Edge(4, 'white'), -1, Edge(6, 'black'), -1, Edge(4, 'black'), -1],
                       [Edge(5, 'white'), -1, Edge(6, 'black'), -1, -1, -1, Edge(3, 'white')],
                       [Edge(2, 'black'), -1, -1, -1, -1, Edge(3, 'white'), Edge(3, 'white')],
                       [-1, -1, Edge(4, 'black'), -1, Edge(3, 'white'), -1, Edge(2, 'black')],
                       [-1, -1, -1, Edge(3, 'white'), Edge(3, 'white'), Edge(2, 'black'), -1]])
    ''' This is commented out because it adds randomness to what tracks are what colors, for AI we dont want this
    cityConnection = ([[-1, Edge(3, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(5, chosenColors[randrange(0, len(chosenColors))]),
                        Edge(2, chosenColors[randrange(0, len(chosenColors))]), -1, -1],
                       [Edge(3, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(4, chosenColors[randrange(0, len(chosenColors))]), -1, -1, -1, -1],
                       [-1, Edge(4, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(6, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(4, chosenColors[randrange(0, len(chosenColors))]), -1],
                       [Edge(5, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(6, chosenColors[randrange(0, len(chosenColors))]), -1, -1, -1,
                        Edge(3, chosenColors[randrange(0, len(chosenColors))])],
                       [Edge(2, chosenColors[randrange(0, len(chosenColors))]), -1, -1, -1, -1,
                        Edge(3, chosenColors[randrange(0, len(chosenColors))]),
                        Edge(3, chosenColors[randrange(0, len(chosenColors))])],
                       [-1, -1, Edge(4, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(3, chosenColors[randrange(0, len(chosenColors))]), -1,
                        Edge(2, chosenColors[randrange(0, len(chosenColors))])],
                       [-1, -1, -1, Edge(3, chosenColors[randrange(0, len(chosenColors))]),
                        Edge(3, chosenColors[randrange(0, len(chosenColors))]),
                        Edge(2, chosenColors[randrange(0, len(chosenColors))]), -1]])
    '''


whiteDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.03, display_height * 0.85, 100, 100), 1)
pinkDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.13, display_height * 0.85, 100, 100), 1)
redDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.23, display_height * 0.85, 100, 100), 1)
orangeDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.33, display_height * 0.85, 100, 100), 1)
yellowDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.43, display_height * 0.85, 100, 100), 1)
greenDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.53, display_height * 0.85, 100, 100), 1)
blueDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.63, display_height * 0.85, 100, 100), 1)
blackDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.73, display_height * 0.85, 100, 100), 1)
passTurn = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.75, display_height * 0.5, 100, 75), 1)
destDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.70, display_height * 0.6, 200, 75), 1)


def drawGameBoard():

    pygame.draw.line(screen, black, (WA.getX(), WA.getY()), (CO.getX(), CO.getY()))
    pygame.draw.line(screen, black, (WA.getX(), WA.getY()), (TX.getX(), TX.getY()))
    pygame.draw.line(screen, black, (WA.getX(), WA.getY()), (MT.getX(), MT.getY()))
    pygame.draw.line(screen, black, (TX.getX(), TX.getY()), (NY.getX(), NY.getY()))
    pygame.draw.line(screen, black, (NY.getX(), NY.getY()), (MT.getX(), MT.getY()))
    pygame.draw.line(screen, black, (NY.getX(), NY.getY()), (KS.getX(), KS.getY()))
    pygame.draw.line(screen, black, (TX.getX(), TX.getY()), (OK.getX(), OK.getY()))
    pygame.draw.line(screen, black, (OK.getX(), OK.getY()), (CO.getX(), CO.getY()))
    pygame.draw.line(screen, black, (KS.getX(), KS.getY()), (CO.getX(), CO.getY()))
    pygame.draw.line(screen, black, (OK.getX(), OK.getY()), (KS.getX(), KS.getY()))

    # draws the black and white train card on the card piles over the hit boxes
    for x in range(0, len(chosenColors), 1):
        drawDecks(chosenColors[x])

    pygame.draw.rect(screen, darkGreen, (display_width * 0.83, display_height * 0.125, display_width * 0.15, display_height * 0.66))
    displayText("HAND", display_width * 0.95, display_height * 0.14)

    drawCities()

def drawCities():
    pygame.draw.circle(screen, white, [WA.getX(), WA.getY()], 50, 50)
    pygame.draw.circle(screen, white, [CO.getX(), CO.getY()], 50, 50)
    pygame.draw.circle(screen, white, [MT.getX(), MT.getY()], 50, 50)
    pygame.draw.circle(screen, white, [TX.getX(), TX.getY()], 50, 50)
    pygame.draw.circle(screen, white, [OK.getX(), OK.getY()], 50, 50)
    pygame.draw.circle(screen, white, [KS.getX(), KS.getY()], 50, 50)
    pygame.draw.circle(screen, white, [NY.getX(), NY.getY()], 50, 50)

    displayText("WA", WA.getX(), WA.getY())
    displayText("CO", CO.getX(), CO.getY())
    displayText("MT", MT.getX(), MT.getY())
    displayText("TX", TX.getX(), TX.getY())
    displayText("OK", OK.getX(), OK.getY())
    displayText("KS", KS.getX(), KS.getY())
    displayText("NY", NY.getX(), NY.getY())


trackDataArray = [[-1 for x in range(20)] for y in range(11)]
#draws the tracks
def drawTracks():
    row = 0
    for i in range(0, len(cityConnection), 1):
        for j in range(i, len(cityConnection[i]), 1):
            if cityConnection[i][j] != -1:
                length = cityConnection[i][j].getLength()
                testLength = length
                color = cityConnection[i][j].getColor()
                x1 = cityArray[i].getX()
                y1 = cityArray[i].getY()
                x2 = cityArray[j].getX()
                y2 = cityArray[j].getY()
                difx = x2 - x1
                dify = y2 - y1
                radians = math.atan2(dify, difx)
                rot = math.degrees(radians)

                perLenX = difx/length
                perLenY = dify/length

                trackImg = pygame.transform.scale(eval(color + "Track"), (100, 50))
                trackImgFin = pygame.transform.rotate(trackImg, -rot)

                for pri in range(1, length+1):
                    if testLength >= 0:
                        left = x1 + (perLenX*pri*.8) - 50
                        top = y1 + (perLenY*pri*.8) - 50
                        screen.blit(trackImgFin, (left, top))

                        trackDataArray[row][pri-1] = Track(top, left, color, trackImgFin, length, rot, perLenX, perLenY, False, [i, j])
                        testLength -= 1
                        if testLength == 0:
                            row += 1

def claimTrack(track, row, playerName):  # player name variable is just for print statement
    color = track.getColor()
    trackImg = pygame.transform.scale(eval(color + "TrackOcc"), (100, 50))
    trackImgFin = pygame.transform.rotate(trackImg, -track.getRot())
    testLength = track.getLength()
    for pri in range(0, track.getLength()):
        trackDataArray[row][pri].setOccupied(True)
        if testLength >= 0:
            left = track.getLeft() + (track.getPerX() * pri * .8)
            top = track.getTop() + (track.getPerY() * pri * .8)
            screen.blit(trackImgFin, (left, top))

    print(playerName + " claimed tracks between " + cityNames[track.getEdgeData()[0]] + " and " + cityNames[track.getEdgeData()[1]])


def drawCard(color):
    screen.blit(globals()[color + 'TrainImg'], (display_width * 0.85, display_height * 0.13 + (40 * playerOne.cardIndex)))
    playerOne.addCardToHand(color)

def removeCardsFromHand(color, numRemove):
    for k in range(playerOne.handCards.__len__()-1, -1, -1):
        if playerOne.handCards[k].getColor() == color and numRemove > 0:
            playerOne.handCards.remove(playerOne.handCards[k])
            playerOne.cardIndex -= 1
            numRemove -= 1
    pygame.draw.rect(screen, darkGreen, (display_width * 0.83, display_height * 0.125, display_width * 0.15, display_height * 0.66))
    displayText("HAND", display_width * 0.95, display_height * 0.14)
    for k in range(0, playerOne.handCards.__len__(), 1):
        color = playerOne.handCards[k].getColor()
        screen.blit(globals()[color + 'TrainImg'], (display_width * 0.85, display_height * 0.13 + (40 * k)))

def getHumanMove():
    colorsdrawn = []
    drawCount = 0
    while True:  # keeps looping until user makes a valid move
        button("Title Screen", 17, display_width * 0.85, display_height * 0.055, 100, 75, blue, darkBlue, titleScreen)
        button("Quit", 20, display_width * 0.85, display_height * 0.8, 100, 75, red, darkRed, quitGame)
        button("Pass Turn", 17, display_width * 0.75, display_height * 0.5, 100, 75, white, grey)
        button("Draw Destination Card", 17, display_width * 0.70, display_height * 0.6, 200, 75, white, grey)

        displayText("Destination", display_width * 0.1, display_height * 0.32)
        displayText("Cards", display_width * 0.1, display_height * 0.34)
        height = 0.365
        for i in range(0, len(playerOne.destinationCards)):
            toDisplay = str(playerOne.destinationCards[i].city1)
            toDisplay += ", " + str(playerOne.destinationCards[i].city2)
            toDisplay += " = " + str(playerOne.destinationCards[i].points)
            displayText(toDisplay, display_width * 0.1, display_height * height)
            height += 0.025

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if drawCount == 0:  # if draw count is 0 then the player can draw or claim. if draw count is above 0 player can only draw
                    for i in range(0, len(trackDataArray), 1):
                        for j in range(0, len(trackDataArray[i]), 1):
                            data = trackDataArray[i][j]

                            if data != -1:
                                # pygame.draw.circle(screen, black, (int(data.getLeft()), int(data.getTop())), 10)
                                if data.getImg().get_rect().move(data.getLeft(), data.getTop()).collidepoint(pos) and not data.getOccupied():
                                    sameColor = 0
                                    for k in range(0, playerOne.handCards.__len__(), 1):
                                        if playerOne.handCards[k].getColor() == data.getColor():
                                            sameColor += 1
                                        if sameColor == data.getLength():
                                            #next to lines moved elsewhere so it is update the same it is an AI or human claiming a track
                                            #firstTrack = trackDataArray[i][0]
                                            #claimTrack(firstTrack, i)
                                            removeCardsFromHand(data.getColor(), data.getLength())
                                            return ['claim', np.array(data.getEdgeData()).tolist()]

                if passTurn.collidepoint(pos):  # passTurn   statement previously included: and drawCount == 0:
                    # no need to update the game state since there is no change
                    return ['pass']

                elif drawCount == 0 and destDeck.collidepoint(pos):
                    playerOne.addDestCardToHand()
                    return ['draw d']
                elif drawCount == 0 and len(playerOne.handCards) + 1 >= 14:
                    print('There are 14 cards in your hand, you can not draw any more!')
                    displayText("There are 14 cards in your hand, you can not draw any more!", display_width * 0.5, display_height * 0.03)
                    # add a way for the player to see this message in game since they cant see the console while playing
                elif drawCount == 0 or drawCount == 1:  # this is basically an else statement since drawCount will always be 0 or 1 at this point
                    outputBuffer = True
                    for x in range(0, len(chosenColors), 1):
                        if eval(chosenColors[x] + "Deck").collidepoint(pos):
                            checkHitBoxes(chosenColors[x])
                            colorsdrawn.append(chosenColors[x])
                            drawCount += 1
                            outputBuffer = False
                            if drawCount == 2:
                                return ['draw t', colorsdrawn]  # for the record 'colorsdrawn is never used or saved
                    if outputBuffer and drawCount == 1:  # if you exit the above for loop and outputBuffer = true then the player did not click on a card
                        print('You drew one card already this turn you cannot claim a track or destination card you must draw one more train card this turn.')
                        displayText("You drew one card already this turn you cannot claim a track or destination card you must draw one more train card this turn.", display_width * 0.5,
                                    display_height * 0.03)
                        # add a way for the player to see this message in game since they cant see the console while playing

        # keeps updating since its stuck in this loop until user clicks
        pygame.display.update()
        clock.tick(60)


def quitGame():
    pygame.quit()
    quit()

def titleScreen():
    #   print(pygame.font.get_fonts())
    start = True
    screen.fill(white)
    screen.blit(TitleScreenImg.image, TitleScreenImg.rect)

    while start:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
        button("Start Train-ing", 20, display_width * 0.45, display_height * 0.4, 200, 75, green, darkGreen, gameStart)
        button("Settings", 20, display_width * 0.45, display_height * 0.5, 200, 75, blue, darkBlue, settings)
        button("Quit", 20, display_width * 0.45, display_height * 0.6, 200, 75, red, darkRed, quitGame)

        pygame.display.update()
        clock.tick(60)

def settings():
    global playerMode
    screen.fill(white)
    screen.blit(BackGround.image, BackGround.rect)
    pygame.draw.rect(screen, grey, (display_width * 0.075, display_height * 0.15, 1550, 200), 0)
    for j in range(0, len(chosenColors), 1):
        pygame.draw.rect(screen, darkBlue, (display_width * (colors.index(chosenColors[j])+1) / 10 - 6, display_height * 0.2 - 6, 110, 110), 11)

    running = True

    global whiteDeck1, pinkDeck1, redDeck1, orangeDeck1, yellowDeck1, greenDeck1, blueDeck1, blackDeck1

    while running:

        whiteDeck1 = pygame.draw.rect(screen, white, (display_width * 0.1, display_height * 0.2, 100, 100), 0)
        pinkDeck1 = pygame.draw.rect(screen, pink, (display_width * 0.2, display_height * 0.2, 100, 100), 0)
        redDeck1 = pygame.draw.rect(screen, red, (display_width * 0.3, display_height * 0.2, 100, 100), 0)
        orangeDeck1 = pygame.draw.rect(screen, orange, (display_width * 0.4, display_height * 0.2, 100, 100), 0)
        yellowDeck1 = pygame.draw.rect(screen, yellow, (display_width * 0.5, display_height * 0.2, 100, 100), 0)
        greenDeck1 = pygame.draw.rect(screen, green, (display_width * 0.6, display_height * 0.2, 100, 100), 0)
        blueDeck1 = pygame.draw.rect(screen, blue, (display_width * 0.7, display_height * 0.2, 100, 100), 0)
        blackDeck1 = pygame.draw.rect(screen, black, (display_width * 0.8, display_height * 0.2, 100, 100), 0)

        pygame.draw.rect(screen, grey, (display_width * 0.12, display_height * 0.38, 300, 100), 0)
        modeOption = pygame.draw.rect(screen, white, (display_width * 0.3, display_height * 0.4, 200, 75), 0)
        button("Change Mode", 20, display_width * 0.3, display_height * 0.4, 200, 75, white, grey)
        displayText("Mode: " + playerMode, display_width * 0.2, display_height * 0.43)

        button("Play Game", 20, display_width * 0.45, display_height * 0.4, 200, 75, blue, darkBlue, titleScreen)
        button("Quit", 20, display_width * 0.45, display_height * 0.6, 200, 75, red, darkRed, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if modeOption.collidepoint(pos):
                    if playerMode == 'Human vs AI':
                        playerMode = 'AI vs AI'
                    elif playerMode == 'AI vs AI':
                        playerMode = 'Human vs AI'
                else:
                    for i in range(0, len(colors), 1):
                        colorDeck = switchDeck(colors[i])
                        if eval(colorDeck).collidepoint(pos):
                            if chosenColors.__contains__(colors[i]):
                                chosenColors.remove(colors[i])
                                pygame.draw.rect(screen, grey,
                                                 (display_width * (i + 1) / 10 - 6, display_height * 0.2 - 6, 110, 110), 11)
                            else:
                                chosenColors.append(colors[i])
                                pygame.draw.rect(screen, darkBlue,
                                                 (display_width * (i + 1) / 10 - 6, display_height * 0.2 - 6, 110, 110), 11)

            pygame.display.update()
        clock.tick(60)

def gameStart(loopsRemaining=loopFlag):
    loopsRemaining -= 1

    global playerMode, p1Wins, p2Wins
    createPlayers()
    currentTurn = GameState(1, cityConnection, playerOne, playerTwo)

    screen.fill(white)
    screen.blit(BackGround.image, BackGround.rect)

    createBoard()
    drawTracks()
    drawGameBoard()
    drawCities()
    running = True
    # game state array for saving every turn
    #GameStateArray = []

    if csvFlag:
        currentTurn.createCSVs()

    while running:

        drawCities()  # they do not change but sometimes the tracks are drawn over them making the names unreadable so we just redraw them again here

        pygame.draw.rect(screen, grey, (display_width * 0.075, display_height * 0.01, 1600, 50), 0)
        displayText("Error Msg: ", display_width * 0.04, display_height * 0.04)
        button("Quit", 20, display_width * 0.85, display_height * 0.8, 100, 75, red, darkRed, quitGame)

        p1Move = None
        # AI or Human makes its move and stores it in the game state
        if playerMode == 'Human vs AI':  # or type(playerOne) == Human
            # humanMove = playerOne.makeMove(currentTurn, deckArray)  # it did not work
            # I hope the line above works, it may not since it has the human class calling a TTR class function
            p1Move = getHumanMove()  # since the line above did not work I use this
        elif playerMode == 'AI vs AI':
            p1Move = playerOne.makeMove(currentTurn)

        currentTurn.setPlayerMove(playerOne, p1Move[0])
        currentTurn.LastFullAction = p1Move
        currentTurn.LastP = 'playerOne'

        if currentTurn.getP1Move() == 'claim':  # if a player claims a track the cityConnection and trackDataArray
            # needs to be updated but for the other move options the values are just updated in that player's instance
            x = p1Move[1][0]
            y = p1Move[1][1]
            playerOne.points += getEdgeValue(cityConnection[x][y].getLength())
            cityConnection[x][y].claim(playerOne)
            cityConnection[y][x].claim(playerOne)  # this could be wrong so if weird stuff starts happening check this
            #also now update if claiming this track happens to complete a destination card
            for row in range(0, len(trackDataArray)):
                if type(trackDataArray[row]) != int:
                    if type(trackDataArray[row][0]) != int:
                        if (trackDataArray[row][0].getEdgeData() == p1Move[1]):  #.all():
                            claimTrack(trackDataArray[row][0], row, "Player one")  # updates track data array
                            break  # ima do my best to explain this quick: because the track data array is filled "wrong" it has some -1 values in
                            # it so row is equal to -1 sometimes and you cannot get edge data of a non track obj

        print("Player one chose to " + currentTurn.getP1Move())
        # updating the game state based on player one's move
        playerOne.checkDestCardCompletion(cityConnection)  # this will update the players points if a dcard was completed
        currentTurn.updatePlayerInfo(playerOne)
        currentTurn.updateTracks(cityConnection)

        #GameStateArray.append(currentTurn.returnListedforP())
        # AI makes its move and stores it in the game state
        p2Move = playerTwo.makeMove(currentTurn)
        currentTurn.setPlayerMove(playerTwo, p2Move[0])

        currentTurn.LastFullAction = p2Move
        currentTurn.LastP = 'playerTwo'

        if currentTurn.getP2Move() == 'claim':
            x = p2Move[1][0]
            y = p2Move[1][1]
            playerTwo.points += getEdgeValue(cityConnection[x][y].getLength())
            cityConnection[x][y].claim(playerTwo)
            cityConnection[y][x].claim(playerTwo)  # this could be wrong so if weird stuff starts happening check this
            for row in range(0, len(trackDataArray)):
                if type(trackDataArray[row]) != int:
                    if type(trackDataArray[row][0]) != int:
                        if (trackDataArray[row][0].getEdgeData() == p2Move[1]):  #.all():
                            claimTrack(trackDataArray[row][0], row, "Player two")  # updates track data array
                            break

        print("Player two chose to " + currentTurn.getP2Move())
        # updating the game state based on player two's move
        #remember to update trackDataArray when AI makes move since it affects the player (yep i did, that's done above)
        playerTwo.checkDestCardCompletion(cityConnection)  # this will update the players points if a dcard was completed
        currentTurn.updatePlayerInfo(playerTwo)
        currentTurn.updateTracks(cityConnection)


        # check for deadlock
        if currentTurn.getP1Move() == 'pass' and currentTurn.getP2Move() == 'pass':
            print("Since both players passed their turn it is likely the game has reached a deadlock so game ends")
            running = False  # break should also work

        # tests if there are any edges left to be claimed, if not: end game, if there are unclaimed edges then continue
        edgeLeft = False
        for i in range(len(cityConnection)):
            toLeave = False
            for edge in cityConnection[i]:
                if type(edge) != int:  # aka if there is an edge between those two cities
                    if edge.occupied == 'False':
                        toLeave = True
                        edgeLeft = True
                        break
            if toLeave:
                break
        if not edgeLeft:
            print("All tracks have been claimed so the game is over!")
            running = False  # break should also work

        #save each turn for debugging/prototyping
        # currentTurn.writeToNPY()
        if csvFlag:
            currentTurn.writeToCSV()  # btw you def want this before you increment the turn

        #GameStateArray.append(currentTurn.returnListedforP())  # used for alex's numpy stuff i think, if not idk what its for
        currentTurn.incrementTurn()


        pygame.display.update()
        clock.tick(60)

    #check which destination cards are not completed and update player score
    for card in playerOne.getDestCards():
        if not card.completed:
            playerOne.points -= card.points
            print("Player one did not complete the destination card between " + card.city1 + " and " + card.city2 +
                  " thus lost " + str(card.points) + " points.")
    for card in playerTwo.getDestCards():
        if not card.completed:
            playerTwo.points -= card.points
            print("Player two did not complete the destination card between " + card.city1 + " and " + card.city2 +
                  " thus lost " + str(card.points) + " points.")

    currentTurn.addFinalScores(playerOne, playerTwo)
    if csvFlag:
        currentTurn.writeToCSV()

    # next lines find and print the winner of the game (all based on points) !!! make it also check for num destination cards completed if score ties
    if playerOne.points > playerTwo.points:
        print("Player one won with " + str(playerOne.points) + " over player two who had " + str(
            playerTwo.points) + ".")
        p1Wins += 1
    elif playerOne.points < playerTwo.points:
        print("Player two won with " + str(playerTwo.points) + " over player one who had " + str(
            playerOne.points) + ".")
        p2Wins += 1
    else:  # then test number of destination cards as a tie breaker
        p1DCount = 0
        for dCard in playerOne.destinationCards:
            if dCard.completed:
                p1DCount += 1
        p2DCount = 0
        for dCard in playerTwo.destinationCards:
            if dCard.completed:
                p2DCount += 1
        if p1DCount > p2DCount:
            print("Player one won with " + str(playerOne.points) + " over player two who also had " + str(
                playerTwo.points) + " because player one completed " + str(p1DCount) + " destination cards"
                " compared to player two who only completed " + str(p2DCount) + " destination cards.")
            p1Wins += 1
        elif p1DCount < p2DCount:
            print("Player two won with " + str(playerTwo.points) + " over player one who also had " + str(
                playerOne.points) + " because player two completed " + str(p2DCount) + " destination cards"
                " compared to player one who only completed " + str(p1DCount) + " destination cards.")
            p2Wins += 1
        else:
            print("It was a draw! Both players had " + str(playerTwo.points) + " points and completed " + str(p2DCount)
                  + " destination cards.")

    print("So far player one has won " + str(p1Wins) + " times, and player two has won " + str(p2Wins) + " times.")

    if loopsRemaining > 0:
        gameStart(loopsRemaining)
    titleScreen()
    quit()
    # saving full gamestate array to file at end of game
    # np.save(os.getcwd()+'/saves/save.npy', np.array(GameStateArray))


if commandlineFlag == 'cmd':
    gameStart()
titleScreen()
settings()
gameStart()