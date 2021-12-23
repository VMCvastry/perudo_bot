import random

from perudo_game.exceptions import PlayerException
from perudo_game.game.gameMove import GameMove
from perudo_game.game.gameStatus import GameStatus
from perudo_game.game.player_entity import PlayerEntity
from perudo_game.players import PlayerInterface
from perudo_game.players.CLI_player import HumanPlayer
from perudo_game.ui import UI, CLI
from perudo_game.ui.no_ui import NoUI


def roll_dice() -> int:
    return random.randint(1, 6)


class Game:
    def __init__(
        self,
        game_players: dict[int, type[PlayerInterface]],
        selected_ui: UI = NoUI(),
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
            if id == self.next_player_id:
                self.next_player_id = self.game_status.next_id(self.next_player_id)
            self.game_status.players.remove(self.players[id])
        else:
            self.next_player_id = id

    def count(self, move):
        found = 0
        for player in self.players.values():
            found += player.numbers.count(move.number)
            if move.number != 1:
                found += player.numbers.count(1)
        return found

    def count_no_jolly(self, move):
        found = 0
        for player in self.players.values():
            found += player.numbers.count(move.number)
        return found

    def check_spot(self):
        self.ui.show_round_check(self.game_status)
        move = self.game_status.last_move()
        found = self.count_no_jolly(move)
        if found != move.amount:
            self.penalty(self.game_status.last_id(self.next_player_id))
        else:
            self.penalty(move.player_id)
        self.ui.show_result(found != move.amount, GameMove.SPOT_ON)

    def check_bluff(self):
        self.ui.show_round_check(self.game_status)
        move = self.game_status.last_move()
        found = self.count(move)
        if found >= move.amount:
            self.penalty(self.game_status.last_id(self.next_player_id))
        else:
            self.penalty(move.player_id)
        self.ui.show_result(found >= move.amount, GameMove.BLUFF)

    def evaluate_move(self, move: GameMove):
        self.game_status.add_move(move)

    def start_round(self):
        self.game_status.round += 1
        self.ui.show_summary(self.game_status)
        for id, player in self.players.items():
            player.set_rolled_dices([roll_dice() for _ in range(player.n_dices)])

    def start(self):
        self.ui.show_header()
        self.start_round()
        while self.on_going():
            player = self.get_next_player()
            self.ui.show_round(self.game_status.moves_history)
            self.ui.show_players_dices(player.numbers, player.id)
            try:
                move = player.make_move(self.game_status.get_game_info())
                move.player_id = player.id
            except Exception as e:
                self.exception = PlayerException(player.id, e)
                raise PlayerException(player.id, e)
            if move.special is not None:
                self.ui.show_player_move(move)
                if move.special == GameMove.SPOT_ON:
                    self.check_spot()
                else:
                    self.check_bluff()
                self.game_status.new_round()
                self.start_round()
            else:
                self.evaluate_move(move)
                self.ui.show_player_move(move)
        self.ui.show_winner(self.next_player_id)
        self.winner = [self.next_player_id]
        return self.next_player_id
