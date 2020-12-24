import pygame
import setting
import sprites
class Monster(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a kind of monster.
        Create a child class for each kind of monster."""

    ## What direction is the monster facing?
    face_right = False
    # Is monster attacking?
    attacking = False
    # Is monster is moving
    moving = False
    # Velcity of monster
    vel = [0, 0]
    # Frame for stand, run action
    frame = 0
    # Frame for attack action
    attack_frame = 0
    # Image for monster
    image = None
    rect = None
    size = (0,0)
    mask = None
    # All action of monster
    stand_r = None
    stand_l = None
    attack_r = None
    attack_l = None
    dead_r = None
    dead_l = None
    run_r = None
    run_l = None
    # HP of monster
    HP = 0
    # Range attack

    def __init__(self):
        """ Constructor function"""
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        """ This function used to update the monster (cordinates, image). """

        # Monster moving
        if self.moving:
            self.frame += setting.SPEED_RUN
            if self.face_right:
                self.vel[0] += setting.MONSTER_VEL
                self.image = self.run_r[int(self.frame)%len(self.run_r)]
            else:
                self.vel[0] -= setting.MONSTER_VEL
                self.image = self.run_l[int(self.frame) % len(self.run_l)]
        # Monster standing
        else:
            self.frame += setting.SPEED_STAND
            if self.face_right:
                self.image = self.stand_r[int(self.frame) % len(self.stand_r)]
            else:
                self.image = self.stand_l[int(self.frame) % len(self.stand_l)]

        if self.attacking:
            self.attack_frame += setting.SPEED_ATTACK
            if self.attack_frame >= len(self.attack_r):
                self.attacking = False
            if self.face_right:
                self.image = self.attack_r[int(self.attack_frame) % len(self.attack_r)]
            else:
                self.image = self.attack_l[int(self.attack_frame) % len(self.attack_l)]

        if self.vel[0] <= -setting.MONSTER_MAX_X:
            self.vel[0] = -setting.MONSTER_MAX_X
        if self.vel[0] >= setting.MONSTER_MAX_X:
            self.vel[0] = setting.MONSTER_MAX_X
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        # Get size, mask of image
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
    def AI(self, target, platforms):
        pass
    def draw_health(self):
        pass

    def draw(self, screen):
        """ This is a function used to draw monster. """
        screen.blit(self.image,
                    (self.rect.x - (self.size[0] - self.rect.w)/2,
                     self.rect.y - (self.size[1] - self.rect.h)))
        """ Why do we have to draw on the screen at this coordinate?
            Because the images in different actions are of different sizes.
            And we need the player in the middle. """

class Wolf(Monster):
    """ Create Wolf"""
    def __init__(self, x, y):
        Monster.__init__(self)
        """ Load all images of Wolf"""
        self.stand_r = sprites.load_sprite('image/Monster/Wolf/stand/', 4)
        self.stand_l = sprites.hori_flip_sprite('image/Monster/Wolf/stand/', 4)
        self.attack_r = sprites.load_sprite('image/Monster/Wolf/attack/', 7)
        self.attack_l = sprites.hori_flip_sprite('image/Monster/Wolf/attack/', 7)
        self.dead_r = sprites.load_sprite('image/Monster/Wolf/dead/', 9)
        self.dead_l = sprites.hori_flip_sprite('image/Monster/Wolf/dead/', 9)
        self.run_r = sprites.load_sprite('image/Monster/Wolf/run/', 6)
        self.run_l = sprites.hori_flip_sprite('image/Monster/Wolf/run/', 6)

        # Get image
        self.image = self.stand_r[0]
        # Get rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        # Get mask
        self.mask = pygame.mask.from_surface(self.image)
        self.HP = 100
    # def draw_health(self):
    #     col = setting.RED
    #     width = int(self.rect.w * self.HP/setting.MONSTER_MAX_HEALTH)
    #     self.health_bar = pygame.Rect(0, 0, width, 7)
    #     if self.HP < setting.MONSTER_MAX_HEALTH:
    #         pygame.draw.rect(self.image, col, self.health_bar)