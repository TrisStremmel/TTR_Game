from typing import Any
from random import *
import pygame
import sys
from Background import Background
from Edge import Edge
from City import City
from Card import Card
from Player import Player

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
blueMovingImg = pygame.image.load('Ticket To Ride Assets\Blue\RotatedCard_Blue.png')
blackMovingImg = pygame.image.load('Ticket To Ride Assets\Black\RotatedCard_Black.png')

# loads images to act as the draw deck
whiteDeckImg = pygame.image.load('Ticket To Ride Assets\White\WhiteDeck.png')
pinkDeckImg = pygame.image.load('Ticket To Ride Assets\Pink\PinkDeck.png')
redDeckImg = pygame.image.load('Ticket To Ride Assets\Red\RedDeck.png')
orangeDeckImg = pygame.image.load('Ticket To Ride Assets\Orange\OrangeDeck.png')
yellowDeckImg = pygame.image.load('Ticket To Ride Assets\Yellow\YellowDeck.png')
greenDeckImg = pygame.image.load('Ticket To Ride Assets\Green\GreenDeck.png')
blueDeckImg = pygame.image.load('Ticket To Ride Assets\Blue\BlueDeck.png')
blackDeckImg = pygame.image.load('Ticket To Ride Assets\Black\BlackDeck.png')

human = Player()
bot = Player()


screen.blit(blackTrainImg,(display_width * 0.05,display_height * 0.9))
screen.blit(whiteTrainImg,(display_width * 0.15,display_height * 0.9))

BackGround = Background('Ticket To Ride Assets\BackGrounds\Background.png', [0, 0])
TitleScreenImg = Background('Ticket To Ride Assets\BackGrounds\TitleScreen.png', [0, 0])


##numNodes = input('How many cities?')

cityConnection = ([[-1,                      Edge(3, [0, 1], 'black'), -1,                      Edge(5, [0, 3],'white'),  Edge(2, [0, 4],'black'),  -1,                      -1],
                   [Edge(3, [1, 0],'black'), -1,                       Edge(4, [1, 2],'white'), -1,                       -1,                       -1,                      -1],
                   [-1,                      Edge(4, [2, 1],'white'),  -1,                      Edge(6, [2, 3],'black'),  -1,                       Edge(4, [2, 5],'black'), -1],
                   [Edge(5, [3, 0],'white'), -1,                       Edge(6, [3, 2],'black'), -1,                       -1,                       -1,                      Edge(3, [3, 6],'white')],
                   [Edge(2, [4, 0],'black'), -1,                        -1,                     -1,                       -1,                       Edge(3, [4, 5],'white'), Edge(3, [4, 6],'white')],
                   [-1,                      -1,                       Edge(4, [5, 2],'black'), -1,                       Edge(3,  [5, 4],'white'), -1,                      Edge(2, [5, 6],'black')],
                   [-1,                      -1,                        -1,                     Edge(3,  [6, 3],'white'), Edge(3,  [6, 4],'white'), Edge(2, [6, 5],'black'), -1]])

cityNames = ['Los Angeles', 'Seattle', 'New York', 'Dallas', 'Salt Lake', 'Milwaukee', 'Chicago']

# numNodes = input('How many cities?')
#cityNames = ['Los Angeles', 'Seattle', 'New York', 'Dallas', 'Salt Lake', 'Milwaukee', 'Chicago']
#cities = [City(1, 2, 'Los Angeles', red), City(3, 4, 'Seattle', blue), City(5, 6, 'New York', green),

'''
          City(6, 7, 'Dallas', black), City(7, 8, 'Salt Lake', white), City(8, 9, 'Milwaukee', red),
          City(10, 11, 'Chicago', blue)]
cityConnection = ([[-1, Edge(3, [0, 1], 'black'), -1, Edge(5, [0, 3], 'white'), Edge(2, [0, 4], 'black'), -1, -1],
                   [Edge(3, [1, 0], 'black'), -1, Edge(4, [1, 2], 'white'), -1, -1, -1, -1],
                   [-1, Edge(4, [2, 1], 'white'), -1, Edge(6, [2, 3], 'black'), -1, Edge(4, [2, 5], 'black'), -1],
                   [Edge(5, [3, 0], 'white'), -1, Edge(6, [3, 2], 'black'), -1, -1, -1, Edge(3, [3, 6], 'white')],
                   [Edge(2, [4, 0], 'black'), -1, -1, -1, -1, Edge(3, [4, 5], 'white'), Edge(3, [4, 6], 'white')],
                   [-1, -1, Edge(4, [5, 2], 'black'), -1, Edge(3, [5, 4], 'white'), -1, Edge(2, [5, 6], 'black')],
                   [-1, -1, -1, Edge(3, [6, 3], 'white'), Edge(3, [6, 4], 'white'), Edge(2, [6, 5], 'black'), -1]])
>>>>>>> f91e5c7cc1ac9b4fa6c184d2e4803e38f89820f3
'''

