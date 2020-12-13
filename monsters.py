# import pygame
# from setting import *
# from sprites import *
# vec = pygame.math.Vector2
# class Monster(pygame.sprite.Sprite):
#     def __init__(self, x = 0, y = 0, type = "Wolf"):
#         pygame.sprite.Sprite.__init__(self)
#         self.type = type
#         self.load_image()
#         self.image = self.stand[0]
#         self.mask = pygame.mask.from_surface(self.image)
#         self.face_right = False
#         self.attacking = False
#         self.moving = False
#         self.rect = self.image.get_rect()
#         self.size = self.image.get_size()
#         self.normal_frame = 0
#         self.attack_frame = 0
#         self.pause_attack = 0
#         self.rect.x = x
#         self.rect.y = y
#         self.vel = vec(0, 0)
#     def load_image(self):
#         self.stand = load_sprite('image/Monster/' + self.type +'/stand/', 4)
#         self.attack = load_sprite('image/Monster/Wolf/attack/', 7)
#         self.dead = load_sprite('image/Monster/Wolf/dead/', 9)
#     def animate(self, action, speed):
#         self.normal_frame += speed
#         if self.face_right:
#             self.image = action[int(self.normal_frame) % len(action)]
#         else:
#             self.image = pygame.transform.flip(action[int(self.normal_frame) % len(action)], True, False)
#     def update(self):
#         if self.attacking:
#             self.vel.x = 0
#             self.attack_frame += SPEED_ATTACK
#             if self.attack_frame >= len(self.attack):
#                 self.attacking = False
#                 self.pause_attack = pygame.time.get_ticks()
#                 self.attack_frame = 0
#             if self.face_right:
#                 self.image = self.attack[int(self.attack_frame)]
#             else:
#                 self.image = pygame.transform.flip(self.attack[int(self.attack_frame)], True, False)
#         else:
#             self.animate(self.stand, 0.2)
#         self.size = self.image.get_size()
#         self.mask = pygame.mask.from_surface(self.image)
pass