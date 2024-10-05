import pygame
import random
import time

import resource.settings as config
from model.map import Map
from model.human_player import HumanPlayer
from model.ai_player import AIPlayer
from model.dice import Dice
from util.painter import Painter
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

class GameController:
    """
    Controls the game flow, player actions, and game state.
    """

    def __init__(self) -> None:
        """
        Initializes the GameController, the map, and the dice.
        """
        self.screen = pygame.display.get_surface()
        self.map = Map()
        self.dice = Dice()
        self.active = False   
        self.timer_name = 'end-game_timer'
        UpdaterManager.add_to_animate(self.timer_name, 2.5)     

    def draw_map(self) -> None:
        """
        Draws the game map on the screen.
        """
        self.map.draw_map()

    def start_game(self, players:dict) -> None:
        """
        Starts the game with the given players.

        Args:
            players (dict): A dictionary containing player information.
        """
        self.active_end_game_music = True
        self.checked_goal_achieved = False
        self.players = []
        for ply in players:
            if ply['player'] == config.INACTIVE: continue

            if ply['player'] == config.PLAYER:
                p = HumanPlayer(config.colors[ply['color']]) 
            if ply['player'] == config.AI:
                p = AIPlayer(config.colors[ply['color']]) 

            self.players.append(p)

        self.ply_id = 0
        self.atual_ply = self.players[self.ply_id]
        self.draw_map()
        self.active = True

    def next_ply(self) -> None:
        """
        Moves to the next player in turn.
        """
        self.ply_id = (self.ply_id + 1) % len(self.players)
        self.atual_ply = self.players[self.ply_id]
        self.checked_goal_achieved = False
        self.play_again()

    # DRAW
    def draw_ply_indicator(self) -> None:
        """
        Draws the current player's indicator on the screen.
        """
        if not self.dice.rolled:
            self.draw_dice_to_roll()
        else:
            self.draw_atual_ply_color()

    def draw_dice_to_roll(self) -> None:
        """
        Draws the dice area to roll for the current player.
        """
        rect_tl = self.dice.rect.topleft
        pygame.draw.rect(self.screen, self.atual_ply.color, (rect_tl[0], rect_tl[1], config.TILE_SIZE, config.TILE_SIZE), 4)
        pygame.draw.rect(self.screen, 'black', (rect_tl[0], rect_tl[1], config.TILE_SIZE, config.TILE_SIZE), 1)

    def draw_atual_ply_color(self) -> None:
        """
        Draws the current player's color on the dice.
        """
        rect_c = self.dice.rect.center
        pygame.draw.rect(self.screen, self.atual_ply.color, (rect_c[0] + 8, rect_c[1] + 8, 8, 8), 0)
        pygame.draw.rect(self.screen, 'black', (rect_c[0] + 8, rect_c[1] + 8, 8, 8), 1)

    def draw_ply_piece(self) -> None:
        """
        Draws the current player's pieces on the board if playable.
        """
        if not self.dice.rolled: return
        if self.atual_ply.atual_piece.moved: return
        for p in self.atual_ply.pieces:
            if not p.is_playable(self.dice): continue  
            pos = p.rect.center
            pygame.draw.circle(self.screen, 'black', (pos[0] + 1, pos[1] + 1), 5, 0)

    def draw_end_game(self, color:str) -> None:
        """
        Draws the end game screen with the winner's information.

        Args:
            color (str): The color of the winning player.
        """
        size = (300, 150)
        pos = (config.SCREEN_WIDTH/2 - size[0]/2, config.SCREEN_HEIGHT/2 - size[1]/2)
        Painter.draw_rect(screen=self.screen, 
                          size=size, 
                          pos=pos,
                          d=5,
                          f_color=color,
                          b_color='gray')
        
        pos = (config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2)
        Painter.blit_text_shadow(screen=self.screen,
                                 text=f'PLAYER{self.ply_id+1}', 
                                 color=self.atual_ply.color, 
                                 pos=(pos[0], pos[1]-20), 
                                 back_color='black', 
                                 center=True,
                                 font_size=42)
        
        Painter.blit_text_shadow(screen=self.screen,
                                 text=f'WIN!', 
                                 color='red', 
                                 pos=(pos[0], pos[1] + 20), 
                                 back_color='black', 
                                 center=True,
                                 font_size=42)
        
    def draw(self) -> None:
        """
        Draws all game elements on the screen.
        """
        self.map.draw()
        self.dice.draw()
        self.draw_ply_indicator()
        for i in range(len(self.players)):
            if self.ply_id == i: continue
            self.players[i].draw()
        self.atual_ply.draw()
        self.draw_ply_piece()

    # UPDATE
    def update(self) -> None:
        """
        Updates the game state based on the current player's actions.
        """
        if not self.atual_ply.played:
            self.atual_ply.update(self.dice)
        else:
            if not self.is_end_game():
                if self.is_end_turn():
                    self.next_ply()

    def play_again(self) -> None:
        """
        Resets the current player's state and the dice for a new turn.
        """
        self.atual_ply.play_again()
        self.dice.reset()

    def animate(self) -> None:
        """
        Animates the end game sequence.
        """
        if self.active_end_game_music:
            self.active_end_game_music = False
            SoundManager.play_sound('won')
        self.draw_end_game(random.choice(config.colors))
        time.sleep(0.3)

    def callback(self) -> None:
        """
        Callback function called after the end game animation.
        """
        self.draw_map()
        self.active = False
        self.active_end_game_music = True

    def is_end_game(self) -> bool:
        """
        Checks if the current player has won the game.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        if self.atual_ply.is_win():
            UpdaterManager.call_to_animate(self.timer_name, self.animate, self.callback)
            return True
        return False
    
    def is_end_turn(self) -> bool:
        """
        Checks if the current turn has ended based on the dice value.

        Returns:
            bool: True if the turn continues, False otherwise.
        """
        if self.dice.is_max_value():
            self.is_eliminate_piece()
            self.play_again()
            return False
        elif self.atual_ply.atual_piece.goal_achieved and not self.checked_goal_achieved:
            self.checked_goal_achieved = True
            self.play_again()
            return False
        else:
            if self.is_eliminate_piece():
                self.play_again()
                return False
        return True
        
    def is_eliminate_piece(self) -> bool:
        """
        Checks if the current player's piece has been eliminated by another player.

        Returns:
            bool: True if a piece has been eliminated, False otherwise.
        """
        # células neutras
        if config.star_cells.count(self.atual_ply.get_atual_piece_pos()): return False
        if config.map_fcell_colors.count(self.atual_ply.get_atual_piece_pos()): return False

        again = False
        for i, ply in enumerate(self.players):
            if self.ply_id == i: continue
            for p in ply.pieces:
                if p.get_atual_pos() == self.atual_ply.get_atual_piece_pos():
                    p.move_to_lobby()
                    again = True
                    SoundManager.play_sound('eliminate')
        return again
