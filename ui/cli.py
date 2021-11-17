from gameMove import GameMove
from gameStatus import GameStatus
from ui import UI
import os


class CLI(UI):
    def show_header(self):
        print("header")

    def show_summary(self, game: GameStatus):
        os.system("clear")
        print("summary")
        [print(p) for p in game.players]

    def show_round(self, moves: list[GameMove]):
        print("pastmoves")
        print(moves[-1])

    def show_round_check(self, game: GameStatus):
        print("the dices are")
        print([p.numbers for p in game.players])

    def show_players_dices(self, numbers: list[int]):
        print("your dices:")
        print(numbers)

    def show_result(self, result):
        # print("he won")
        print(result)
        input("continue")
