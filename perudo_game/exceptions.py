class PlayerException(Exception):
    def __init__(self, player_id, exception: Exception):
        self.player_id = player_id
        self.exception = exception
        self.message = str(exception)
        super().__init__(self.message)


class IllegalMove(Exception):
    def __init__(self):
        self.message = "move.numbers must be in [1,6] and amount must be >0"
        super().__init__(self.message)
