import argparse
import sys

from inputimeout import inputimeout, TimeoutOccurred
from snake_game import Game, Step


class Player:
    def __init__(self, game: Game):
        self.game = game

    def read_step_from_input(self) -> Step:
        try:
            step = inputimeout(
                prompt="Please enter your next move (l: left, r: right) to move the snake. No input will result in snake moving forward. To exit the game, enter 'q': ",
                timeout=1,
            )
        except TimeoutOccurred:
            step = "f"

        match step:
            case "f":
                return Step.FORWARD
            case "l":
                return Step.LEFT
            case "r":
                return Step.RIGHT
            case "q":
                print("Exiting the game.")
                sys.exit(0)
            case _:
                print(f"{step} is an invalid input.")
                return Step.FORWARD

    def run_interactive(self) -> None:
        print("Running in interactive mode.")
        self.game.display()
        step = self.read_step_from_input()
        while self.game.step(step):
            self.game.display()
            step = self.read_step_from_input()

    def run_consume_first_pellet(self) -> None:
        print("Automatically consuming first pellet.")
        # move snake to correct x-coordinate
        snake_x, snake_y = self.game.snake[0]
        pellet_x, pellet_y = self.game.pellet
        while snake_x != pellet_x:
            self.game.step(Step.FORWARD)
            self.game.display()
            snake_x, snake_y = self.game.snake[0]

        if snake_x == pellet_x and snake_y == pellet_y:
            print("Pellet consumed.")
            self.game.display()
            return

        # make one RIGHT turn to move along y axis
        self.game.step(Step.RIGHT)
        self.game.display()
        snake_x, snake_y = self.game.snake[0]

        # move snake to correct y-coordinate
        while snake_y != pellet_y:
            self.game.step(Step.FORWARD)
            self.game.display()
            snake_x, snake_y = self.game.snake[0]

        print("Pellet consumed.")
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interactive", action="store_true", help="Run the game in interactive mode"
    )
    parser.add_argument(
        "--consume_first_pellet",
        action="store_true",
        help="Automatically consume the first pellet",
    )
    parser.add_argument("--width", type=int, default=8, help="Width of the game board")
    parser.add_argument(
        "--height", type=int, default=8, help="Height of the game board"
    )
    args = parser.parse_args()

    game = Game(args.height, args.width)
    player = Player(game)

    if args.interactive:
        player.run_interactive()
    elif args.consume_first_pellet:
        player.run_consume_first_pellet()
    else:
        print(
            "No player mode selected. Choose either '--iteractive' or '--consume_first_pellet'"
        )
        sys.exit(1)
