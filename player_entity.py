from playerInterface import PlayerInterface


class PlayerEntity:
    def __init__(self, player: PlayerInterface,id):
        self.player = player
        # self.tokens = 21
        self.n_dices = 6
        self.numbers = []
        self.id=id

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
        self.player.set_rolled_dices(numbers.copy())
