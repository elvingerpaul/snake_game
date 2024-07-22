import random
import sys

from collections import deque
from enum import Enum


class Dir(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Step(Enum):
    FORWARD = 1
    LEFT = 2
    RIGHT = 3


class Game:
    def __init__(self, height: int, width: int):
        if width < 3 or height < 3:
            print("Width and height of board must be at least 3.")
            sys.exit(1)
        self._height = height
        self._width = width

        # intial snake position
        self.snake = deque()
        self.snake.append((self._width // 2, self._height // 2))
        self.snake.append(((self._width // 2 - 1) % self._width, self._height // 2))
        self.snake.append(((self._width // 2 - 2) % self._width, self._height // 2))

        # initial pellet position
        self.pellet = self._generate_pellet()

        self.prev_direction = Dir.EAST
        self.navigation = {
            Dir.NORTH: {
                Step.FORWARD: Dir.NORTH,
                Step.LEFT: Dir.WEST,
                Step.RIGHT: Dir.EAST,
            },
            Dir.EAST: {
                Step.FORWARD: Dir.EAST,
                Step.LEFT: Dir.NORTH,
                Step.RIGHT: Dir.SOUTH,
            },
            Dir.SOUTH: {
                Step.FORWARD: Dir.SOUTH,
                Step.LEFT: Dir.EAST,
                Step.RIGHT: Dir.WEST,
            },
            Dir.WEST: {
                Step.FORWARD: Dir.WEST,
                Step.LEFT: Dir.SOUTH,
                Step.RIGHT: Dir.NORTH,
            },
        }

    def _generate_pellet(self) -> tuple[int, int]:
        """Generates a new pellet in a random location that should not be part
        of the snake"""
        available_positions = [
            (x, y)
            for x in range(self._width)
            for y in range(self._height)
            if (x, y) not in self.snake
        ]
        return random.choice(available_positions)

    def _get_next_coord(self, step: Step) -> tuple[int, int]:
        """Calculates the next coordinate of the snake's head based on the
        previous direction"""
        s_x, s_y = self.snake[0]
        next_dir = self.navigation[self.prev_direction][step]
        self.prev_direction = next_dir
        match next_dir:
            case Dir.NORTH:
                return s_x, (s_y - 1) % self._height
            case Dir.EAST:
                return (s_x + 1) % self._width, s_y
            case Dir.SOUTH:
                return s_x, (s_y + 1) % self._height
            case Dir.WEST:
                return (s_x - 1) % self._width, s_y

    def _check_collision(self, next_x: int, next_y: int) -> bool:
        """Checks if the next move will result in a collision. Exclude the tail
        because it will move forward"""
        if (next_x, next_y) in self.snake and (next_x, next_y) != self.snake[-1]:
            return True
        return False

    def _get_print_symbol(self, x: int, y: int) -> str:
        """Returns the symbol to be printed at the given coordinate"""
        if (x, y) in self.snake:
            return "o" if (x, y) == self.snake[0] else "x"
        elif (x, y) == self.pellet:
            return "@"
        else:
            return "."

    def step(self, step: Step = Step.FORWARD) -> bool:
        """Performs one move of the snake, a move can be advancing the snake
        forward (default), left or right. Returns True if the game is still
        running, False otherwise in the case of a collision or win."""
        next_x, next_y = self._get_next_coord(step)

        if self._check_collision(next_x, next_y):
            print("Collision: Game Over!")
            return False

        print(f"Moving {step.name}")
        if (next_x, next_y) == self.pellet:
            self.snake.appendleft((next_x, next_y))
            if len(self.snake) == self._width * self._height:
                print("You Win!")
                return False
            self.pellet = self._generate_pellet()
        else:
            self.snake.appendleft((next_x, next_y))
            self.snake.pop()

        return True

    def display(self) -> None:
        """Displays the current state of the game"""
        for y in range(self._height):
            row = []
            for x in range(self._width):
                row.append(self._get_print_symbol(x, y))
            print(" ".join(row))
