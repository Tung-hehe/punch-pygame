import pygame
from setting import *

vec = pygame.math.Vector2
def load_sprite(file_name, num_image):
    sprite_sheet = [pygame.image.load(file_name + str(i+1) + '.png') for i in range(num_image)]
    return sprite_sheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.image = self.stand[0]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.current_frame = 0
        self.current_attack = 0
        self.attack_q = False
        self.attack_e = False
        self.attack_r = False
        self.attack_f = False
        self.moving = False
        self.face_right = True
        self.cout_jump = 0
        self.vel = vec(0., 0.5)
    def load_image(self):
        self.stand = load_sprite('image/Player/stand/', 6)
        self.run = load_sprite('image/Player/run/', 8)
        self.jump = load_sprite('image/Player/jump/', 4)
        self.combo1 = load_sprite('image/Player/attack/combo1/', 8)
        self.combo2 = load_sprite('image/Player/attack/combo2/', 7)
        self.combo3 = load_sprite('image/Player/attack/combo3/', 8)
        self.combo4 = load_sprite('image/Player/attack/combo4/', 7)
    def animate(self, action):
        self.current_frame += 0.2
        if self.face_right == True:
            self.image = action[int(self.current_frame) % len(action)]
        else:
            self.image = pygame.transform.flip(action[int(self.current_frame) % len(action)], True, False)
    def update(self):
        self.vel.y += GRAVITY
        if self.vel.y > PLAYER_MAX_Y:
            self.vel.y = PLAYER_MAX_Y
        # if self.jump:
        #     if self.face_right:
        #         self.vel.x += PLAYER_ACC
        #     self.animate(self.jump)
        if self.moving:
            if self.face_right:
                self.vel.x += PLAYER_ACC
            else:
                self.vel.x -= PLAYER_ACC
            self.animate(self.run)
        else:
            self.animate(self.stand)
            self.vel.x = 0
        if self.vel.x <= -PLAYER_MAX_X:
            self.vel.x = -PLAYER_MAX_X
        if self.vel.x >= PLAYER_MAX_X:
            self.vel.x = PLAYER_MAX_X
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.attack_q:
            self.current_attack += 0.2
            if self.current_attack >= len(self.combo1):
                self.current_attack = 0
                self.attack_q = False
            if self.face_right:
                self.image = self.combo1[int(self.current_attack)]
            else:
                self.image = pygame.transform.flip(self.combo1[int(self.current_attack)], True, False)
        if self.attack_r:
            self.current_attack += 0.2
            if self.current_attack >= len(self.combo3):
                self.current_attack = 0
                self.attack_r = False
            if self.face_right:
                self.image = self.combo3[int(self.current_attack)]
            else:
                self.image = pygame.transform.flip(self.combo3[int(self.current_attack)], True, False)
        if self.attack_e:
            self.current_attack += 0.2
            if self.current_attack >= len(self.combo2):
                self.current_attack = 0
                self.attack_e = False
            if self.face_right:
                self.image = self.combo2[int(self.current_attack)]
            else:
                self.image = pygame.transform.flip(self.combo2[int(self.current_attack)], True, False)
        if self.attack_f:
            self.current_attack += 0.2
            if self.current_attack >= len(self.combo4):
                self.current_attack = 0
                self.attack_f = False
            if self.face_right:
                self.image = self.combo4[int(self.current_attack)]
            else:
                self.image = pygame.transform.flip(self.combo4[int(self.current_attack)], True, False)
        self.size = self.image.get_size()

class Platform(pygame.sprite.Sprite):
     def __init__(self, x = 0, y = 0, type = '1'):
         pygame.sprite.Sprite.__init__(self)
         self.type = type
         self.image = pygame.image.load('image/Map_2/Tiles/Tile_' + self.type +'.png').convert_alpha()
         self.image.set_colorkey(WHITE)
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y
         self.pos = vec(self.rect.x, self.rect.y)