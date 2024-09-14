import pygame, sys

import resource.settings as config
from services.game_controller import GameController
from services.start_game import StartGame

from util.timer_management import TimerManagement

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('L U D O')
        self.clock = pygame.time.Clock()

        self.game_controller = GameController()
        self.start_game = StartGame()

        self.game_controller.draw_map()
    
    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            TimerManagement.update_timers()

            if self.start_game.active:
                self.start_game.update()
                self.start_game.draw()
            else:
                if self.start_game.active_game_controller:
                    self.game_controller.start_game(self.start_game.selectors)
                    self.start_game.active_game_controller = False

            if self.game_controller.run:
                self.game_controller.update()
                self.game_controller.draw()
            else:
                if not self.start_game.active_game_controller:
                    self.start_game.init()

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()