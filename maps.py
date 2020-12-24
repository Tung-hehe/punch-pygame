import pygame
import setting
import platforms
import monsters
import items

def load_ground(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    ground = []
    for tile in data:
        ground.append(list(tile))
    return ground

class Map(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a map.
        Create a child class for each map with map-specific info."""

    # Lists of sprites used in all maps
    platform_list = None
    enemy_list = None
    item_list = None

    # Background map
    background = None
    ground = None

    # How far this map been scrolled
    map_scroll = 0
    map_limit = 0

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        """ Update everything on this map"""
        self.enemy_list.update()
        self.item_list.update()
        for enemy in self.enemy_list:
            if abs(enemy.rect.x - self.player.rect.x) <= 50:
                enemy.attacking = True
                enemy.HP -= 1
        hits = pygame.sprite.spritecollide(self.player, self.enemy_list,
                                           False, pygame.sprite.collide_mask)

    def draw(self, screen):
        """ Draw everything on this map"""

        # Draw background
        screen.blit(self.background, (0, 0))
        # Draw all platform
        screen.blit(self.ground, (self.map_scroll, 0))

        # Draw all enemmy
        for enemy in self.enemy_list:
            enemy.draw_health()
            enemy.draw(screen)
        # Draw all item
        self.item_list.draw(screen)

    def scroll_map(self, scroll_x):
        """ When the user moves left/right and we need to scroll everything"""

        self.map_scroll += scroll_x

        for platform in self.platform_list:
            platform.rect.x += scroll_x

        for enemy in self.enemy_list:
            enemy.rect.x += scroll_x

class Map_01(Map):
    """ Create map 1. """

    def __init__(self, player):
        # Call the parent constructor
        Map.__init__(self, player)

        self.background = pygame.image.load('image/Map_1/background.png').convert()
        self.ground = pygame.image.load('image/Map_1/front_map.png').convert_alpha()
        self.ground.set_colorkey(setting.WHITE)
        tiles = load_ground('image/Map_1/map.txt')
        self.map_limit = setting.TILE_SIZE * len(tiles[0])
        for x in range(len(tiles)):
            for y in range(len(tiles[0])):
                if tiles[x][y] != '0':
                    tile = platforms.Platform(y * setting.TILE_SIZE, x * setting.TILE_SIZE)
                    self.platform_list.add(tile)
        enemy = monsters.Wolf(1020,258)
        self.enemy_list.add(enemy)
        item = items.Coin(20,20)
        self.item_list.add(item)
        item = items.Coin(50, 50)
        self.item_list.add(item)
        item = items.Coin(80, 80)
        self.item_list.add(item)
        item = items.Coin(110, 110)
        self.item_list.add(item)
