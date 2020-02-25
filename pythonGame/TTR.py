import pygame
import sys

pygame.init()

# sets the window size to 800x600px
display_width = 1024
display_height = 512

# easy access to colors
black = (0, 0, 0)
grey = (139, 139, 139)
white = (255, 255, 255)
red = (255, 0, 0)
darkred = (139, 0, 0)
green = (0, 255, 0)
darkgreen = (0, 139, 0)
blue = (0, 0, 255)
darkblue = (0, 0, 139)


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


# Allows the background image to be loaded with a method background needs to be at least the size of the window
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# card class, holds color
class Card:

    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color


# noinspection PyAttributeOutsideInit
class MovingCard:

    def __init(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        return self.color

    def setX(self, X):
        self.x = X

    def setY(self, Y):
        self.y = Y

    def setColor(self, color):
        self.color = color


# makes the screen as wide and tall as above variables, makes a white background, adds TTR title, and starts a clock
screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption("Ticket To Ride")
clock = pygame.time.Clock()
BackGround = Background('Ticket To Ride Assets\BackGrounds\Background.png', [0, 0])
TitleScreenImg = Background('Ticket To Ride Assets\BackGrounds\TitleScreen.png', [0, 0])

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


def quitGame():
    pygame.quit()
    quit()


def titleScreen():
    print(pygame.font.get_fonts())
    start = True
    screen.fill(white)

    screen.blit(TitleScreenImg.image, TitleScreenImg.rect)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
        button("Start Train-ing", 20, 400, 100, 200, 75, green, darkgreen, gameLoop)
        button("Coward", 20, 400, 200, 200, 75, red, darkred, quitGame)

        pygame.display.update()
        clock.tick(10)


def gameLoop():
    numCards = 0
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

    # draws the black and white train card on the card piles over the hit boxes
    screen.blit(whiteDeckImg, (display_width * 0.012, display_height * 0.75))
    screen.blit(pinkDeckImg, (display_width * 0.112, display_height * 0.75))
    screen.blit(redDeckImg, (display_width * 0.212, display_height * 0.75))
    screen.blit(orangeDeckImg, (display_width * 0.312, display_height * 0.75))
    screen.blit(yellowDeckImg, (display_width * 0.412, display_height * 0.75))
    screen.blit(greenDeckImg, (display_width * 0.512, display_height * 0.75))
    screen.blit(blueDeckImg, (display_width * 0.612, display_height * 0.75))
    screen.blit(blackDeckImg, (display_width * 0.712, display_height * 0.75))

    # initialised the hand array and keeps track of the card index
    handCards = []
    cardIndex = 0

    running = True
    while running:
        button("Title Screen", 17, display_width * 0.85, display_height * 0.65, 100, 75, blue, darkblue, titleScreen)
        button("Coward", 20, display_width * 0.85, display_height * 0.8, 100, 75, red, darkred, quitGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if len(handCards) >= 14:
                    print('There are 14 cards in your hand, you can not draw any more!')

                elif whiteDeck.collidepoint(pos):
                    print('added white card to your hand')
                    handCards.append(Card('white'))
                    screen.blit(whiteTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif pinkDeck.collidepoint(pos):
                    print('added pink card to your hand')
                    handCards.append(Card('pink'))
                    screen.blit(pinkTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif redDeck.collidepoint(pos):
                    print('added red card to your hand')
                    handCards.append(Card('red'))
                    screen.blit(redTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif orangeDeck.collidepoint(pos):
                    print('added orange card to your hand')
                    handCards.append(Card('orange'))
                    screen.blit(orangeTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif yellowDeck.collidepoint(pos):
                    print('added yellow card to your hand')
                    handCards.append(Card('yellow'))
                    screen.blit(yellowTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif greenDeck.collidepoint(pos):
                    print('added green card to your hand')
                    handCards.append(Card('green'))
                    screen.blit(greenTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif blueDeck.collidepoint(pos):
                    print('added blue card to your hand')
                    handCards.append(Card('blue'))
                    screen.blit(blueTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

                elif blackDeck.collidepoint(pos):
                    handCards.append(Card('black'))
                    print('added black card to your hand')
                    screen.blit(blackTrainImg, (display_width * 0.05 + (50 * cardIndex), display_height * 0.05))
                    cardIndex += 1

        pygame.display.update()
        clock.tick(10)
    pygame.quit()
    quit()


titleScreen()
gameLoop()
