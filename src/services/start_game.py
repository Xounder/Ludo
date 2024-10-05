import pygame

import resource.settings as config
from managers.input_manager import InputManager
from util.painter import ClickRect, Painter

class StartGame:
    """
    Controls the start game menu and player selections.
    """

    def __init__(self) -> None:
        """
        Initializes the start game menu.
        """
        self.screen = pygame.display.get_surface()
        self.size = (300, 260)
        self.pos = (config.SCREEN_WIDTH/2 - self.size[0]/2, config.SCREEN_HEIGHT/2 - self.size[1]/2)
        
        self.initialize()
        self.create_surf_inputs()

        self.painter = Painter()

    def initialize(self) -> None:
        """
        Sets up the initial state of players and selectors.
        """
        self.players = []
        self.active = True
        self.selectors = [
            {'color': 0, 'player': config.PLAYER},
            {'color': 1, 'player': config.PLAYER},
            {'color': 2, 'player': config.PLAYER},
            {'color': 3, 'player': config.PLAYER}
        ]

    def create_surf_inputs(self) -> None:
        """
        Creates surface inputs for start and player selection buttons.
        """
        # Start Button
        self.start_button = ClickRect(surf_size=(90, 60),
                                      rect_pos=(config.SCREEN_WIDTH/2 + 40, config.SCREEN_HEIGHT/2 - 15),
                                      d=3,
                                      topleft=True)
        # Color Selection Button
        self.color_selection = []
        # Player Selection Button
        self.player_selection = []
        pos = [40, 95]
        for i in range(4):
            # Color
            self.color_selection.append(ClickRect(surf_size=(20, 20), 
                                                  rect_pos=(self.pos[0] + pos[0], self.pos[1] + pos[1]),
                                                  r=10,
                                                  center=True))
            # Player
            self.player_selection.append(ClickRect(surf_size=(100, 30),
                                                   rect_pos=(self.pos[0] + pos[0] + 20, self.pos[1] + pos[1] - 15),
                                                   d=2,
                                                   topleft=True))
            pos[1] += 40

    def draw(self) -> None:
        """
        Draws the start game menu and buttons on the screen.
        """
        Painter.draw_rect(screen=self.screen, size=self.size, pos=self.pos, d=10)

        b_c = 'green' if self.is_start_game() else 'red'
        self.start_button.draw_animated_rect(self.screen, b_color=[b_c, 'gray'])
            
        for i in range(4):
            self.draw_selector(i)

        self.draw_texts()

    def draw_selector(self, id:int) -> None:
        """
        Draws the selector for a specific player based on their current state.
        
        Args:
            id (int): The index of the player selector to draw.
        """
        atual_sel = self.selectors[id]
        c = (['gray', 'gray'] if atual_sel['player'] == config.INACTIVE 
                             else ['black', config.colors[atual_sel['color']]])

        self.color_selection[id].draw_animated_circle(screen=self.screen, colors=c)
        self.player_selection[id].draw_animated_rect(screen=self.screen, f_color='black')

    def draw_texts(self) -> None:
        """
        Draws the game title and player status texts.
        """
        Painter.blit_text_shadow(screen=self.screen,
                                 text='L U D O', 
                                 color='red', 
                                 pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 85), 
                                 back_color='black', 
                                 center=True)

        Painter.blit_text_shadow(screen=self.screen,
                                 text='PLAY', 
                                 color='black', 
                                 pos=self.start_button.get_rect(center=True), 
                                 back_color='white', 
                                 center=True)
        
        for i, sel in enumerate(self.selectors):
            Painter.blit_text_shadow(screen=self.screen,
                                     text=config.player_status[sel['player']], 
                                     color=config.colors[sel['color']], 
                                     pos=self.player_selection[i].get_rect(center=True), 
                                     back_color='black', 
                                     center=True,
                                     font_size=26)
            
            pos = self.player_selection[i].get_rect(midright=True)
            Painter.blit_text_shadow(screen=self.screen,
                                     text=f'P{i+1}', 
                                     color=config.colors[sel['color']], 
                                     pos=(pos[0] + 10, pos[1]), 
                                     back_color='black', 
                                     center=True,
                                     font_size=24)

    def update(self) -> None:
        """
        Handles input updates for starting the game and changing selections.
        """
        if InputManager.mouse_is_pressed():
            if self.start_button.is_rect_collide_point(InputManager.cursor):
                self.active = not self.is_start_game()
            else:
                for i, b_color in enumerate(self.color_selection):
                    if self.selectors[i]['player'] == config.INACTIVE: continue
                    if b_color.is_rect_collide_point(InputManager.cursor):
                        self.selectors[i]['color'] = (self.selectors[i]['color'] + 1) % len(config.colors)
                        return

                for i, ply_sel in enumerate(self.player_selection):
                    if ply_sel.is_rect_collide_point(InputManager.cursor):
                        self.selectors[i]['player'] = (self.selectors[i]['player'] + 1) % 3
                        break
            
    def is_start_game(self) -> bool:
        """Checks if the conditions to start the game are met.
        
        Returns:
            bool: True if the game can start, False otherwise.
        """
        check_color = []
        check_player = []
        for sel in self.selectors:
            if sel['player'] == config.INACTIVE: continue
            if check_color and check_color.count(sel['color']): return False
            check_color.append(sel['color'])
            check_player.append(sel['player'])
        if len(check_color) >= 2 and check_player.count(config.PLAYER) >= 1: return True
        return False
