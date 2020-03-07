import pygame

# sets the window size to 800x600px
display_width = 1920
display_height = 1080

# Allows the background image to be loaded with a method background needs to be at least the size of the window
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(image_file), (display_width, display_height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
