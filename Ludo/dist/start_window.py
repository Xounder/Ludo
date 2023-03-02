import pygame
from settings import *
from timer import Timer

class StartWindow:
    def __init__(self, active_game):
        self.display_surface = pygame.display.get_surface()
        self.active_game = active_game
        self.qnt_ply = 2
        self.colors = players_color
        self.ply_circ_color = [0, 1, 2, 3]
        self.first_win = True
        self.mouse_timer = Timer(0.4)
        # image
        self.start_surf = pygame.image.load(f'img/start_window.png').convert()
        self.start_rect = self.start_surf.get_rect(topleft = (0, 0))
        # rects contacts
        self.players_rect = [pygame.Surface((122, 88)) for i in range(3)]
        self.players_rect_pos = [[screen_width/2 - 202, screen_height/2 - 162], [screen_width/2 - 62, screen_height/2 - 162], [screen_width/2 + 80, screen_height/2 - 162]]
        self.players_rect_rect = [self.players_rect[i].get_rect(topleft= (self.players_rect_pos[i])) for i in range(3)]

        self.players_circ_pos =[[screen_width/2 - 168, screen_height/2 + 19], [screen_width/2 - 168, screen_height/2 + 44], 
                                [screen_width/2 - 168, screen_height/2 + 69], [screen_width/2 - 168, screen_height/2 + 94]]
        self.players_circ_surf = [pygame.Surface((10, 10)) for i in range(4)]
        self.players_circ_rect = [self.players_circ_surf[i].get_rect(center= self.players_circ_pos[i]) for i in range(4)]

        self.start_button = pygame.Surface((160, 55))
        self.start_button_rect = self.start_button.get_rect(center= (screen_width/2 - 15, screen_height - 58))

        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))

    def can_start_game(self):
        start_game = True
        playabe_chars = self.ply_circ_color[:self.qnt_ply]
        for i in range(self.qnt_ply):
            if playabe_chars.count(playabe_chars[i]) != 1:
                start_game = False
        return start_game

    def draw(self):
        self.display_surface.blit(self.start_surf, self.start_rect)
        # players_surf
        for i in range(3):
            color_rect = 'purple' if i == self.qnt_ply - 2 else 'black'
            pygame.draw.rect(self.display_surface, color_rect, [self.players_rect_pos[i][0] - 1, self.players_rect_pos[i][1], 122, 88], 3)
        # players_circ
        for i in range(self.qnt_ply):
            color = self.colors[self.ply_circ_color[i]]
            pygame.draw.circle(self.display_surface, color, self.players_circ_pos[i], 5)
        # start_button
        if self.can_start_game():
            pygame.draw.rect(self.display_surface, 'red', [self.start_button_rect[0] - 1, self.start_button_rect[1], 160, 55], 3)

    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.mouse_rect.colliderect(self.start_button_rect) and self.can_start_game():
                    self.active_game(self.ply_circ_color[:self.qnt_ply])
                else:
                    for i, player_rect in enumerate(self.players_rect_rect):
                        if self.mouse_rect.colliderect(player_rect):
                            self.qnt_ply = 2 + i
                            break
                    for i, ply_circ_rect in enumerate(self.players_circ_rect):
                        if self.mouse_rect.colliderect(ply_circ_rect) and i+1 <= self.qnt_ply:
                            if self.ply_circ_color[i] < len(self.colors) - 1:
                                self.ply_circ_color[i] += 1
                            else:
                                self.ply_circ_color[i] = 0
                            break
                self.mouse_timer.active()

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        self.input()
    