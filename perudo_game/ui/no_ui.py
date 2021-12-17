from perudo_game.game.gameMove import GameMove
from perudo_game.game.gameStatus import GameStatus
from perudo_game.ui import UI


class NoUI(UI):
    def show_header(self):
        # print("header")
        pass

    def show_summary(self, game: GameStatus):
        # os.system("clear")
        # print("summary")
        # [print(p) for p in game.players]
        pass

    def show_round(self, moves: list[GameMove]):
        # print("pastmoves")
        # print(moves[-1])
        pass

    def show_round_check(self, game: GameStatus):
        # print("the dices are")
        # print([p.numbers for p in game.players])
        pass

    def show_players_dices(self, numbers: list[int], player_id):
        # print("your dices:")
        # print(numbers)
        pass

    def show_result(self, result):
        # print("he won")
        # print(result)
        # input("continue")
        pass

    def show_player_move(self, move):
        pass

    def show_winner(self, player_id):
        pass
