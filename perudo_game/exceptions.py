class PlayerException(Exception):
    def __init__(self, player_id, exception: Exception):
        self.player_id = player_id
        self.exception = exception
        self.message = str(exception)
        super().__init__(self.message)


class IllegalMove(Exception):
    def __init__(self):
        self.message = (
            "move.numbers must be an integer in [1,6] and amount must be and integer >0"
        )
        super().__init__(self.message)


class InvalidMove(Exception):
    def __init__(self):
        self.message = "You Must call a higher number of dices or the same number of dices of an higher seed"
        super().__init__(self.message)


class InvalidBluff(Exception):
    def __init__(self):
        self.message = "Cannot call bluff on first move"
        super().__init__(self.message)


def raise_exception_invalid_move(info, move):

    if not info.moves_history[-1]:
        if move is None:
            raise InvalidBluff
        else:
            return
    if move is None:
        return
    last = info.moves_history[-1][-1]
    if not (
        move.amount > last.amount
        or (move.amount == last.amount and move.number > last.number)
    ):
        raise InvalidMove
