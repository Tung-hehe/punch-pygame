import pygame
import sys
import setting
from player import Player
import maps

class Game():
    """This class is used to create game object."""
    def __init__(self):

        """ Contructor function."""
        # Create a screen
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
        pygame.display.set_caption('PUNCH!!!!!')

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Create the player
        self.player = Player()
        self.player.rect.x = 0
        self.player.rect.y = 400

        # Create all the maps
        self.map_list = [maps.Map_02(self.player), maps.Map_01(self.player)]

        # Set the current map
        self.current_map_index = 0
        self.current_map = self.map_list[self.current_map_index]
        self.player.map = self.current_map

        # Loop until the user clicks the close button
        self.running = True
        self.waiting = True

    def show_start_screen(self):
        """ This function is used to show start screen."""
        while self.waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.waiting = False
            self.screen.fill(setting.BLACK)
            font = pygame.font.SysFont(None, 50)
            Text = font.render("Press any key to start!", True, setting.RED, None)
            TextRect = Text.get_rect()
            TextRect.center = (setting.WIDTH / 2, setting.HEIGHT / 2)
            self.screen.blit(Text, TextRect)
            pygame.display.flip()
    def game_over_screen(self):
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    game_over = False
            self.screen.fill(setting.BLACK)
            font = pygame.font.SysFont(None, 70)
            Text = font.render("GAME OVER!", True, setting.RED, None)
            TextRect = Text.get_rect()
            TextRect.center = (setting.WIDTH / 2, setting.HEIGHT / 2)
            self.screen.blit(Text, TextRect)
            pygame.display.flip()
    def run(self):
        """ This function is used to run game. """
        while self.running:
            self.clock.tick(setting.FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """ This function is used to get events for this game."""
        # Handing events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Moving left event
                if event.key == pygame.K_a:
                    self.player.moving = True
                    self.player.face_right = False
                # Moving right event
                if event.key == pygame.K_d:
                    self.player.moving = True
                    self.player.face_right = True
                # Jumping event
                if event.key == pygame.K_w:
                    if self.player.cout_jump < 1:
                        self.player.jumping = True
                        self.player.cout_jump += 1
                # Attacking event
                if event.key == pygame.K_j:
                    if not self.player.attacking:
                        self.player.attacking = True
                # Quit event
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.moving = False
                if event.key == pygame.K_d:
                    self.player.moving = False

    def update(self):
        """ This function is used to update all objects of this game."""
        # If the player near the right side, scroll the map left
        if self.player.rect.x >= setting.WIDTH * 1 / 2:
            if self.current_map.map_scroll > - self.current_map.map_limit + setting.WIDTH:
                diff = self.player.rect.x - setting.WIDTH * 1 / 2
                self.player.rect.x = setting.WIDTH * 1 / 2
                self.current_map.scroll_map(-diff)

        # If the player near the left side, scroll the map right
        if self.player.rect.x <= setting.WIDTH * 1 / 2 - 1:
            if self.current_map.map_scroll < 0:
                diff = self.player.rect.x - setting.WIDTH * 1 / 2 + 1
                self.current_map.scroll_map(-diff)
                self.player.rect.x = setting.WIDTH * 1 / 2 - 1
        # Next map
        if self.player.rect.left >= setting.WIDTH - self.player.rect.width:
            if self.current_map_index < len(self.map_list) - 1:
                if len(self.current_map.enemy_list) == 0:
                    self.current_map_index += 1
                    self.current_map = self.map_list[self.current_map_index]
                    self.player.map = self.current_map
                    self.player.rect.x = 0
                    self.player.rect.y = 0
        if self.player.current_HP <= 0:
            self.running = False

        # Update everything
        self.player.update()
        self.current_map.update()

    def draw(self):
        """ This function is used to draw all objects of this game. """
        # Draw everything
        self.current_map.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

def main():
    """ Main function."""
    while True:
        game = Game()
        game.show_start_screen()
        game.run()
        game.game_over_screen()

# Run function main.
if __name__ == "__main__":
    main()
