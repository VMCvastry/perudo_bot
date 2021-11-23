class Player(PlayerInterface):
    def __init__(self, player_status_JSON):
        super().__init__(player_status_JSON)

    @staticmethod
    def get_player_name() -> str:
        return "Bot_2"

    def make_a_move(self, status: GameInfo, numbers) -> (GameMove, str):
        print("MOVING")
        numbers = Counter(numbers)
        value, n = numbers.most_common(1)[0]
        if status.first_call:
            return GameMove(value, n), self.get_ending_status_as_JSON()
        else:
            last = status.moves_history[-1][-1]
            if last.amount >= n:
                if random.random() > 0.5:
                    return (
                        GameMove(value, last.amount + 1),
                        self.get_ending_status_as_JSON(),
                    )
                return None, self.get_ending_status_as_JSON()
            else:
                return GameMove(value, n), self.get_ending_status_as_JSON()

    def get_ending_status_as_JSON(self) -> str:
        return json.dumps(self.status)
