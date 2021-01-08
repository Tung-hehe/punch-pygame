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
    beaten = False
    # Is the player jumping?
    jumping = False
    # Is the player falling?
    falling = True
    # Which map is the player on?
    map = None
    # Frame for action run, stand, fall
    frame = 0
    # Frame for action attack
    attack_frame = 0
    # Frame for action jump
    jump_frame = 0
    # Frame for action beaten
    beaten_frame = 0
    # Check double-jump
    cout_jump = 0
    # Check combo of player
    cout_attack = 0
    # HP of player
    max_HP = setting.PLAYER_MAX_HEALTH
    current_HP = setting.PLAYER_MAX_HEALTH
    damage = 20

    def __init__(self):
        """ Constructor function"""
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        """ Load all image of the player"""
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
        # Load all the attack images
        self.normal_attack_r = [sprites.load_sprite('image/Player/attack/normal_attack_1/', 4),
                        sprites.load_sprite('image/Player/attack/normal_attack_2/', 4),
                        sprites.load_sprite('image/Player/attack/normal_attack_3/', 7)]
        self.normal_attack_l = [sprites.hori_flip_sprite('image/Player/attack/normal_attack_1/', 4),
                        sprites.hori_flip_sprite('image/Player/attack/normal_attack_2/', 4),
                        sprites.hori_flip_sprite('image/Player/attack/normal_attack_3/', 7)]
        self.beaten_r = sprites.load_sprite('image/Player/beaten/', 5)
        self.beaten_l = sprites.hori_flip_sprite('image/Player/beaten/', 5)
        self.true_attack = [self.normal_attack_l[0][1], self.normal_attack_r[0][1],
                            self.normal_attack_l[1][1], self.normal_attack_r[1][1],
                            self.normal_attack_l[2][2], self.normal_attack_r[2][2]]
        self.image = self.stand_r[0]
        # Get rectangle surrounding image, we will calculate its coordinates
        self.rect = self.image.get_rect()
        # Get size of image
        self.size = self.image.get_size()

    def update(self):
        """ This function used to update the player (coordinates, image). """
        # If the player is moving
        if self.moving:
            # Update coordinate
            if self.face_right:
                self.vel[0] += setting.PLAYER_VEL
            else:
                self.vel[0] -= setting.PLAYER_VEL

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
            # Update coordinate
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
            # Update coordinate, the player are affected by gravity
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
            if self.attack_frame >= len(self.normal_attack_r[self.cout_attack]):
                self.attacking = False
                self.attack_frame = 0
                self.cout_attack += 1
            if self.cout_attack >= len(self.normal_attack_r):
                self.cout_attack = 0
            if self.face_right:
                self.image = self.normal_attack_r[self.cout_attack][int(self.attack_frame)]
            else:
                self.image = self.normal_attack_l[self.cout_attack][int(self.attack_frame)]
        if self.beaten:
            self.vel[0] = 0
            self.beaten_frame += setting.SPEED_ATTACK
            if self.beaten_frame >= len(self.beaten_r):
                self.beaten = False
                self.beaten_frame = 0
                self.start_timer = pygame.time.get_ticks()
            if self.face_right:
                self.image = self.beaten_r[int(self.beaten_frame)]
            else:
                self.image = self.beaten_l[int(self.beaten_frame)]

        # Limit of coordinate, velocity
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

        # ----------------Move player----------------
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
                self.vel[1] = 0
            self.cout_jump = 0
        if len(hits_list) == 0:
            self.falling = True

        # Get size, mask of image
        self.size = self.image.get_size()

    def draw(self, screen):
        """ This function is used to draw player"""
        screen.blit(self.image,
                    (self.rect.x - (self.size[0] - self.rect.w)/2,
                     self.rect.y - (self.size[1] - self.rect.h)))
        """ Why do we have to draw on the screen at this coordinate?
            Because the images in different actions are of different sizes.
            And we need the player in the middle. """

        """ Draw health bar of the player"""
        if self.current_HP > 60:
            col = setting.GREEN
        elif self.current_HP > 30:
            col = setting.YELLOW
        else:
            col = setting.RED
        width = int(self.rect.width * self.current_HP / self.max_HP) * 10
        font = pygame.font.SysFont(None, 20)
        text = str(int(self.current_HP)) + "/" + str(self.max_HP)
        Text = font.render(text, True, setting.WHITE, None)
        TextRect = Text.get_rect()
        TextRect.center = (200, 15)
        if self.current_HP > 0:
            pygame.draw.rect(screen, col, (0, 0, width, 30))
            screen.blit(Text, TextRect)
