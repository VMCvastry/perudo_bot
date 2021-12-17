from perudo_game.exceptions import IllegalMove
from perudo_game.game.dices_emoji import get_face_emoji


class GameMove:
    def __init__(self, number, amount):
        if (
            not isinstance(number, int)
            or not isinstance(amount, int)
            or number > 6
            or number < 1
            or amount < 1
        ):
            raise IllegalMove
        self.number: int = number
        self.amount: int = amount
        self.player_id: int = None

    def __str__(self):
        return f"Player {self.player_id} called {self.amount} X {get_face_emoji(self.number)}"
