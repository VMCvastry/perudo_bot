class Player(PlayerInterface):
    # TODO player_id in abstract interface, static name
    def __init__(self, player_id: int):
        self.name = "Bot3"
        self.numbers = []

    def get_player_name(self) -> str:
        return self.name

    def make_a_move(self, status):
        print("MOVING", self.name)
        numbers = Counter(self.numbers)
        value, n = numbers.most_common(1)[0]
        if status.first_call:
            return GameMove(value, n)
        else:
            last = status.moves_history[-1][-1]
            if last.amount >= n:
                if random.random() > 0.5:
                    return GameMove(value, last.amount + 1)
                return None
            else:
                return GameMove(value, n)

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
