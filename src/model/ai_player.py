from model.dice import Dice
from model.player import Player

class AIPlayer(Player):
    """
    Represents an AI player in the game, handling automated gameplay logic.
    """
    
    def __init__(self, color: str) -> None:
        """
        Initializes an AIPlayer with the specified color.

        Args:
            color (str): The color of the player.
        """
        super().__init__(color)

    def update(self, dice:Dice) -> None:
        """
        Updates the AI player's actions based on the rolled dice.

        Args:
            dice (Dice): The current dice object that tracks the rolled state.
        """
        pass