from perudo_game.game_core import Game
from perudo_game.players.CLI_player import HumanPlayer
from perudo_game.ui import CLI
from players.player_v1 import Player

ui = CLI()
players = {
    0: HumanPlayer,
    1: Player,
}
Game(players, ui, [(0, HumanPlayer("{}"))]).start()
