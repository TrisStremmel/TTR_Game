from typing import Any
from random import *
import pygame
import math
import sys
from Background import Background
from Edge import Edge
from City import City
from Card import Card
from Player import Player
from Track import Track

pygame.init()

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
screen = pygame.display.set_mode([display_width, display_height])
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

blankTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Blank.png')
redTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Red.png')
orangeTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Orange.png')
yellowTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Yellow.png')
greenTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Green.png')
blueTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Blue.png')
pinkTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Pink.png')
whiteTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_White.png')
blackTrack = pygame.image.load('Ticket To Ride Assets\Tracks\Bar\Track_Black.png')

human = Player()
bot = Player()

screen.blit(blackTrainImg, (display_width * 0.05, display_height * 0.9))
screen.blit(whiteTrainImg, (display_width * 0.15, display_height * 0.9))

BackGround = Background('Ticket To Ride Assets\BackGrounds\Background.png', [0, 0])
TitleScreenImg = Background('Ticket To Ride Assets\BackGrounds\TitleScreen.png', [0, 0])

##numNodes = input('How many cities?')

cityConnection = ([[-1, Edge(3, 'black'), -1, Edge(5, 'white'), Edge(2,  'black'), -1, -1],
                   [Edge(3, 'black'), -1, Edge(4, 'white'), -1, -1, -1, -1],
                   [-1, Edge(4, 'white'), -1, Edge(6, 'black'), -1, Edge(4, 'black'), -1],
                   [Edge(5, 'white'), -1, Edge(6, 'black'), -1, -1, -1, Edge(3, 'white')],
                   [Edge(2, 'black'), -1, -1, -1, -1, Edge(3, 'white'), Edge(3, 'white')],
                   [-1, -1, Edge(4, 'black'), -1, Edge(3, 'white'), -1, Edge(2, 'black')],
                   [-1, -1, -1, Edge(3, 'white'), Edge(3, 'white'), Edge(2, 'black'), -1]])

cityNames = ['Washington', 'Montana', 'New York', 'Texas', 'Colorado', 'Kansas', 'Oklahoma']

# numNodes = input('How many cities?')
# cityNames = ['Los Angeles', 'Seattle', 'New York', 'Dallas', 'Salt Lake', 'Milwaukee', 'Chicago']
# cities = [City(1, 2, 'Los Angeles', red), City(3, 4, 'Seattle', blue), City(5, 6, 'New York', green),

def quitGame():
    pygame.quit()
    quit()


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
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.Font('freesansbold.ttf', fs)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x + (w / 2), (y + (h / 2)))
    screen.blit(textSurf, textRect)


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
        button("Start Train-ing", 20, 400, 100, 200, 75, green, darkGreen, gameLoop)
        button("Settings", 20, 400, 200, 200, 75, blue, darkBlue, settings)
        button("Quit", 20, 400, 300, 200, 75, red, darkRed, quitGame)

        pygame.display.update()
        clock.tick(10)


