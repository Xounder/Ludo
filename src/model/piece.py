import pygame

import resource.settings as config
from model.map import Map
from model.dice import Dice
from managers.updater_manager import UpdaterManager
from managers.sound_manager import SoundManager

import time

class Piece:
    def __init__(self, id:int, color:str, lobby_pos:list) -> None:
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
        self.image = pygame.image.load(f'img/{self.color}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.to_tile(self.lobby_pos))
        UpdaterManager.add_to_animate(self.timer_name, 2)

    def get_atual_pos(self, step=-1) -> list:
        step = step if step != -1 else self.steps
        if step <= config.PIECE_STEPS_GOAL:
            if not self.is_lobby: 
                return config.map_steps[self.atual_cell] 
            else: 
                return self.lobby_pos
        else:
            return config.map_goal_steps[self.color][self.atual_cell]
    
    def is_playable(self, dice:Dice) -> bool:
        if self.goal_achieved: return False
        if self.steps + dice.value <= config.MAX_PIECE_STEPS:
            if self.is_lobby:
                return dice.is_max_value()
            return True
        return False

    def update_rect(self):
        if self.steps <= self.PIECE_STEPS_GOAL: 
            to_tile_list = config.map_steps[self.atual_cell] 
        else: 
            to_tile_list = config.map_goal_steps[self.color][self.atual_cell]
        self.rect.topleft = self.to_tile(to_tile_list)
        
    def to_tile(self, to_tile_list:list):
        gap_center = 8
        return list(map(lambda x: x * config.TILE_SIZE + gap_center, to_tile_list))

    def move_to_lobby(self) -> None:
        Map.add_redraw_map(self.get_atual_pos())
        self.rect.topleft = self.to_tile(self.lobby_pos)
        self.atual_cell = self.first_cell
        self.steps = 0
        self.is_lobby = True

    def leave_lobby(self) -> None:
        Map.add_redraw_map(self.lobby_pos)
        self.rect.topleft = self.to_tile(config.map_steps[self.first_cell])
        self.steps = 1
        self.is_lobby = False

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    def reset(self) -> None:
        self.moved = False

    def animate(self) -> None:
        if self.steps < self.max_steps:
            self.steps += 1
            self.move()
            SoundManager.play_sound('movement')
            time.sleep(0.01)
        else:
            UpdaterManager.finish_animation(self.timer_name)

    def move(self) -> bool:
        Map.add_redraw_map(self.get_atual_pos(self.steps - 1))
        self.change_atual_cell()
        self.update_rect()
        self.check_goal()
    
    def can_move(self) -> None:
        if self.steps >= self.PIECE_STEPS_GOAL:
            if self.steps + self.moves > config.MAX_PIECE_STEPS:
                return False
        return True     
    
    def to_animate_move(self, moves:int):
        self.moves = moves
        if self.can_move():
            self.max_steps = self.steps + moves 
            self.moved = True
            UpdaterManager.call_to_animate(self.timer_name, self.animate, callback=self.reset)
            return True
        return False
                   
    def change_atual_cell(self) -> None:
        self.atual_cell += 1
        if self.steps >= config.MAX_STEPS_MAP:
            self.atual_cell = self.steps - config.MAX_STEPS_MAP
        else:
            if self.atual_cell >= config.MAX_STEPS_MAP:
                self.atual_cell = self.atual_cell - config.MAX_STEPS_MAP
    
    def check_goal(self) -> None:
        if self.steps == config.MAX_PIECE_STEPS:
            self.goal_achieved = True 
            SoundManager.play_sound('goal_achieved')     

    def is_collide(self, mouse_pos:list, dice_value:int) -> bool:
        if self.rect.collidepoint(mouse_pos):
            if not self.is_lobby:
                return self.to_animate_move(dice_value)
            else:
                self.leave_lobby()
                return True
        return False
    