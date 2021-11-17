import random
from copy import deepcopy

from GameMove import GameMove
from gameStatus import GameStatus
from players.player1 import Player
from player_entity import PlayerEntity
from players.player2 import HumanPlayer
from ui import UI
from ui.cli import CLI


def roll_dice() -> int:
    return random.randint(0, 6)


class Game:
    def __init__(self, ui: UI):
        self.players = {x: PlayerEntity(HumanPlayer(x), x) for x in range(3)}
        self.n_players = len(self.players)
        self.game_status = GameStatus(list(self.players.values()))
        self.current_player_id = random.randint(0, self.n_players - 1)
        self.ui = ui

    def on_going(self):
        return len(self.game_status.players) != 1

    def get_next_player(self) -> PlayerEntity:
        player = self.players[self.current_player_id]

        self.current_player_id = self.game_status.next_id(self.current_player_id)
        return player

    def penalty(self, id):
        self.players[id].n_dices -= 1
        if self.players[id].n_dices == 0:
            self.game_status.players.remove(self.players[id])
            if id == self.current_player_id:
                self.current_player_id = self.game_status.next_id(
                    self.current_player_id
                )
        else:
            self.current_player_id = id

    def check(self):
        self.ui.show_round_check(self.game_status)
        move = self.game_status.last_move()
        found = 0
        for player in self.players.values():
            found += player.numbers.count(move.number)
        if found >= move.amount:
            self.penalty(self.current_player_id)
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
            self.ui.show_players_dices(player.numbers)
            move = player.player.make_a_move(deepcopy(self.game_status))
            if not move:
                self.check()
            else:
                move.player_id = player.id
                self.evaluate_move(move)
        print(f"player {self.current_player_id} won")


if __name__ == "__main__":
    ui = CLI()
    Game(ui).start()
