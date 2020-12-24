import pygame
import sprites
import setting


class Item(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a kind of item.
        Create a child class for each kind of item."""

    image = None
    rect = None
    mask = None
    frame = 0

    def __init__(self):
        """ Constructor function. """
        pygame.sprite.Sprite.__init__(self)

    def draw(self, screen):
        """ This function used to draw item. """
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Coin(Item):
    """ Create coin class"""
    def __init__(self,x,y):
        """ Constructor function"""
        Item.__init__(self)
        self.images = sprites.load_sprite('image/Coins/Style 2/', 6)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """ This function used to update image of item. """
        self.frame += setting.SPEED_STAND
        self.image = self.images[int(self.frame) % len(self.images)]
