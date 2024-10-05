from model.dice import Dice
from model.player import Player

class AIPlayer(Player):
    def __init__(self, color: str) -> None:
        super().__init__(color)

    def update(self, dice:Dice) -> None:
        pass