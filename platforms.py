import pygame
from setting import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)