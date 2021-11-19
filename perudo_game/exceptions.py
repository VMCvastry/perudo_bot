class PlayerException(Exception):
    def __init__(self, player_id, exception: Exception):
        self.player_id = player_id
        self.exception = exception
        self.message = str(exception)
        super().__init__(self.message)
