import random

from perudo_game.exceptions import PlayerException
from perudo_game.game.gameMove import GameMove
from perudo_game.game.gameStatus import GameStatus
from perudo_game.game.player_entity import PlayerEntity
from perudo_game.players import PlayerInterface
from perudo_game.players.CLI_player import HumanPlayer
from perudo_game.ui import UI, CLI


def roll_dice() -> int:
    return random.randint(1, 6)


class Game:
    def __init__(
        self,
        game_players: dict[int, type[PlayerInterface]],
        selected_ui: UI,
        actual_players=[],  # not a problem since default type is not actually used
    ):

        self.players = {
            i: PlayerEntity(player, i) for i, player in game_players.items()
        }
        for player_id, player_instance in actual_players:
            self.players[player_id].instance = player_instance

        self.n_players = len(self.players)
        self.game_status = GameStatus(list(self.players.values()))
        self.next_player_id = random.randint(0, self.n_players - 1)
        self.ui = selected_ui
        self.winner = None
        self.exception: PlayerException = None

    def on_going(self):
        return len(self.game_status.players) != 1

    def get_next_player(self) -> PlayerEntity:
        player = self.players[self.next_player_id]
        self.next_player_id = self.game_status.next_id(self.next_player_id)
        return player

    def penalty(self, id):
        self.players[id].n_dices -= 1
        if self.players[id].n_dices == 0:
            self.game_status.players.remove(self.players[id])
            if id == self.next_player_id:
                self.next_player_id = self.game_status.next_id(self.next_player_id)
        else:
            self.next_player_id = id

    def check(self):
        self.ui.show_round_check(self.game_status)
        move = self.game_status.last_move()
        found = 0
        for player in self.players.values():
            found += player.numbers.count(move.number)
        if found >= move.amount:
            self.penalty(self.game_status.last_id(self.next_player_id))
        else:
            self.penalty(move.player_id)
        self.ui.show_result(found >= move.amount)
        self.game_status.new_round()
        self.start_round()

    def evaluate_move(self, move: GameMove):
        self.game_status.add_move(move)

    def start_round(self):
        self.ui.show_summary(self.game_status)
        for id, player in self.players.items():
            player.set_rolled_dices([roll_dice() for _ in range(player.n_dices)])

    def start(self):
        self.start_round()
        self.ui.show_header()
        while self.on_going():
            player = self.get_next_player()
            self.ui.show_round(self.game_status.moves_history)
            self.ui.show_players_dices(player.numbers, player.id)
            try:
                move = player.make_move(self.game_status.get_game_info())
            except Exception as e:
                self.exception = PlayerException(player.id, e)
                raise PlayerException(player.id, e)
            if not move:
                self.ui.show_player_move(move, player.id)
                self.check()
            else:
                move.player_id = player.id
                self.evaluate_move(move)
                self.ui.show_player_move(move, player.id)
        print(f"player {self.next_player_id} won")
        self.winner = [self.next_player_id]
        return self.next_player_id


# if __name__ == "__main__":
#     ui = CLI()
#     players = {
#         0: HumanPlayer,
#         1: Bot1,
#     }
#     Game(players, ui).start()