for row in cityConnection:
    for colm in row:
        if type(colm) != int:
            print(colm.getColor(), end=", ")
        else:
            print("none", end=", ")
    print("\n")


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
        button("Coward", 20, 400, 300, 200, 75, red, darkRed, quitGame)

        pygame.display.update()
        clock.tick(10)


def settings():
    screen.fill(white)
    screen.blit(BackGround.image, BackGround.rect)
    running = True
    while running:
        button("Title Screen", 20, 400, 100, 200, 75, blue, darkBlue, titleScreen)
        button("Coward", 20, 400, 300, 200, 75, red, darkRed, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            pygame.display.update()
        clock.tick(10)

def drawHand(color):
    print('added ' + color + ' card to your hand')
    human.handCards.append(Card('white', randint(1, 10)))
    print(len(human.handCards))
    # pos = (display_width * 0.05 + (50 * cardIndex), display_height * 0.05)
    screen.blit(globals()[color + 'TrainImg'], (display_width * 0.85, display_height * 0.13 + (40 * human.cardIndex)))
    human.cardIndex += 1

def drawGameBoard():
    pygame.draw.circle(screen, black, [80, 80], 80, 10)
    pygame.draw.circle(screen, black, [80, 80], 80, 1)
    pygame.draw.circle(screen, black, [80, 80], 80, 1)
    pygame.draw.circle(screen, black, [80, 80], 80, 1)




def gameLoop():
    numCards = 0
    screen.fill(white)

    screen.blit(BackGround.image, BackGround.rect)

    # draws the hit boxes for the white and black card draw piles
    #  pygame.Surface.set_colorkey(255,255,255)
    whiteDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.03, display_height * 0.77, 100, 100), 1)
    pinkDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.13, display_height * 0.77, 100, 100), 1)
    redDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.23, display_height * 0.77, 100, 100), 1)
    orangeDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.33, display_height * 0.77, 100, 100), 1)
    yellowDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.43, display_height * 0.77, 100, 100), 1)
    greenDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.53, display_height * 0.77, 100, 100), 1)
    blueDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.63, display_height * 0.77, 100, 100), 1)
    blackDeck = pygame.draw.rect(screen, (255, 255, 255), (display_width * 0.73, display_height * 0.77, 100, 100), 1)

    # draws the black and white train card on the card piles over the hit boxes
    screen.blit(whiteDeckImg, (display_width * 0.012, display_height * 0.75))
    screen.blit(pinkDeckImg, (display_width * 0.112, display_height * 0.75))
    screen.blit(redDeckImg, (display_width * 0.212, display_height * 0.75))
    screen.blit(orangeDeckImg, (display_width * 0.312, display_height * 0.75))
    screen.blit(yellowDeckImg, (display_width * 0.412, display_height * 0.75))
    screen.blit(greenDeckImg, (display_width * 0.512, display_height * 0.75))
    screen.blit(blueDeckImg, (display_width * 0.612, display_height * 0.75))
    screen.blit(blackDeckImg, (display_width * 0.712, display_height * 0.75))

    drawGameBoard()

    # initialised the hand array and keeps track of the card index

    running = True


    while running:
        button("Title Screen", 17, display_width * 0.85, display_height * 0.05, 100, 75, blue, darkBlue, titleScreen)
        button("Coward", 20, display_width * 0.85, display_height * 0.8, 100, 75, red, darkRed, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if len(human.handCards) >= 14:
                    print('There are 14 cards in your hand, you can not draw any more!')

                elif whiteDeck.collidepoint(pos):
                    print('added white card to your hand')
                    drawHand('white')

                elif pinkDeck.collidepoint(pos):
                    print('added pink card to your hand')
                    drawHand('pink')

                elif redDeck.collidepoint(pos):
                    print('added red card to your hand')
                    drawHand('red')

                elif orangeDeck.collidepoint(pos):
                    print('added orange card to your hand')
                    drawHand('orange')

                elif yellowDeck.collidepoint(pos):
                    print('added yellow card to your hand')
                    drawHand('yellow')

                elif greenDeck.collidepoint(pos):
                    print('added green card to your hand')
                    drawHand('green')

                elif blueDeck.collidepoint(pos):
                    print('added blue card to your hand')
                    drawHand('blue')

                elif blackDeck.collidepoint(pos):
                    print('added black card to your hand')
                    drawHand('black')

        pygame.display.update()
        clock.tick(10)
    pygame.quit()
    quit()


titleScreen()
settings()
gameLoop()
