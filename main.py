import pygame
from setting import *
from sprites import *
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My_game')
clock = pygame.time.Clock()
background = pygame.image.load('image/Map_2/BG.png').convert()
map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','1','2','3','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','1','2','8','5','6','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','1','2','8','5','5','5','6','0','0','0','0','1','2','3'],
       ['1','2','2','2','3','0','4','5','5','5','5','5','10','2','2','2','2','8','5','6'],
       ['4','5','5','5','6','0','4','5','5','5','5','5','5','5','5','5','5','5','5','6']]
map_width = len(map[0])*TILE_SIZE
map_height = len(map)*TILE_SIZE
map_check_x = 0
map_check_y = 0
all_sprites = pygame.sprite.Group()
player = Player()
platforms = pygame.sprite.Group()
platform = Platform()
for x in range(len(map)):
    for y in range(len(map[0])):
        if map[x][y] != '0':
            platform = Platform(y*TILE_SIZE, x*TILE_SIZE, map[x][y])
            platforms.add(platform)
all_sprites.add(platforms)
all_sprites.add(player)
running = True
def move_player(player, tiles):
    player.rect.x += player.vel.x
    hits_list = pygame.sprite.spritecollide(player, tiles, False)
    for hit in hits_list:
        if player.vel.x > 0:
            player.rect.right = hit.rect.left
        if player.vel.x < 0:
            player.rect.left = hit.rect.right
    player.rect.y += player.vel.y
    hits_list = pygame.sprite.spritecollide(player, tiles, False)
    for hit in hits_list:
        if player.vel.y > 0:
            player.rect.bottom = hit.rect.top
        if player.vel.y < 0:
            player.rect.top = hit.rect.bottom
        player.cout_jump = 0
while running:
    clock.tick(FPS)
    screen.blit(background, (-360, -200))
    move_player(player, platforms)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving = True
                player.face_right = False
            if event.key == pygame.K_d:
                player.moving = True
                player.face_right = True
            if event.key == pygame.K_w:
                if player.cout_jump < 2:
                    player.vel.y = -8
                    player.cout_jump += 1
            if event.key == pygame.K_q:
                player.attack_q = True
            if event.key == pygame.K_e:
                player.attack_e = True
            if event.key == pygame.K_r:
                player.attack_r = True
            if event.key == pygame.K_f:
                player.attack_f = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving = False
            if event.key == pygame.K_d:
                player.moving = False
    map_check_x += player.vel.x
    map_check_y += player.vel.y
    all_sprites.update()
    platforms.draw(screen)
    screen.blit(player.image, (player.rect.x - (player.size[0] - player.rect.w)/2, player.rect.y - (player.size[1] - player.rect.h)))
    pygame.display.flip()
pygame.quit()