import pygame

import resource.settings as config
from model.piece import Piece
from model.dice import Dice
from managers.input_manager import InputManager

class Player:
    def __init__(self, color:str) -> None:
        self.color = color
        self.pieces = [Piece(id=i, 
                             color=self.color, 
                             lobby_pos=config.lobby_pos[self.color][i]) 
                             for i in range(4)] 
        self.atual_piece = self.pieces[0]
        self.played = False
        self.check_auto = True

    def play_again(self) -> None:
        self.played = False
        self.check_auto = True

    def is_one_out(self) -> bool:
        for p in self.pieces:
            if not p.is_lobby: return True
        return False
    
    def is_only1_out(self) -> bool:
        return True if len([1 for p in self.pieces if not p.is_lobby]) == 1 else False

    def is_only1_piece_to_move(self, value:Dice) -> bool:
        p = [p.id for p in self.pieces 
                if not p.is_lobby and p.steps + value <= config.MAX_PIECE_STEPS or p.is_lobby and value == 6]
        if len(p) == 1:
            self.atual_piece = self.pieces[p[0]]
            return True
        return False
    
    def is_win(self) -> bool:
        return True if len([1 for p in self.pieces if p.goal_achieved]) == 4 else False
    
    def get_pieces_pos(self) -> list:
        return [self.pieces[i].get_atual_pos() for i in range(4)]
    
    def get_atual_piece_pos(self) -> list:
        return self.atual_piece.get_atual_pos()
    
    def get_piece_pos(self, piece:int) -> list:
        return self.pieces[piece].get_atual_pos()

    def draw(self) -> None:
        for p in self.pieces: p.draw()

    def update(self, dice:Dice) -> None:
        if dice.rolled and self.check_auto:
            if not self.can_play(dice): return
            self.check_auto = False
            self.played = self.is_auto_play(dice)
        self.input(dice)

    def input(self, dice:Dice) -> None:
        if InputManager.mouse_is_pressed():
            if dice.to_roll:
                dice.is_collide(InputManager.cursor)
            else:
                if not dice.rolled: return

                if not self.played:
                    for p in self.pieces:
                        if p.is_collide(InputManager.cursor, dice.value):
                            self.atual_piece = p
                            self.played = True
                            break
                
    def can_play(self, dice:Dice):
        for p in self.pieces:
            if p.is_playable(dice):
                self.played = False
                return True
        self.played = True
        return False

    def is_auto_play(self, dice:Dice) -> bool:
        if dice.is_max_value(): return False
        
        if self.is_only1_out() or self.is_only1_piece_to_move(dice.value): # somente uma peça fora do lobby
            return self.atual_piece.to_animate_move(dice.value)                
    