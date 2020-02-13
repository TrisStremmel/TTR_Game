import pygame, sys
pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red =   (255,0,0)
green = (0,255,0)
blue =  (0,0,255)

screen = pygame.display.set_mode([display_width,display_height])
screen.fill(white)
pygame.display.set_caption("TTR")
clock = pygame.time.Clock()

whiteTrainImg = pygame.image.load('whiteTrain.png')
blackTrainImg = pygame.image.load('blackTrain.png')

def trainCard(color,x,y):
    if color == white:
        screen.blit(whiteTrainImg,(x,y))
    if color == black:
        screen.blit(blackTrainImg,(x,y))

crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
##        print(event)
    trainCard(white,display_width * 0.05,display_height * 0.9)
    trainCard(black,display_width * 0.15,display_height * 0.9)
    pygame.display.update()
    clock.tick(10)
pygame.quit()
quit()
 
