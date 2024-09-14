import pygame, sys

import resource.settings as config
from services.game_controller import GameController
from services.start_game import StartGame

from util.timer_management import TimerManagement
from services.updater import Updater

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('L U D O')
        self.clock = pygame.time.Clock()

        self.game_controller = GameController()
        self.start_game = StartGame()

        Updater.set_exclusive_update(self.start_game, self.game_start)
        
        self.game_controller.draw_map()
    
    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            Updater.update()
            if self.start_game.active:
                self.start_game.draw()
            else:
                Updater.set_exclusive_update(self.game_controller, self.start_game.init)

            if self.game_controller.active:
                self.game_controller.draw()
            else:
                Updater.set_exclusive_update(self.start_game, self.game_start)

            pygame.display.update()
            self.clock.tick(60)

    def game_start(self) -> None:
        self.game_controller.start_game(self.start_game.selectors)

game = Game()
game.run()
