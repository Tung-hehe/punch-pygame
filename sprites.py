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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.cout_attack = 0
        self.start_attack = pygame.time.get_ticks()
        self.type_attack = self.punch

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
        self.kick = [load_sprite('image/Player/attack/kick1/', 7), 
                     load_sprite('image/Player/attack/kick2/', 7)]
        self.block = [load_sprite('image/Player/block/',7)]

    def move_x(self, tiles):
        self.rect.x += self.vel.x
        hits_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hits_list:
            if self.vel.x > 0:
                self.rect.right = hit.rect.left
            if self.vel.x < 0:
                self.rect.left = hit.rect.right
    def move_y(self, tiles):
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

    # def animate(self, action, speed):
    #     self.normal_frame += speed
    #     if self.face_right:
    #         self.image = action[int(self.normal_frame) % len(action)]
    #     else:
    #         self.image = pygame.transform.flip(action[int(self.normal_frame) % len(action)], True, False)
    def animate(self, action, speed):
        self.normal_frame += speed
        frame_action = action[int(self.normal_frame) % len(action)]
        if self.face_right:
            image_action = frame_action
        else:
            image_action = pygame.transform.flip(frame_action, True, False)
        self.image = image_action
    
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
            if self.attack_frame >= len(self.type_attack[self.cout_attack]):
                self.attacking = False
                self.attack_frame = 0
                self.cout_attack += 1
            if self.cout_attack >= len(self.type_attack):
                self.cout_attack = 0
            if self.face_right:
                self.image = self.type_attack[self.cout_attack][int(self.attack_frame)]
            else:
                self.image = pygame.transform.flip(self.type_attack[self.cout_attack][int(self.attack_frame)], True, False)
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
        self.mask = pygame.mask.from_surface(self.image)

class Platform(pygame.sprite.Sprite):
     def __init__(self, x = 0, y = 0):
         pygame.sprite.Sprite.__init__(self)
         self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0, type = "Wolf"):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.load_image()
        self.image = self.stand[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.face_right = False
        self.attacking = False
        self.moving = False
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.normal_frame = 0
        self.attack_frame = 0
        self.pause_attack = 0
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
    def load_image(self):
        self.stand = load_sprite('image/Monster/' + self.type +'/stand/', 4)
        self.attack = load_sprite('image/Monster/Wolf/attack/', 7)
        self.dead = load_sprite('image/Monster/Wolf/dead/', 9)
    def animate(self, action, speed):
        self.normal_frame += speed
        if self.face_right:
            self.image = action[int(self.normal_frame) % len(action)]
        else:
            self.image = pygame.transform.flip(action[int(self.normal_frame) % len(action)], True, False)
    def update(self):
        if self.attacking:
            self.vel.x = 0
            self.attack_frame += SPEED_ATTACK
            if self.attack_frame >= len(self.attack):
                self.attacking = False
                self.pause_attack = pygame.time.get_ticks()
                self.attack_frame = 0
            if self.face_right:
                self.image = self.attack[int(self.attack_frame)]
            else:
                self.image = pygame.transform.flip(self.attack[int(self.attack_frame)], True, False)
        else:
            self.animate(self.stand, 0.2)
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)