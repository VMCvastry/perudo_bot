import random
from copy import deepcopy

from GameMove import GameMove
from gameStatus import GameStatus
from player1 import Player
from player_entity import PlayerEntity


def roll_dice() -> int:
    return random.randint(0, 6)


class Game:
    def __init__(self):
        self.players = {x: PlayerEntity(Player(x), x) for x in range(3)}
        self.n_players = len(self.players)
        self.game_status = GameStatus(list(self.players.values()))
        self.current_player_id = random.randint(0, self.n_players)

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
            if id==self.current_player_id:
                self.current_player_id = self.game_status.next_id(self.current_player_id)
        else:
            self.current_player_id=id

    def check(self):
        move = self.game_status.last_move()
        found = 0
        for player in self.players:
            found += player.numbers.count(move.number)
        if found >= move.amount:
            self.penalty(self.current_player_id)
        else:
            self.penalty(move.player_id)
        self.game_status.new_round()
        self.start_round()

    def evaluate_move(self, move: GameMove):
        self.game_status.add_move(move)

    def start_round(self):
        for player in self.players:
            player.set_rolled_dices([roll_dice() for _ in range(player.n_dices)])

    def start(self):
        self.start_round()
        while self.on_going():
            player = self.get_next_player()
            move = player.player.make_a_move(deepcopy(self.game_status))
            move.player_id = player.id
            if not move:
                self.check()
            else:
                self.evaluate_move(move)
        print(f"player {self.current_player_id} won")


if __name__ == '__main__':
    Game().start()
