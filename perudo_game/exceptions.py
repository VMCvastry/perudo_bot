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
    def __init__(
        self,
        msg="You Must call a higher number of dices or the same number of dices of an higher seed",
    ):
        self.message = msg
        super().__init__(self.message)


class InvalidBluff(Exception):
    def __init__(self):
        self.message = "Cannot call bluff on first move"
        super().__init__(self.message)


class InvalidSpot(Exception):
    def __init__(self):
        self.message = "Cannot call Spot-on on first move"
        super().__init__(self.message)


class InvalidSpecial(Exception):
    def __init__(self):
        self.message = "The only special move available are 'bluff' and 'spot on' DO NOT use the field GameMove.special,\n use the provided methods GameMove.call_bluff()/GameMove.call_spot_on() to use them"
        super().__init__(self.message)


def raise_exception_if_invalid_move(info, move):

    if not info.moves_history[-1]:
        if move.special == "BLUFF":
            raise InvalidBluff
        elif move.special == "SPOTON":
            raise InvalidSpot
        else:
            return
    if move.special is not None:
        if move.special == "BLUFF" or move.special == "SPOTON":
            return
        else:
            raise InvalidSpecial
    last = info.moves_history[-1][-1]
    if last.number == 1:
        if move.number != 1:
            if not (move.amount > last.amount * 2):
                print("a")
                raise InvalidMove(
                    "Last call was a Jolly, you have to Double+1 that bet or call a Jolly as well"
                )
        else:
            if not (move.amount > last.amount):
                print("b")
                raise InvalidMove
    else:
        if move.number != 1:
            if not (
                move.amount > last.amount
                or (move.amount == last.amount and move.number > last.number)
            ):
                print("c")
                raise InvalidMove
        else:
            if not (move.amount >= last.amount // 2 + 1):
                print("d")
                raise InvalidMove(
                    "You are calling a Jolly, you have to bet at least half +1 of the previous bet"
                )
