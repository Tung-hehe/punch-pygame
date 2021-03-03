import pygame
import setting
import sprites

class Monster(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a kind of monster.
        Create a child class for each kind of monster."""

    # What direction is the monster facing?
    face_right = False
    # Is monster attacking?
    attacking = False
    # If monster is beaten.
    beaten = False
    # Velcity of monster
    vel = 0
    # Frame for all actions
    stand_frame = 0
    run_frame = 0
    attack_frame = 0
    beaten_frame = 0
    death_frame = 0
    # Image for monster
    image = None
    rect = None
    size = (0,0)
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
    max_HP = 0
    current_HP = 0
    damage = 30

    # Attack timer
    start_timer = 0
    # True attack image
    true_attack = None

    def __init__(self, moving, speed):
        """ Constructor function"""
        pygame.sprite.Sprite.__init__(self)
        self.moving = moving
        self.speed = speed

    def idle(self):
        self.vel = 0
        self.stand_frame += setting.SPEED_STAND
        if self.face_right:
            self.image = self.stand_r[int(self.stand_frame) % len(self.stand_r)]
        else:
            self.image = self.stand_l[int(self.stand_frame) % len(self.stand_l)]

    def update(self, platforms):
        """ This function used to update the monster (cordinates, image). """

        # Monster move
        if self.moving:
            self.run_frame += setting.SPEED_RUN
            if self.face_right:
                self.vel = setting.MONSTER_VEL * self.speed
                self.image = self.run_r[int(self.run_frame)%len(self.run_r)]
            else:
                self.vel = -setting.MONSTER_VEL * self.speed
                self.image = self.run_l[int(self.run_frame) % len(self.run_l)]
        # Monster stand
        else:
            self.idle()
        # Monster attack
        if self.attacking:
            self.vel = 0
            if pygame.time.get_ticks() - self.start_timer > 500:
                self.attack_frame += setting.SPEED_ATTACK
                if self.attack_frame >= len(self.attack_r):
                    self.attacking = False
                    self.attack_frame = 0
                    self.start_timer = pygame.time.get_ticks()
                if self.face_right:
                    self.image = self.attack_r[int(self.attack_frame)]
                else:
                    self.image = self.attack_l[int(self.attack_frame)]
            else:
                self.idle()
        # Monster beaten
        if self.beaten:
            self.vel = 0
            self.beaten_frame += setting.SPEED_ATTACK
            if self.beaten_frame >= len(self.beaten_r):
                self.beaten = False
                self.beaten_frame = 0
                self.start_timer = pygame.time.get_ticks()
            if self.face_right:
                self.image = self.beaten_r[int(self.beaten_frame)]
            else:
                self.image = self.beaten_l[int(self.beaten_frame)]
        # Monster die
        if self.current_HP <= 0:
            self.vel = 0
            self.death_frame += setting.SPEED_ATTACK
            if self.death_frame >= len(self.death_r):
                self.death_frame = int(len(self.death_r)) - 1
                pygame.sprite.Sprite.kill(self)
            if self.face_right:
                self.image = self.death_r[int(self.death_frame)]
            else:
                self.image = self.death_l[int(self.death_frame)]

        # ----------------Move monster----------------
        # Move horizontally
        self.rect.x += self.vel
        hits_list = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits_list:
            if self.vel > 0:
                self.rect.right = hit.rect.left
                self.face_right = False
            if self.vel < 0:
                self.rect.left = hit.rect.right
                self.face_right = True
        if self.rect.x <= 0:
            self.face_right = True
        self.size = self.image.get_size()

    def draw(self, screen):
        """ This is a function used to draw monster. """
        screen.blit(self.image,
                    (self.rect.x - (self.size[0] - self.rect.w)/2,
                     self.rect.y - (self.size[1] - self.rect.h)))
        """ Why do we have to draw on the screen at this coordinate?
            Because the images in different actions are of different sizes.
            And we need the player in the middle. """

        """ Draw health bar of the monster"""
        if self.current_HP > 60:
            col = setting.GREEN
        elif self.current_HP > 30:
            col = setting.YELLOW
        else:
            col = setting.RED
        width = int(self.rect.width * self.current_HP / self.max_HP)
        if self.current_HP > 0:
            pygame.draw.rect(screen, col, (self.rect.left, self.rect.top - 12, width, 7))

class Wolf(Monster):
    """ Create Wolf"""
    def __init__(self,x, y):
        super().__init__(True, 3)
        """ Load all images of Wolf"""
        self.stand_r = sprites.load_sprite('image/Monster/Wolf/stand/', 4)
        self.stand_l = sprites.hori_flip_sprite('image/Monster/Wolf/stand/', 4)
        self.attack_r = sprites.load_sprite('image/Monster/Wolf/attack/', 7)
        self.attack_l = sprites.hori_flip_sprite('image/Monster/Wolf/attack/', 7)
        self.death_r = sprites.load_sprite('image/Monster/Wolf/death/', 9)
        self.death_l = sprites.hori_flip_sprite('image/Monster/Wolf/death/', 9)
        self.run_r = sprites.load_sprite('image/Monster/Wolf/run/', 6)
        self.run_l = sprites.hori_flip_sprite('image/Monster/Wolf/run/', 6)
        self.beaten_r = sprites.load_sprite('image/Monster/Wolf/beaten/1/', 3)
        self.beaten_l = sprites.hori_flip_sprite('image/Monster/Wolf/beaten/1/', 3)
        self.true_attack = [self.attack_r[4], self.attack_l[4]]

        # Get image
        self.image = self.stand_r[0]
        # Get rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.max_HP = 120
        self.current_HP = 100
        self.damage = 15

class Female_Zombie(Monster):
    """ Create female zombie"""
    def __init__(self, x, y):
        super().__init__(True, 1)
        """ Load all image of female zombie"""
        self.stand_r = sprites.load_sprite('image/Monster/Female_Zombie/stand/', 8)
        self.stand_l = sprites.hori_flip_sprite('image/Monster/Female_Zombie/stand/', 8)
        self.attack_r = sprites.load_sprite('image/Monster/Female_Zombie/attack/', 12)
        self.attack_l = sprites.hori_flip_sprite('image/Monster/Female_Zombie/attack/', 12)
        self.death_r = sprites.load_sprite('image/Monster/Female_Zombie/death/', 6)
        self.death_l = sprites.hori_flip_sprite('image/Monster/Female_Zombie/death/', 6)
        self.run_r = sprites.load_sprite('image/Monster/Female_Zombie/move/', 12)
        self.run_l = sprites.hori_flip_sprite('image/Monster/Female_Zombie/move/', 12)
        self.beaten_r = sprites.load_sprite('image/Monster/Female_Zombie/beaten/', 3)
        self.beaten_l = sprites.hori_flip_sprite('image/Monster/Female_Zombie/beaten/', 3)
        self.true_attack = [self.attack_r[7], self.attack_l[7]]
        # Get image
        self.image = self.stand_r[0]
        # Get rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.max_HP = 150
        self.current_HP = 100
        self.damage = 10

class Male_Zombie(Monster):
    """ Create female zombie"""
    def __init__(self, x, y):
        super().__init__(True, 1)
        """ Load all image of male zombie"""
        self.stand_r = sprites.load_sprite('image/Monster/Male_Zombie/stand/', 10)
        self.stand_l = sprites.hori_flip_sprite('image/Monster/Male_Zombie/stand/', 10)
        self.attack_r = sprites.load_sprite('image/Monster/Male_Zombie/attack/', 9)
        self.attack_l = sprites.hori_flip_sprite('image/Monster/Male_Zombie/attack/', 9)
        self.death_r = sprites.load_sprite('image/Monster/Male_Zombie/death/', 7)
        self.death_l = sprites.hori_flip_sprite('image/Monster/Male_Zombie/death/', 7)
        self.run_r = sprites.load_sprite('image/Monster/Male_Zombie/move/', 20)
        self.run_l = sprites.hori_flip_sprite('image/Monster/Male_Zombie/move/', 20)
        self.beaten_r = sprites.load_sprite('image/Monster/Male_Zombie/beaten/', 3)
        self.beaten_l = sprites.hori_flip_sprite('image/Monster/Male_Zombie/beaten/', 3)
        self.true_attack = [self.attack_r[4], self.attack_l[4]]
        # Get image
        self.image = self.stand_r[0]
        # Get rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.max_HP = 150
        self.current_HP = 100
        self.damage = 10