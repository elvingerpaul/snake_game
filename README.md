# Snake Game
This respository contains a basic implementation of the Snake Game. The minimum requirements of the game can be found in the [Task Description](#task-description). The game can be played from the command line in:
- automatic mode: the game will automatically generate directions to consume the first pellet on the board and then terminate.
- interactive mode: the user will be prompted to input directions for the snake to move along the board until the user either wins, looses or exits. The snake moves in time intervals of 1 second. Not providing an input will result in the snake moving forward. **The user needs to confirm the input by pressing Enter**.

## Requirements
It is expected that the host has Python installed on the machine. All instructions below assume Python3 to be installed. Follow the steps below to create a virtual environment and install the necessary packages.
```
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

## How to play the game?
You can play the game by executing the `main.py` file and either pass it the `--consume_first_pellet` flag to run in automatic mode or the `interactive` flag to run in automatic mode. In addition you can optionally pass it the `--width [int]` and `--height [int]` flag to specify the board dimensions. The default dimension is set to `8x8`.

#### Example to run in automatic mode
```
python3 main.py --consume_first_pellet --width 10 --height 10
```

#### Example to run in interactive mode
```
python3 main.py --interactive --width 10 --height 10
```

## How to run the tests?
To run the tests, you can run
```
python3 -m unittest snake_game_tests.py
```

To report the test coverage, you can execute the commands below
```
python3 -m coverage run -m unittest snake_game_tests.py
...
python3 -m coverage report -m
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
snake_game.py            74      5    93%   117-121
snake_game_tests.py     159      0   100%
---------------------------------------------------
TOTAL                   233      5    98%
```

## Task Description

Your task is to model a Snake game, logic wise only. There's a summary of what Snake is below. No need for a fancy UI or threading, if you need to display something do it in Std.out!

#### Steps

1) Model the board (that wraps around), the snake and food pellets.

2) Place a size 2 snake in the middle of the board and a food somewhere else than the snake.

3) `Display` board state in the console (ASCII "art")

    - The snake's body: 'x'

    - The snake's head: 'o'

    - The food pellet: '@'

    - An empty space: '.'

    - The inital state should look similar to this:

    ```

    ........

    ........

    ........

    ...xxo..

    ........

    ......@.

    ........

    ........

    ```

4) Define a method that performs a 'step' of the game

    - takes a possible user input as parameter

    - is called from outside (Launcher?) at a regular time interval

    - update the board's state

5) Code an input sequence that eats the first food pellet. An example could be
    - step()
    - step(right)
    - step()
    - step()

6) Randomise food pellet placement


#### Summary: Snake game
- You control a Snake that moves around in a grid, the snake spans over a 2 cells at the beginning.
- You can only turn the snake left or right and it moves one cell every "game turn".
- There is always one food pellet on the grid.
- Goal of the game is to eat said pellets by moving the snake to its position.
- When the snake eats a pellet it grows one cell longer.
- If the snake collides with itself, the game is lost.
- If the snake reaches one of the grid's borders, it wraps around (i.e. going out on the left side means you come back in on the right side).