import os

from perudo_game.game.gameMove import GameMove
from perudo_game.game.gameStatus import GameStatus
from perudo_game.ui import UI


class CLI(UI):
    def show_header(self):
        print("header")

    def show_summary(self, game: GameStatus):
        # os.system("clear")
        print("summary")
        [print(p) for p in game.players]

    def show_round(self, moves: list[list[GameMove]]):
        print("pastmoves\n" + "\n".join([str(m) for m in moves[-1]]))

    def show_round_check(self, game: GameStatus):
        print("the dices are")
        print([p.numbers for p in game.players])

    def show_players_dices(self, numbers: list[int], player_id):
        print("your dices:")
        print(numbers)

    def show_result(self, result, special):
        # print("he won")
        print(result, special)
        input("continue")

    def show_player_move(self, move, player_id):
        pass

    def show_winner(self, player_id):
        pass
