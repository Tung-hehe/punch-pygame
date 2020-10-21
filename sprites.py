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
        self.vel = vec(0, 0)
        self.face_right = True
        self.moving = False
        self.attacking = False
        self.jumping = False
        self.falling = False
        self.normal_frame = 0
        self.attack_frame = 0
        self.jump_frame = 0
        self.cout_jump = 0

    def load_image(self):
        self.stand = load_sprite('image/Player/stand/', 6)
        self.run = load_sprite('image/Player/run/', 8)
        self.jump = [[pygame.image.load('image/Player/jump/1.png')],
                     [pygame.image.load('image/Player/jump/' + str(i+1) + '.png') for i in range(4,9)]]
        self.fall = [[pygame.image.load('image/Player/jump/' + str(i+1) + '.png') for i in range(1,4)],
                     [pygame.image.load('image/Player/jump/' + str(i+1) + '.png') for i in range(9,12)]]
        self.punch = [load_sprite('image/Player/attack/punch1/', 4),
                      load_sprite('image/Player/attack/punch2/', 4),
                      load_sprite('image/Player/attack/punch3/', 8)]
        self.kick = load_sprite('image/Player/attack/kick/',7)
        self.block = load_sprite('image/Player/block/',7)

    def move(self, tiles):
        self.rect.x += self.vel.x
        hits_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hits_list:
            if self.vel.x > 0:
                self.rect.right = hit.rect.left
            if self.vel.x < 0:
                self.rect.left = hit.rect.right
        self.rect.y += self.vel.y
        hits_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hits_list:
            if self.vel.y > 0:
                self.rect.bottom = hit.rect.top
                self.falling = False
            if self.vel.y < 0:
                self.rect.top = hit.rect.bottom
            self.cout_jump = 0
        if len(hits_list) == 0:
            self.falling = True

    def animate(self, action, speed):
        self.normal_frame += speed
        if self.face_right == True:
            self.image = action[int(self.normal_frame) % len(action)]
        else:
            self.image = pygame.transform.flip(action[int(self.normal_frame) % len(action)], True, False)

    def update(self):
        if self.moving:
            if self.face_right:
                self.vel.x += PLAYER_ACC
            else:
                self.vel.x -= PLAYER_ACC
            if not self.jumping and not self.falling:
                self.animate(self.run, SPEED_RUN)
        else:
            self.animate(self.stand, SPEED_STAND)
            self.vel.x = 0
        if self.jumping:
            self.vel.x = 0
            self.falling = False
            self.jump_frame += SPEED_JUMP
            if self.jump_frame >= len(self.jump[self.cout_jump]):
                self.jumping = False
                self.jump_frame = 0
                self.falling = True
                self.vel.y = -PLAYER_MAX_Y + 2
            if self.face_right:
                self.image = self.jump[self.cout_jump][int(self.jump_frame)]
            else:
                self.image = pygame.transform.flip(self.jump[self.cout_jump][int(self.jump_frame)], True, False)
        if self.falling:
            self.vel.y += GRAVITY
            self.animate(self.fall[self.cout_jump], SPEED_FALL)
        if self.attacking:
            self.vel.x = 0
            self.attack_frame += SPEED_ATTACK
            if self.attack_frame >= len(self.punch[0]) + len(self.punch[1]):
                self.attacking = False
                self.attack_frame = 0
            if self.face_right:
                if self.attack_frame < len(self.punch[0]):
                    self.image = self.punch[0][int(self.attack_frame)]
                if self.attack_frame >= len(self.punch[0]) and self.attack_frame < len(self.punch[0]) + len(self.punch[1]):
                    self.image = self.punch[1][int(self.attack_frame)%len(self.punch[1])]
            else:
                if self.attack_frame < len(self.punch[0]):
                    self.image = pygame.transform.flip(self.punch[0][int(self.attack_frame)], True, False)
                if self.attack_frame >= len(self.punch[0]) and self.attack_frame < len(self.punch[0]) + len(self.punch[1]):
                    self.image = pygame.transform.flip(self.punch[1][int(self.attack_frame)%len(self.punch[1])], True, False)
        if self.vel.y > PLAYER_MAX_Y:
            self.vel.y = PLAYER_MAX_Y
        if self.vel.x <= -PLAYER_MAX_X:
            self.vel.x = -PLAYER_MAX_X
        if self.vel.x >= PLAYER_MAX_X:
            self.vel.x = PLAYER_MAX_X
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
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