import pygame
from random import randint

import resource.settings as config
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

class Dice:
    """
    Represents a dice that can be rolled and displayed on the screen.
    """

    def __init__(self) -> None:
        """
        Initializes the Dice instance and loads dice images.
        """
        self.screen = pygame.display.get_surface()
        self.MAX_VALUE = config.MAX_DICE_VALUE
        self.value = self.MAX_VALUE
        self.to_roll = True
        self.rolled = False
        self.atual_frame = 0
        self.timer_name = 'dice_timer'
        self.assets()

    def assets(self) -> None:
        """
        Loads dice images and initializes the dice's display properties.
        """
        self.dices_surf = [pygame.image.load(f'img/dice/dice{i+1}.png').convert_alpha() for i in range(6)]
        self.image = self.dices_surf[self.value-1]
        self.rect = self.image.get_rect(center=(config.SCREEN_WIDTH/2 + 1, config.SCREEN_HEIGHT/2 + 1))
        UpdaterManager.add_to_animate(self.timer_name, 0.4)

    def is_max_value(self) -> bool:
        """
        Checks if the current dice value is the maximum.

        Returns:
            bool: True if the dice value is the maximum, False otherwise.
        """
        return True if self.value == self.MAX_VALUE else False

    def roll(self) -> None:
        """
        Rolls the dice and updates its value and displayed image.
        """
        self.value = randint(1, self.MAX_VALUE)
        self.image = self.dices_surf[self.value-1]

    def reset(self) -> None:
        """
        Resets the dice state for a new roll.
        """
        self.to_roll = True
        self.rolled = False

    def draw(self) -> None:
        """
        Draws the current dice image on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def callback(self) -> None:
        """
        Callback function to be called after rolling the dice.
        """
        self.rolled = True
        self.roll()

    def animate(self) -> None:
        """
        Animates the dice display by cycling through the dice images.
        """
        self.atual_frame += 0.15
        if self.atual_frame > len(self.dices_surf)-1:
            self.atual_frame = 0
        self.image = self.dices_surf[int(self.atual_frame)]
        
    def is_collide(self, mouse_pos:list) -> bool:
        """
        Checks if the dice was clicked and initiates the rolling animation.

        Args:
            mouse_pos (list): The position of the mouse click.

        Returns:
            bool: True if the dice was clicked, False otherwise.
        """
        if self.rect.collidepoint(mouse_pos):
            SoundManager.play_sound('dice_rolling')
            UpdaterManager.call_to_animate(self.timer_name, self.animate, self.callback)
            self.to_roll = False    
            return True
        return False
