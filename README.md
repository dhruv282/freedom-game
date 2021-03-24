# Freedom Game

This game is a two player game where a human player plays against the computer. The computer uses minimax algorithm with alpha-beta pruning to determine the best move for it. Description about this game can be found at: [https://boardgamegeek.com/boardgame/100480/freedom](https://boardgamegeek.com/boardgame/100480/freedom)

[Python 3](https://www.python.org/downloads/) along with the [random](https://docs.python.org/3/library/random.html) and [copy](https://docs.python.org/3/library/copy.html) packages are required to run this game.

## Running the game:
The game requires exactly 2 arguments;

- `m`: number of rows in the board
- `n`: number of columns in the board

```shell
$ python3 startGame.py m n 
```
### Example:
```shell
$ python3 startGame.py 10 10
```