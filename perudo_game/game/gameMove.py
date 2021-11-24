from perudo_game.exceptions import IllegalMove


class GameMove:
    def __init__(self, number, amount):
        if number > 6 or number < 1 or amount < 1:
            raise IllegalMove
        self.number: int = number
        self.amount: int = amount
        self.player_id: int = None
