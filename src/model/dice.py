import pygame
from random import randint

import resource.settings as config
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

class Dice:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.MAX_VALUE = config.MAX_DICE_VALUE
        self.value = self.MAX_VALUE
        self.to_roll = True
        self.rolled = False
        self.atual_frame = 0
        self.timer_name = 'dice_timer'
        self.assets()

    def assets(self) -> None:
        self.dices_surf = [pygame.image.load(f'img/dice/dice{i+1}.png').convert_alpha() for i in range(6)]
        self.image = self.dices_surf[self.value-1]
        self.rect = self.image.get_rect(center=(config.SCREEN_WIDTH/2 + 1, config.SCREEN_HEIGHT/2 + 1))
        UpdaterManager.add_to_animate(self.timer_name, 0.4)

    def is_max_value(self) -> bool:
        return True if self.value == self.MAX_VALUE else False

    def roll(self) -> None:
        self.value = randint(1, self.MAX_VALUE)
        self.image = self.dices_surf[self.value-1]

    def reset(self) -> None:
        self.to_roll = True
        self.rolled = False

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    def callback(self) -> None:
        self.rolled = True
        self.roll()

    def animate(self) -> None:
        self.atual_frame += 0.15
        if self.atual_frame > len(self.dices_surf)-1:
            self.atual_frame = 0
        self.image = self.dices_surf[int(self.atual_frame)]
        
    def is_collide(self, mouse_pos:list) -> bool:
        if self.rect.collidepoint(mouse_pos):
            SoundManager.play_sound('dice_rolling')
            UpdaterManager.call_to_animate(self.timer_name, self.animate, self.callback)
            self.to_roll = False    
            return True
        return False
