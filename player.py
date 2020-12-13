import pygame
import setting
import sprites
class Player(pygame.sprite.Sprite):
    """ This class represents the player controls. """

    # Set velocity of player
    vel = [0,0]
    # What direction is the player facing?
    face_right = True
    # Is the player moving?
    moving = False
    # Is the player attacking?
    attacking = False
    # Is the player jumping?
    jumping = False
    # Is the player falling?
    falling = True
    # Which map is the phayer on?
    map = None
    # Frame for action run, stand
    frame = 0
    # Frame for action attack
    attack_frame = 0
    # Frame for action jump
    jump_frame = 0
    # Check double-jump
    cout_jump = 0
    # Check combo of player
    cout_attack = 0

    def __init__(self):
        """ Constructor function"""
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Load all image of the player
        self.load_image()
        self.image = self.stand_r[0]
        # Create mask for player, Useful for fast pixel perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)
        # Get rectangle surrounding image, we will calculate its coordinates
        self.rect = self.image.get_rect()
        # Get size of image
        self.size = self.image.get_size()
        # Attack type of the player
        self.type_attack = self.punch_r

    def load_image(self):
        """ This is a function used to load all the images of the player. """
        # Load all the standing images
        self.stand_r = sprites.load_sprite('image/Player/stand/', 6)
        self.stand_l = sprites.hori_flip_sprite('image/Player/stand/', 6)
        # Load all the running images
        self.run_r = sprites.load_sprite('image/Player/run/', 8)
        self.run_l = sprites.hori_flip_sprite('image/Player/run/', 8)
        # Load all the jumping images
        self.jump_r = [sprites.load_sprite('image/Player/jump1/', 1),
                     sprites.load_sprite('image/Player/jump2/', 5)]
        self.jump_l = [sprites.hori_flip_sprite('image/Player/jump1/', 1),
                     sprites.hori_flip_sprite('image/Player/jump2/', 5)]
        # Load all the falling images
        self.fall_r = [sprites.load_sprite('image/Player/fall1/', 3),
                     sprites.load_sprite('image/Player/fall2/', 3)]
        self.fall_l = [sprites.hori_flip_sprite('image/Player/fall1/', 3),
                     sprites.hori_flip_sprite('image/Player/fall2/', 3)]
        # Load all the punching images
        self.punch_l = [sprites.load_sprite('image/Player/attack/punch1/', 4),
                      sprites.load_sprite('image/Player/attack/punch2/', 4),
                      sprites.load_sprite('image/Player/attack/punch3/', 8)]
        self.punch_r = [sprites.hori_flip_sprite('image/Player/attack/punch1/', 4),
                      sprites.hori_flip_sprite('image/Player/attack/punch2/', 4),
                      sprites.hori_flip_sprite('image/Player/attack/punch3/', 8)]
        # Load all the kicking images
        self.kick_r = [sprites.load_sprite('image/Player/attack/kick1/', 7),
                     sprites.load_sprite('image/Player/attack/kick2/', 7)]
        self.kick_l = [sprites.hori_flip_sprite('image/Player/attack/kick1/', 7),
                     sprites.hori_flip_sprite('image/Player/attack/kick2/', 7)]
        # Load all the blockiong images
        self.block_r = [sprites.load_sprite('image/Player/block/', 7)]
        self.block_l = [sprites.hori_flip_sprite('image/Player/block/', 7)]

    def update(self):
        """ This function used to update the player (cordinates, image). """
        # If the player is moving
        if self.moving:
            # Update cordinate
            if self.face_right:
                self.vel[0] += setting.PLAYER_ACC
            else:
                self.vel[0] -= setting.PLAYER_ACC

            # If the player isn't jumping, falling => the player is running. Then load image for action run
            if not self.jumping and not self.falling:
                self.frame += setting.SPEED_RUN
                if self.face_right:
                    self.image = self.run_r[int(self.frame)%len(self.run_r)]
                else:
                    self.image = self.run_l[int(self.frame) % len(self.run_l)]

        # If the player isn't moving => the player is standing. Then load image for action stand
        else:
            self.frame += setting.SPEED_STAND
            if self.face_right:
                self.image = self.stand_r[int(self.frame) % len(self.stand_r)]
            else:
                self.image = self.stand_l[int(self.frame) % len(self.stand_l)]
            self.vel[0] = 0

        #If the player is jumping
        if self.jumping:
            # Update cordinate
            self.vel[0] = 0
            self.falling = False
            self.jump_frame += setting.SPEED_JUMP
            if self.jump_frame >= len(self.jump_r[self.cout_jump]):
                self.jumping = False
                self.jump_frame = 0
                self.falling = True
                self.vel[1] = -setting.PLAYER_MAX_Y
            # Load image for action jump
            if self.face_right:
                self.image = self.jump_r[self.cout_jump][int(self.jump_frame)]
            else:
                self.image = self.jump_l[self.cout_jump][int(self.jump_frame)]

        # If the player is falling
        if self.falling:
            # Update cordinate, the player are affected by gravity
            self.vel[1] += setting.GRAVITY

            # Load image for action fall
            self.frame += setting.SPEED_FALL
            if self.face_right:
                self.image = self.fall_r[self.cout_jump][int(self.frame) % len(self.fall_r[self.cout_jump])]
            else:
                self.image = self.fall_l[self.cout_jump][int(self.frame) % len(self.fall_l[self.cout_jump])]

        # If the player is attacking
        if self.attacking:
            self.vel[0] = 0
            self.attack_frame += setting.SPEED_ATTACK
            if self.attack_frame >= len(self.type_attack[self.cout_attack]):
                self.attacking = False
                self.attack_frame = 0
                self.cout_attack += 1
            if self.cout_attack >= len(self.type_attack):
                self.cout_attack = 0
            if self.face_right:
                self.image = self.type_attack[self.cout_attack][int(self.attack_frame)]
            else:
                self.image = self.type_attack[self.cout_attack][int(self.attack_frame)]

        # Limit of cordinate, velocity
        if self.vel[1] > setting.PLAYER_MAX_Y:
            self.vel[1] = setting.PLAYER_MAX_Y
        if self.vel[0] <= -setting.PLAYER_MAX_X:
            self.vel[0] = -setting.PLAYER_MAX_X
        if self.vel[0] >= setting.PLAYER_MAX_X:
            self.vel[0] = setting.PLAYER_MAX_X
        if self.rect[0] <= 0:
            self.rect[0] = 0
        if self.rect[0] >= setting.WIDTH - self.rect.width:
            self.rect[0] = setting.WIDTH - self.rect.width

        # -----Move player-----
        # Move horizontally
        self.rect.x += self.vel[0]
        hits_list = pygame.sprite.spritecollide(self, self.map.platform_list, False)
        for hit in hits_list:
            if self.vel[0] > 0:
                self.rect.right = hit.rect.left
            if self.vel[0] < 0:
                self.rect.left = hit.rect.right

        # Move vertically
        self.rect.y += self.vel[1]
        hits_list = pygame.sprite.spritecollide(self, self.map.platform_list, False)
        for hit in hits_list:
            if self.vel[1] > 0:
                self.rect.bottom = hit.rect.top
                self.falling = False
            if self.vel[1] < 0:
                self.rect.top = hit.rect.bottom
            self.cout_jump = 0
        if len(hits_list) == 0:
            self.falling = True

        # Get size, mask of image
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """ This function is used to draw player"""
        screen.blit(self.image,
                    (self.rect.x - (self.size[0] - self.rect.w)/2,
                     self.rect.y - (self.size[1] - self.rect.h)))
        """ Why do we have to draw on the screen at this coordinate?
            Because the images in different actions are of different sizes.
            And we need the player in the middle. """

