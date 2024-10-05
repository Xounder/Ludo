import pygame, sys

import resource.settings as config
from services.game_controller import GameController
from services.start_game import StartGame
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

class Game:
    def __init__(self) -> None:
        """
        Initializes the game, setting up the display, clock, 
        sound manager, game controller, and start game interface.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('L U D O')
        self.clock = pygame.time.Clock()

        SoundManager.initialize()

        self.game_controller = GameController()
        self.start_game = StartGame()

        UpdaterManager.set_exclusive_update(self.start_game, self.game_start)
        
        self.game_controller.draw_map()

    def game_start(self) -> None:
        """
        Starts the game using the selected player settings from StartGame.
        """
        self.game_controller.start_game(self.start_game.selectors)
    
    def run(self) -> None:
        """
        Main loop of the game that handles events, updates, 
        and rendering of the game components.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            if self.start_game.active:
                self.start_game.draw()
            else:
                UpdaterManager.set_exclusive_update(self.game_controller, self.start_game.initialize)

            if self.game_controller.active:
                self.game_controller.draw()
            else:
                UpdaterManager.set_exclusive_update(self.start_game, self.game_start)
                
            UpdaterManager.update()

            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()
