from perudo_game.exceptions import IllegalMove


class GameMove:
    def __init__(self, number, amount):
        if (
                not isinstance(number, int)
                or isinstance(amount, int)
                or number > 6
                or number < 1
                or amount < 1
        ):
            raise IllegalMove
        self.number: int = number
        self.amount: int = amount
        self.player_id: int = None

    def __str__(self):
        return f"player {self.player_id} called {self.number} with multiplicity {self.amount}"
