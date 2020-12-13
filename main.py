import pygame
import setting
from player import Player
import monsters
import maps

def main():
    """ Main Program """
    pygame.init()
    pygame.mixer.init()

    # Create a screen
    screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
    pygame.display.set_caption('PUNCH!!!!!')

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create the player
    player = Player()

    # Create all the maps
    map_list = []
    map_list.append(maps.Map_01(player))

    # Set the current map
    current_map_index = 0
    current_map = map_list[current_map_index]
    player.map = current_map

    # Loop until the user clicks the close button
    running = True

    # -----Main Program Loop-----
    while running:
        clock.tick(setting.FPS)
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
                    if player.type_attack not in [player.punch_r, player.punch_l]:
                        if player.face_right:
                            player.type_attack = player.punch_r
                        else:
                            player.type_attack = player.punch_l
                        player.cout_attack = 0
                    if not player.attacking:
                        player.attacking = True
                if event.key == pygame.K_k:
                    if player.type_attack not in [player.kick_r, player.kick_l]:
                        if player.face_right:
                            player.type_attack = player.kick_r
                        else:
                            player.type_attack = player.kick_l
                        player.cout_attack = 0
                    if not player.attacking:
                        player.attacking = True
                if event.key == pygame.K_l:
                    if player.type_attack not in [player.block_r, player_l]:
                        if player.face_right:
                            player.type_attack = player.block_r
                        else:
                            player.type_attack = player.block_l
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
        player.update()
        current_map.draw(screen)
        player.draw(screen)
        pygame.display.flip()

    # On exit
    pygame.quit()


if __name__ == "__main__":
    main()