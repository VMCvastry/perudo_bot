# Perudo Arena Bot
This is a Telegram bot [Here](https://t.me/perudoarenabot) that allows you to code your very own implementation of an AI playing the [Perudo](https://it.wikipedia.org/wiki/Perudo) dice game(aka [Dudo](https://en.wikipedia.org/wiki/Dudo), aka Liar's dice).
The actual rules implemented in the game can be read [Here](#rules).

Starting the Telegram chat you will be able to see the leaderboard of the best bots so far and play against them.
Most importantly you will be able tto upload your bot and see who is the best.

## How to  Upload your bot
Once you have written your Bot just drop the .py in the telegram chat.
Unfortunately at the moment Only python 3 is currently supported.

## How to write your bot
Since it needs to be run on ours server and need to be compatible with the current implementation of the game 
your code must follow a few guidelines:
* First the bot must extend the [PlayerInterface](perudo_game/players/playerInterface.py) superclass.
* You Must override just the two abstract methods.
* `get_player_name` must be  a static method that  just returns a string which will be your bots nickname.
    ```python
    @staticmethod
    def get_player_name() -> str:
        return "Pippo the Bluffer"
    ```
* `move` must take two arguments and return a [GameMove](perudo_game/game/gameMove.py) or  `None` if you call the bluff.
* The first argument of type [GameInfo](perudo_game/game/game_info.py) that will give you all the information on the current round.
* The second will be a list of integers representing your dices
* Inside your player you will have access to a `self.status` dict where you can store all the information and computation 
    that you want to preserve between moves, **Everything else inside the player Object will be resetted on each move**
* `self.status` **MUST be JSON serializable**
* Inside the functions in the submitted code you will be able to use only the modules and functions listed [Here](#removed-builtins-functions).
  Eg using functions like `print`, `eval` will throw an error, importing other moules outside the listed ones will throw an error.
  _If you think that a particular module should be available open an Issue and if it is safe it will be added right away_
* Check the [DemoBot](perudo_game/players/player_demo.py) to solve all of  your doubts.

## More info on the provided classes
### GameMove
```python
class GameMove:
    def __init__(self, number, amount):
        if number > 6 or number < 1 or amount < 1:
            raise IllegalMove
        self.number: int = number
        self.amount: int = amount
```
This class just gets an amount for a specific dice face, raises an error if the values are nonsense.
`None` can be used instead of a GameMove to call the bluff on the last player.

### GameInfo
```python
@dataclass
class GameInfo:
    players: list[tuple[int, int]] # [(player_id,number_of_dices),...]
    round: int
    moves_history: list[list[GameMove]]
    first_call: bool
```
* `players` is a list representing for each player the tuple (player_id, remaining dices)
* `round` just states the number of the current round
* `moves_history` is a list of lists containing GameMoves each list is a round, 
   so `moves_history[-1]` is the list of the moves in the current round and `moves_history[-1][-1]` is the last move of the current round
* `first_call` is just a bool stating if you are the first player of the round and so you cannot bluff. (is `moves_history[-1]` empty )


## Rules
_Currently, a simplified version of the game is running new rules may be added later._

Each player starts having five dice and a cup, which is used for shaking the dice and concealing the dice from the other players.
The players shake their dice in their cups, and then each player looks at their own dice, keeping their dice concealed from other players. 
Then, the first player makes a bid about how many dice of a certain value are showing among all players, at a minimum. 
For example, a bid of "five threes" is a claim that between all players, there are at least five dice showing a three.
The player challenges the next player (moving clockwise) to raise the bid or call dudo(I doubt that/ you are bluffing) to end the round.

Raise

also known as "bid" in most versions, a player can increase the quantity of dice (e.g. from "five threes" to "six threes") or the die number (e.g. "five threes" to "five sixes") or both. 
If a player increases the quantity, they can choose any number e.g. a bid may increase from "five threes" to "six twos".

Call

also known as dudo, if the player calls, it means that they do not believe the previous bid was correct. 
All dice are then shown and, if the guess is not correct, the previous player (the player who made the bid) loses a die. 
If it is correct, the player who called loses a die. A player with no dice remaining is eliminated from the game.
After calling, a new round starts with the player that lost a die making the first bid, or (if that player was eliminated) the player to that player's left.

The game ends when only one player has dice remaining; that player is the winner.



## Removed Builtins Functions

* print
* eval
* exec

## Available modules

* PlayerInterface
* GameMove
* GameInfo
* random
* collections.Counter
* json

Open an issue to ask for new modules.
