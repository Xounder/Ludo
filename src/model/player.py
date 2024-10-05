import pygame

import resource.settings as config
from model.piece import Piece
from model.dice import Dice

class Player:
    """
    Represents a player in the game, managing pieces and their movements.
    """
    def __init__(self, color:str) -> None:
        """
        Initializes a Player with a specified color and their pieces.

        Args:
            color (str): The color of the player.
        """
        self.color = color
        self.pieces = [Piece(id=i, 
                             color=self.color, 
                             lobby_pos=config.lobby_pos[self.color][i]) 
                             for i in range(4)] 
        self.atual_piece = self.pieces[0]
        self.played = False
        self.check_auto = True

    def play_again(self) -> None:
        """
        Resets the player's state to allow for another turn.
        """
        self.played = False
        self.check_auto = True

    def is_one_out(self) -> bool:
        """
        Checks if at least one piece is out of the lobby.

        Returns:
            bool: True if at least one piece is out, False otherwise.
        """
        for p in self.pieces:
            if not p.is_lobby: return True
        return False
    
    def is_only1_out(self) -> bool:
        """
        Checks if only one piece is out of the lobby.

        Returns:
            bool: True if only one piece is out, False otherwise.
        """
        return True if len([1 for p in self.pieces if not p.is_lobby]) == 1 else False

    def is_only1_piece_to_move(self, value:Dice) -> bool:
        """
        Checks if there is only one piece that can be moved.

        Args:
            value (Dice): The value rolled on the dice.

        Returns:
            bool: True if only one piece can be moved, False otherwise.
        """
        p = [p.id for p in self.pieces if self.can_move_piece(p, value)]
        if len(p) == 1:
            self.atual_piece = self.pieces[p[0]]
            return True
        return False
    
    def can_move_piece(self, piece:Piece, value: Dice) -> bool:
        """
        Checks if a specific piece can be moved based on the dice value.

        Args:
            piece (Piece): The piece to check.
            value (Dice): The value rolled on the dice.

        Returns:
            bool: True if the piece can be moved, False otherwise.
        """
        if not piece.is_lobby:
            return piece.steps + value <= config.MAX_PIECE_STEPS
        return value == config.MAX_DICE_VALUE 
    
    def is_win(self) -> bool:
        """
        Checks if the player has achieved the goal with all pieces.

        Returns:
            bool: True if all pieces have achieved their goal, False otherwise.
        """
        return True if len([1 for p in self.pieces if p.goal_achieved]) == 4 else False
    
    def get_pieces_pos(self) -> list:
        """
        Gets the current positions of all pieces.

        Returns:
            list: A list of the current positions of the player's pieces.
        """
        return [self.pieces[i].get_atual_pos() for i in range(4)]
    
    def get_atual_piece_pos(self) -> list:
        """
        Gets the current position of the active piece.

        Returns:
            list: The current position of the active piece.
        """
        return self.atual_piece.get_atual_pos()
    
    def get_piece_pos(self, piece:int) -> list:
        """
        Gets the current position of a specified piece.

        Args:
            piece (int): The index of the piece.

        Returns:
            list: The current position of the specified piece.
        """
        return self.pieces[piece].get_atual_pos()

    def draw(self) -> None:
        """
        Draws all pieces of the player on the screen.
        """
        for p in self.pieces: p.draw()

    def update(self, dice:Dice) -> None:
        """
        Updates the player's state based on the rolled dice.

        Args:
            dice (Dice): The rolled dice value.
        """
        # cada classe que extende irá realizar a implementação
        pass
                
    def can_play(self, dice:Dice) -> bool:
        """
        Checks if the player can make a move based on the rolled dice.

        Args:
            dice (Dice): The rolled dice value.

        Returns:
            bool: True if the player can make a move, False otherwise.
        """
        for p in self.pieces:
            if p.is_playable(dice):
                self.played = False
                return True
        self.played = True
        return False