import pygame
from setting import *
from sprites import *
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PUNCH!!!!!')
clock = pygame.time.Clock()
def load_map(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    map = []
    for tile in data:
        map.append(list(tile))
    return map
skeleton_map = load_map('image/Map_2/map.txt')
map = pygame.image.load('image/Map_2/front_map.png')
background = pygame.image.load('image/Map_2/background.png')
map_length = TILE_SIZE * len(skeleton_map[0])
map_check = 0
camera = 0
player = Player()
monster = Monster(1020, 257)
platforms = pygame.sprite.Group()
platform = Platform()
for x in range(len(skeleton_map)):
    for y in range(len(skeleton_map[0])):
        if skeleton_map[x][y] != '0':
            platform = Platform(y*TILE_SIZE, x*TILE_SIZE)
            platforms.add(platform)
running = True
while running:
    screen.blit(background, (0, 0))
    clock.tick(FPS)
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
                if player.cout_jump < 1:
                    player.jumping = True
                    player.cout_jump += 1
            if event.key == pygame.K_j:
                if player.type_attack != player.punch:
                    player.type_attack = player.punch
                    player.cout_attack = 0
                if not player.attacking:
                    player.attacking = True
            if event.key == pygame.K_k:
                if player.type_attack != player.kick:
                    player.type_attack = player.kick
                    player.cout_attack = 0
                if not player.attacking:
                    player.attacking = True
            if event.key == pygame.K_l:
                if player.type_attack != player.block:
                    player.type_attack = player.block
                    player.cout_attack = 0
                if not player.attacking:
                    player.attacking = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving = False
            if event.key == pygame.K_d:
                player.moving = False
    map_check += player.vel.x
    if map_check <= 0:
        map_check = 0
    if map_check >= WIDTH / 2 and map_check <= map_length - WIDTH / 2:
        camera -= player.vel.x
        screen.blit(map, (camera, 0))
        monster.rect.x -= player.vel.x
        for platform in platforms:
            platform.rect.x -= player.vel.x
        hits_list = pygame.sprite.spritecollide(player, platforms, False)
        for hit in hits_list:
            if player.vel.x > 0:
                player.rect.right = hit.rect.left
            if player.vel.x < 0:
                player.rect.left = hit.rect.right
        if len(hits_list) > 0:
            player.vel.x = 0
    else:
        player.move_x(platforms)
        screen.blit(map, (camera, 0))
    player.move_y(platforms)
    player.update()
    monster.update()
    screen.blit(monster.image,
                (monster.rect.x - (monster.size[0] - monster.rect.w) / 2,
                 monster.rect.y - (monster.size[1] - monster.rect.h)))
    screen.blit(player.image,
                (player.rect.x - (player.size[0] - player.rect.w)/2,
                 player.rect.y - (player.size[1] - player.rect.h)))
    pygame.display.flip()
pygame.quit()