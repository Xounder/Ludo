from managers.input_manager import InputManager
from model.dice import Dice
from model.player import Player

class HumanPlayer(Player):
    """
    Represents a human player in the game, handling user input for actions.
    """
    
    def __init__(self, color: str) -> None:
        """
        Initializes a HumanPlayer with the specified color.

        Args:
            color (str): The color of the player.
        """
        super().__init__(color)

    # Override
    def update(self, dice:Dice) -> None:
        """
        Updates the player's state based on the rolled dice and user input.

        Args:
            dice (Dice): The current dice object that tracks the rolled state.
        """
        if dice.rolled and self.check_auto:
            if not self.can_play(dice): return
            self.check_auto = False
            self.played = self.is_auto_play(dice)
        self.input(dice)

    def input(self, dice:Dice) -> None:
        """
        Handles user input for selecting pieces and rolling the dice.

        Args:
            dice (Dice): The current dice object used to check rolling conditions.
        """
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

    def is_auto_play(self, dice:Dice) -> bool:
        """
        Determines if the player can make a move automatically based on the current dice value.

        Args:
            dice (Dice): The current dice object.

        Returns:
            bool: True if the player can auto play, False otherwise.
        """
        if dice.is_max_value(): return False
        
        if self.is_only1_out() or self.is_only1_piece_to_move(dice.value):
            return self.atual_piece.to_animate_move(dice.value)                
    