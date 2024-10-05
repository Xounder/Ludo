import pygame

import resource.settings as config
from model.map import Map
from model.dice import Dice
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

import time

class Piece:
    """
    Represents a game piece that can move on the board and interact with the game state.
    """
    def __init__(self, id:int, color:str, lobby_pos:list) -> None:
        """
        Initializes a Piece with specified ID, color, and lobby position.

        Args:
            id (int): The ID of the piece.
            color (str): The color of the piece.
            lobby_pos (list): The starting position in the lobby.
        """
        self.screen = pygame.display.get_surface()
        self.id = id
        self.color = color
        self.lobby_pos = lobby_pos
        self.first_cell = config.map_fcell[self.color]
        self.atual_cell = self.first_cell
        self.goal_achieved = False
        self.is_lobby = True
        self.steps = 0
        self.moves = 0
        self.max_steps = 0
        self.eliminate = False
        self.moved = False
        self.timer_name = 'piece_timer'
        self.PIECE_STEPS_GOAL = config.PIECE_STEPS_GOAL
        self.assets()
    
    def assets(self) -> None:
        """
        Loads the piece's image assets and sets up the animation timer.
        """
        self.image = pygame.image.load(f'img/{self.color}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.to_tile(self.lobby_pos))
        UpdaterManager.add_to_animate(self.timer_name, 2)

    def get_atual_pos(self, step:int=-1) -> list:
        """
        Gets the current position of the piece based on the number of steps taken.

        Args:
            step (int): The step count to consider for position. Defaults to the current steps.

        Returns:
            list: The current position of the piece.
        """
        step = step if step != -1 else self.steps
        if step <= config.PIECE_STEPS_GOAL:
            if not self.is_lobby: 
                return config.map_steps[self.atual_cell] 
            else: 
                return self.lobby_pos
        else:
            return config.map_goal_steps[self.color][self.atual_cell]
    
    def is_playable(self, dice:Dice) -> bool:
        """
        Checks if the piece can be moved based on the dice value.

        Args:
            dice (Dice): The dice rolled.

        Returns:
            bool: True if the piece can be moved, False otherwise.
        """
        if self.goal_achieved: return False
        if self.steps + dice.value <= config.MAX_PIECE_STEPS:
            if self.is_lobby:
                return dice.is_max_value()
            return True
        return False

    def update_rect(self) -> None:
        """
        Updates the rectangle representing the piece's position on the screen.
        """
        if self.steps <= self.PIECE_STEPS_GOAL: 
            to_tile_list = config.map_steps[self.atual_cell] 
        else: 
            to_tile_list = config.map_goal_steps[self.color][self.atual_cell]
        self.rect.topleft = self.to_tile(to_tile_list)
        
    def to_tile(self, to_tile_list:list) -> list:
        """
        Converts a position to tile coordinates.

        Args:
            to_tile_list (list): The position to convert.

        Returns:
            list: The tile coordinates.
        """
        gap_center = 8
        return list(map(lambda x: x * config.TILE_SIZE + gap_center, to_tile_list))

    def move_to_lobby(self) -> None:
        """
        Moves the piece back to the lobby position and resets its state.
        """
        Map.add_redraw_map(self.get_atual_pos())
        self.rect.topleft = self.to_tile(self.lobby_pos)
        self.atual_cell = self.first_cell
        self.steps = 0
        self.is_lobby = True

    def leave_lobby(self) -> None:
        """
        Moves the piece out of the lobby and sets its initial position on the board.
        """
        Map.add_redraw_map(self.lobby_pos)
        self.rect.topleft = self.to_tile(config.map_steps[self.first_cell])
        self.steps = 1
        self.is_lobby = False

    def draw(self) -> None:
        """
        Draws the piece on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def reset(self) -> None:
        """
        Resets the moved state of the piece.
        """
        self.moved = False

    def animate(self) -> None:
        """
        Animates the movement of the piece by incrementing its steps.
        """
        if self.steps < self.max_steps:
            self.steps += 1
            self.move()
            SoundManager.play_sound('movement')
            time.sleep(0.01)
        else:
            UpdaterManager.finish_animation(self.timer_name)

    def move(self) -> bool:
        """
        Updates the piece's position and checks for goal achievement.

        Returns:
            bool: True if the piece moved, False otherwise.
        """
        Map.add_redraw_map(self.get_atual_pos(self.steps - 1))
        self.change_atual_cell()
        self.update_rect()
        self.check_goal()
    
    def can_move(self) -> None:
        """
        Checks if the piece can move based on its current state and steps taken.
        """
        if self.steps >= self.PIECE_STEPS_GOAL:
            if self.steps + self.moves > config.MAX_PIECE_STEPS:
                return False
        return True     
    
    def to_animate_move(self, moves:int) -> bool:
        """
        Initiates the animation for moving the piece a specified number of steps.

        Args:
            moves (int): The number of moves to animate.

        Returns:
            bool: True if animation started, False otherwise.
        """
        self.moves = moves
        if self.can_move():
            self.max_steps = self.steps + moves 
            self.moved = True
            UpdaterManager.call_to_animate(self.timer_name, self.animate, callback=self.reset)
            return True
        return False
                   
    def change_atual_cell(self) -> None:
        """
        Updates the current cell of the piece based on the steps taken.
        """
        self.atual_cell += 1
        if self.steps >= config.MAX_STEPS_MAP:
            self.atual_cell = self.steps - config.MAX_STEPS_MAP
        else:
            if self.atual_cell >= config.MAX_STEPS_MAP:
                self.atual_cell = self.atual_cell - config.MAX_STEPS_MAP
    
    def check_goal(self) -> None:
        """
        Checks if the piece has reached its goal position and updates its state.
        """
        if self.steps == config.MAX_PIECE_STEPS:
            self.goal_achieved = True 
            SoundManager.play_sound('goal_achieved')     

    def is_collide(self, mouse_pos:list, dice_value:int) -> bool:
        """
        Checks if the piece was clicked and initiates movement or lobby exit.

        Args:
            mouse_pos (list): The position of the mouse click.
            dice_value (int): The value rolled on the dice.

        Returns:
            bool: True if the piece was interacted with, False otherwise.
        """
        if self.rect.collidepoint(mouse_pos):
            if not self.is_lobby:
                return self.to_animate_move(dice_value)
            else:
                self.leave_lobby()
                return True
        return False
    