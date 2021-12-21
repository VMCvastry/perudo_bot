from telegram.ext import CallbackContext

from perudo_game.game.dices_emoji import get_face_emoji
from perudo_game.game.gameStatus import GameStatus
from perudo_game.ui.ui_interface import UI
from perudo_game.game.gameMove import GameMove


class TelegramUI(UI):
    def __init__(self, context: CallbackContext, chat_id, player_id, bots):
        self.bot = context.bot
        self.chat_id = chat_id
        self.player_id = player_id
        self.bots = bots

    def show_header(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="Game is starting!\nUse /stop to interrupt the game",
        )

    def show_summary(self, game: GameStatus):
        message = f"Round {game.round}:\n"
        for player in game.players:
            if player.id == self.player_id:
                message += f"You    {'🎲'*player.n_dices}\n"
            else:
                message += (
                    f"{self.bots[player.id].get_player_name()}  {'🎲'*player.n_dices}\n"
                )
        self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
        )

    def show_round(self, moves: list[list[GameMove]]):
        # self.bot.send_message(
        #     chat_id=self.chat_id,
        #     text="Past Moves List:\n" + "\n".join([str(m) for m in moves[-1]]),
        # )
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
                text="Your dices:   " + " ".join(map(str, sorted(numbers))),
            )
        print("your dices:")
        print(numbers)

    def show_player_move(self, move):
        if move.player_id != self.player_id:
            if move.special == GameMove.BLUFF:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Player {move.player_id} called the Bluff",
                )
            elif move.special == GameMove.SPOT_ON:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Player {player_id} called Spot On",
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"{self.bots[move.player_id].get_player_name()}  called {get_face_emoji(move.number) * move.amount}",
                    # text=f"{self.bots[move.player_id].get_player_name()}  called {move.amount} X {get_face_emoji(move.number)}",
                )

    def show_result(self, result, special):
        if result:
            if special == GameMove.BLUFF:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text="The Player was not bluffing",
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text="The Number is not right",
                )
        else:
            if special == GameMove.BLUFF:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text="It was a Bluff!",
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text="Spot On!",
                )
        print(result)

    def show_winner(self, player_id):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=f"Player {player_id} has Won!",
        )
