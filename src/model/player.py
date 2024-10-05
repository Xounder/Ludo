import pygame

import resource.settings as config
from model.piece import Piece
from model.dice import Dice

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
        p = [p.id for p in self.pieces if self.can_move_piece(p, value)]
        if len(p) == 1:
            self.atual_piece = self.pieces[p[0]]
            return True
        return False
    
    def can_move_piece(self, piece:Piece, value: Dice) -> bool:
        if not piece.is_lobby:
            return piece.steps + value <= config.MAX_PIECE_STEPS
        return value == config.MAX_DICE_VALUE 
    
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
        # cada classe que extende irá realizar a implementação
        pass
                
    def can_play(self, dice:Dice):
        for p in self.pieces:
            if p.is_playable(dice):
                self.played = False
                return True
        self.played = True
        return False