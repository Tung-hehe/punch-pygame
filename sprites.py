import pygame
from setting import *

def load_sprite(file_name, num_image):
    """ This is a function used to load image"""
    sprite_sheets = [pygame.image.load(file_name + str(i+1) + '.png').convert_alpha() for i in range(num_image)]
    for sprite_sheet in sprite_sheets:
        sprite_sheet.set_colorkey(WHITE)
    return sprite_sheets
def hori_flip_sprite(file_name, num_image):
    """This is a function used to horizontal flip image"""
    sprite_sheets = load_sprite(file_name, num_image)
    result = []
    for sprite_sheet in sprite_sheets:
        sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
        result.append(sprite_sheet)
    return  result