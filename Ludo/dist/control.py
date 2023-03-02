from dice import Dice
from settings import *
from player import Player
import pygame
from timer import Timer

class Control:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.dice = Dice()
        self.waiting = True
        self.win = True
        self.winner = 0
        self.atual_player = 0 
        self.run_game = False
        # images
        winner_surf = pygame.image.load(f'img/win.png').convert()
        self.winner_surf = pygame.transform.scale(winner_surf, (winner_surf.get_width()*2, winner_surf.get_height()*2))
        self.winner_rect = self.winner_surf.get_rect(center= (screen_width/2, screen_height/2))
        self.winner_piece = None
        self.winner_piece_rect = None
        # timer
        self.winner_show_timer = Timer(1)
    
    def choose_players(self, color_list):
        self.players = [Player(color_list[i]) for i in range(len(color_list))]

    def draw(self):
        atual_player = self.players[self.atual_player]
        self.dice.draw(players_color[atual_player.player_id], self.waiting)
        self.draw_players()
        if self.win:
            if self.winner_show_timer.run:
                self.display_surface.blit(self.winner_surf, self.winner_rect)
                self.display_surface.blit(self.winner_piece, self.winner_piece_rect)
            else:
                self.run_game = False
    
    def draw_players(self):
        for i, plys in enumerate(self.players):
            if i == self.atual_player:
                continue
            plys.draw()
        self.players[self.atual_player].draw()

    def active_game(self, players_list):
        self.choose_players(players_list)
        self.win = False
        self.run_game = True

    def update(self):
        if self.winner_show_timer.run:
            self.winner_show_timer.update()

        if not self.win:
            if self.waiting:
                response = self.dice.update()
                if response:
                    self.waiting = False   
            else:
                atual_player = self.players[self.atual_player]
                if atual_player.update(self.dice.choosed, self.players, self.atual_player):
                    if self.dice.choosed != 6 and not atual_player.roll_again:
                        if self.atual_player < len(self.players) - 1:
                            self.atual_player += 1 
                        else:
                            self.atual_player = 0
                    atual_player.roll_again = False
                    self.waiting = True
            self.check_win()

    def check_win(self):
        for i, player in enumerate(self.players):
            if player.freedom.count(True) == 4:
                self.winner = i
                self.win = True
                winner_piece = self.players[i].piece_surf[0]
                self.winner_piece = pygame.transform.scale(winner_piece, (winner_piece.get_width()*1.5, winner_piece.get_height()*1.5))
                self.winner_piece_rect = self.winner_piece.get_rect(center= (screen_width/2, screen_height/2))
                self.winner_show_timer.active()