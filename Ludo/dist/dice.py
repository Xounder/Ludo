import pygame
from random import randint
from settings import screen_height, screen_width
from timer import Timer 

class Dice:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.choosed = randint(1, 6)
        self.dices_surf = [pygame.image.load(f'img/dice/dice{i+1}.png').convert_alpha() for i in range(6)]
        self.frame_choosed = self.dices_surf[self.choosed-1]
        self.dice_rect = self.frame_choosed.get_rect(center = (screen_width/2 + 1, screen_height/2 + 1))
        self.atual_frame = 0

        self.mouse_surf = pygame.Surface((5, 5))
        self.dice_used = False
        self.show_time = False

        self.dice_animate_timer = Timer(0.4)
        self.dice_show_timer = Timer(0.7)

        self.player_indicator = pygame.Surface((5, 5))
        ply_ind_pos = [self.dice_rect.bottomright[0] - 6, self.dice_rect.bottomright[1] - 6]
        self.player_indicator_rect = self.player_indicator.get_rect(topleft = (ply_ind_pos))
        
    def draw(self, color_ind, wait):
        if wait:
            self.display_surface.blit(self.frame_choosed, self.dice_rect)
        self.player_indicator.fill(color_ind)
        self.display_surface.blit(self.player_indicator, self.player_indicator_rect)

    def animate(self):
        self.atual_frame += 0.15
        if self.atual_frame > len(self.dices_surf)-1:
            self.atual_frame = 0
        self.frame_choosed = self.dices_surf[int(self.atual_frame)]

    def input(self):
        self.mouse_rect = self.mouse_surf.get_rect(center= (pygame.mouse.get_pos()))
        if pygame.mouse.get_pressed()[0] == True and self.dice_rect.colliderect(self.mouse_rect):
            self.choosed = randint(1, 6)
            self.dice_animate_timer.active()
            self.dice_used = True

    def update(self):
        if not self.dice_used:
            self.input()
        else:
            if self.dice_animate_timer.run:
                self.animate()
                self.dice_animate_timer.update()
            else:
                if not self.show_time:
                    self.frame_choosed = self.dices_surf[self.choosed-1]
                    self.dice_show_timer.active()
                    self.show_time = True
                else:
                    if self.dice_show_timer.run:
                        self.dice_show_timer.update()
                    else:
                        self.show_time = False
                        self.dice_used = False          
                        return True