def settings():
    screen.fill(white)
    screen.blit(BackGround.image, BackGround.rect)
    running = True
    while running:
        button("Title Screen", 20, 400, 100, 200, 75, blue, darkBlue, titleScreen)
        button("Quit", 20, 400, 300, 200, 75, red, darkRed, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            pygame.display.update()
        clock.tick(10)

def strToObj(name):
    return eval(name)

def drawHand(color):
    print('added ' + color + ' card to your hand')
    human.handCards.append(Card('white', randint(1, 10)))
    screen.blit(globals()[color + 'TrainImg'], (display_width * 0.85, display_height * 0.13 + (40 * human.cardIndex)))
    human.cardIndex += 1

def cityNameDisplay(text, x, y):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((x),(y))
    screen.blit(TextSurf, TextRect)

WA = City(int(display_width * 0.1), int(display_height * 0.15))
CO = City(int(display_width * 0.3), int(display_height * 0.35))
MT = City(int(display_width * 0.35), int(display_height * 0.1))
TX = City(int(display_width * 0.4), int(display_height * 0.7))
OK = City(int(display_width * 0.475), int(display_height * 0.45))
KS = City(int(display_width * 0.5), int(display_height * 0.25))
NY = City(int(display_width * 0.75), int(display_height * 0.2))

stateArray = [WA, MT, NY, TX, CO, KS, OK]

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


    pygame.draw.circle(screen, white, [WA.getX(), WA.getY()], 50, 50)
    pygame.draw.circle(screen, white, [CO.getX(), CO.getY()], 50, 50)
    pygame.draw.circle(screen, white, [MT.getX(), MT.getY()], 50, 50)
    pygame.draw.circle(screen, white, [TX.getX(), TX.getY()], 50, 50)
    pygame.draw.circle(screen, white, [OK.getX(), OK.getY()], 50, 50)
    pygame.draw.circle(screen, white, [KS.getX(), KS.getY()], 50, 50)
    pygame.draw.circle(screen, white, [NY.getX(), NY.getY()], 50, 50)

    cityNameDisplay("WA", WA.getX(), WA.getY())
    cityNameDisplay("CO", CO.getX(), CO.getY())
    cityNameDisplay("MT", MT.getX(), MT.getY())
    cityNameDisplay("TX", TX.getX(), TX.getY())
    cityNameDisplay("OK", OK.getX(), OK.getY())
    cityNameDisplay("KS", KS.getX(), KS.getY())
    cityNameDisplay("NY", NY.getX(), NY.getY())

    # draws the black and white train card on the card piles over the hit boxes
    screen.blit(whiteDeckImg, (display_width * 0.017, display_height * 0.75))
    screen.blit(pinkDeckImg, (display_width * 0.117, display_height * 0.75))
    screen.blit(redDeckImg, (display_width * 0.217, display_height * 0.75))
    screen.blit(orangeDeckImg, (display_width * 0.317, display_height * 0.75))
    screen.blit(yellowDeckImg, (display_width * 0.417, display_height * 0.75))
    screen.blit(greenDeckImg, (display_width * 0.517, display_height * 0.75))
    screen.blit(blueDeckImg, (display_width * 0.617, display_height * 0.75))
    screen.blit(blackDeckImg, (display_width * 0.717, display_height * 0.75))

trackDataArray = [[-1 for x in range(11)] for y in range(11)]
    #draws the tracks
def drawTracks():
    for i in range(0, len(cityConnection), 1):
        for j in range(i, len(cityConnection[i]), 1):
            if cityConnection[i][j] != -1:
                length = cityConnection[i][j].getLength()
                color = cityConnection[i][j].getColor()
                x1 = stateArray[i].getX()
                y1 = stateArray[i].getY()
                x2 = stateArray[j].getX()
                y2 = stateArray[j].getY()
                difx = x2 - x1
                dify = y2 - y1
                radians = math.atan2(dify, difx)
                rot = math.degrees(radians)

                perLenX= difx/length
                perLeny= dify/length

                trackImg = pygame.transform.scale(strToObj(color + "Track"), (100, 50))
                trackImgFin = pygame.transform.rotate(trackImg, -rot)

                for pri in range(1, length+1):
                    left = x1 + (perLenX*pri*.8) - 50
                    top = y1 + (perLeny*pri*.8) - 50
                    screen.blit(trackImgFin, (left, top))

                    trackDataArray[i][pri-1] = Track(top, left, abs(dify), abs(difx), color, trackImgFin, -rot)

                    '''
                    print(top)
                    print(left)
                    print(difx)
                    print(dify)
                    '''

def gameLoop():
    numCards = 0

    playerTurn = True

    screen.fill(white)

    screen.blit(BackGround.image, BackGround.rect)

    # draws the hit boxes for the white and black card draw piles
    whiteDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.03, display_height * 0.77, 100, 100), 1)
    pinkDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.13, display_height * 0.77, 100, 100), 1)
    redDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.23, display_height * 0.77, 100, 100), 1)
    orangeDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.33, display_height * 0.77, 100, 100), 1)
    yellowDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.43, display_height * 0.77, 100, 100), 1)
    greenDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.53, display_height * 0.77, 100, 100), 1)
    blueDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.63, display_height * 0.77, 100, 100), 1)
    blackDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.73, display_height * 0.77, 100, 100), 1)

    deackArray = [whiteDeck, pinkDeck, redDeck, orangeDeck, yellowDeck, greenDeck, blueDeck, blackDeck]

    drawTracks()
    drawGameBoard()
    running = True

    while running:
        button("Title Screen", 17, display_width * 0.85, display_height * 0.05, 100, 75, blue, darkBlue, titleScreen)
        button("Quit", 20, display_width * 0.85, display_height * 0.8, 100, 75, red, darkRed, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if playerTurn:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    if len(human.handCards) >= 14:
                        print('There are 14 cards in your hand, you can not draw any more!')

                    elif whiteDeck.collidepoint(pos):
                        drawHand('white')

                    elif pinkDeck.collidepoint(pos):
                        drawHand('pink')

                    elif redDeck.collidepoint(pos):
                        drawHand('red')

                    elif orangeDeck.collidepoint(pos):
                        drawHand('orange')

                    elif yellowDeck.collidepoint(pos):
                        drawHand('yellow')

                    elif greenDeck.collidepoint(pos):
                        drawHand('green')

                    elif blueDeck.collidepoint(pos):
                        drawHand('blue')

                    elif blackDeck.collidepoint(pos):
                        drawHand('black')

                    else:
                        for i in range(0, len(trackDataArray), 1):
                            for j in range(0, len(trackDataArray[i]), 1):
                                data = trackDataArray[i][j]

                                if data == -1:
                                    break
                                else:
                                    #print(i)
                                    #print(data.getColor())
                                    pygame.draw.circle(screen, black, (int(data.getLeft()), int(data.getTop())), 10)
                                    if data.getImg().get_rect().move(data.getLeft(), data.getTop()).collidepoint(pos):
                                        print(trackDataArray[0][0].getColor())
                                        playerTurn = False

            ##ai decision
            if playerTurn == False:
                ##Call ai desision method/class here
                print("ai played its turn")
                playerTurn = True


        pygame.display.update()
        clock.tick(10)
    pygame.quit()
    quit()


titleScreen()
settings()
gameLoop()
