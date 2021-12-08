from telegram.ext import CallbackContext

from perudo_game.game.gameStatus import GameStatus
from perudo_game.ui.ui_interface import UI
from perudo_game.game.gameMove import GameMove


class TelegramUI(UI):
    def __init__(self, context: CallbackContext, chat_id, player_id):
        self.bot = context.bot
        self.chat_id = chat_id
        self.player_id = player_id

    def show_header(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="You are Player 0",
        )

    def show_summary(self, game: GameStatus):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=f"Game Status on round {game.round}:\n"
            + "\n".join([str(p) for p in game.players]),
        )

    def show_round(self, moves: list[list[GameMove]]):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Past Moves List:\n" + "\n".join([str(m) for m in moves[-1]]),
        )
        print("pastmoves\n" + "\n".join([str(m) for m in moves[-1]]))

    def show_round_check(self, game: GameStatus):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="the dices are\n" + str([p.numbers for p in game.players]),
        )
        print("the dices are")
        print([p.numbers for p in game.players])

    def show_players_dices(self, numbers: list[int], player_id):
        if player_id == self.player_id:
            self.bot.send_message(
                chat_id=self.chat_id,
                text="Your dices:\n" + " ".join(map(str, numbers)),
            )
        print("your dices:")
        print(numbers)

    def show_player_move(self, move, player_id):
        if player_id != self.player_id:
            if not move:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Player {player_id} called the Bluff",
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=str(move),
                )

    def show_result(self, result):
        if result:
            self.bot.send_message(
                chat_id=self.chat_id,
                text="The Player was not bluffing",
            )
        else:
            self.bot.send_message(
                chat_id=self.chat_id,
                text="It was a Bluff!",
            )
        print(result)

    def show_winner(self, player_id):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=f"Player {player_id} has Won!",
        )
