import unittest

from collections import deque
from snake_game import Game, Dir, Step


class SnakeGameTest(unittest.TestCase):
    def test_small_board(self):
        with self.assertRaises(SystemExit):
            Game(2, 2)

        with self.assertRaises(SystemExit):
            Game(2, 3)

        with self.assertRaises(SystemExit):
            Game(3, 2)

    def test_generate_pellet(self):
        width = 10
        height = 10
        game = Game(width, height)
        pellet = game._generate_pellet()
        self.assertNotIn(pellet, game.snake)
        self.assertLessEqual(pellet[0], width - 1)
        self.assertLessEqual(pellet[1], height - 1)

    def test_get_next_coord(self):
        game = Game(10, 10)
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (6, 5))

        game.prev_direction = Dir.SOUTH
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (5, 6))

        game.prev_direction = Dir.WEST
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (4, 5))

        game.prev_direction = Dir.NORTH
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (5, 4))

        game.prev_direction = Dir.EAST
        next_coord = game._get_next_coord(Step.LEFT)
        self.assertEqual(next_coord, (5, 4))

        game.prev_direction = Dir.EAST
        next_coord = game._get_next_coord(Step.RIGHT)
        self.assertEqual(next_coord, (5, 6))

    def test_wrap_around_next_coord(self):
        # check boundaries that snake wraps around
        game = Game(10, 10)
        game.snake = deque([(0, 5), (1, 5), (2, 5)])
        game.prev_direction = Dir.WEST
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (9, 5))

        game.snake = deque([(9, 5), (8, 5), (7, 5)])
        game.prev_direction = Dir.EAST
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (0, 5))

        game.snake = deque([(5, 0), (5, 1), (5, 2)])
        game.prev_direction = Dir.NORTH
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (5, 9))

        game.snake = deque([(5, 9), (5, 8), (5, 7)])
        game.prev_direction = Dir.SOUTH
        next_coord = game._get_next_coord(Step.FORWARD)
        self.assertEqual(next_coord, (5, 0))

    def test_check_collision(self):
        game = Game(10, 10)
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertFalse(game._check_collision(6, 5))

        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertTrue(game._check_collision(5, 5))

        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertFalse(game._check_collision(3, 5))

    def test_check_no_collision_edge(self):
        game = Game(10, 10)
        game.snake = deque([(5, 5), (4, 5), (4, 4), (5, 4)])
        game.prev_direction = Dir.EAST
        self.assertFalse(game._check_collision(5, 4))

    def test_step_forward(self):
        game = Game(10, 10)
        game.pellet = (0, 0)  # set pellet to (0, 0) for testing
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertTrue(game.step(Step.FORWARD))
        self.assertEqual(game.snake, deque([(6, 5), (5, 5), (4, 5)]))

        game.snake = deque([(5, 5), (5, 4), (4, 4)])
        game.prev_direction = Dir.SOUTH
        self.assertTrue(game.step(Step.FORWARD))
        self.assertEqual(game.snake, deque([(5, 6), (5, 5), (5, 4)]))

        game.snake = deque([(5, 5), (6, 5), (7, 5)])
        game.prev_direction = Dir.WEST
        self.assertTrue(game.step(Step.FORWARD))
        self.assertEqual(game.snake, deque([(4, 5), (5, 5), (6, 5)]))

        game.snake = deque([(5, 5), (5, 6), (5, 7)])
        game.prev_direction = Dir.NORTH
        self.assertTrue(game.step(Step.FORWARD))
        self.assertEqual(game.snake, deque([(5, 4), (5, 5), (5, 6)]))

    def test_step_left(self):
        game = Game(10, 10)
        game.pellet = (0, 0)  # set pellet to (0, 0) for testing
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertTrue(game.step(Step.LEFT))
        self.assertEqual(game.snake, deque([(5, 4), (5, 5), (4, 5)]))

        game.snake = deque([(5, 5), (5, 4), (4, 4)])
        game.prev_direction = Dir.SOUTH
        self.assertTrue(game.step(Step.LEFT))
        self.assertEqual(game.snake, deque([(6, 5), (5, 5), (5, 4)]))

        game.snake = deque([(5, 5), (6, 5), (7, 5)])
        game.prev_direction = Dir.WEST
        self.assertTrue(game.step(Step.LEFT))
        self.assertEqual(game.snake, deque([(5, 6), (5, 5), (6, 5)]))

        game.snake = deque([(5, 5), (5, 6), (5, 7)])
        game.prev_direction = Dir.NORTH
        self.assertTrue(game.step(Step.LEFT))
        self.assertEqual(game.snake, deque([(4, 5), (5, 5), (5, 6)]))

    def test_step_right(self):
        game = Game(10, 10)
        game.pellet = (0, 0)  # set pellet to (0, 0) for testing
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertTrue(game.step(Step.RIGHT))
        self.assertEqual(game.snake, deque([(5, 6), (5, 5), (4, 5)]))

        game.snake = deque([(5, 5), (5, 4), (4, 4)])
        game.prev_direction = Dir.SOUTH
        self.assertTrue(game.step(Step.RIGHT))
        self.assertEqual(game.snake, deque([(4, 5), (5, 5), (5, 4)]))

        game.snake = deque([(5, 5), (6, 5), (7, 5)])
        game.prev_direction = Dir.WEST
        self.assertTrue(game.step(Step.RIGHT))
        self.assertEqual(game.snake, deque([(5, 4), (5, 5), (6, 5)]))

        game.snake = deque([(5, 5), (5, 6), (5, 7)])
        game.prev_direction = Dir.NORTH
        self.assertTrue(game.step(Step.RIGHT))
        self.assertEqual(game.snake, deque([(6, 5), (5, 5), (5, 6)]))

    def test_pellet_eaten(self):
        game = Game(10, 10)
        game.pellet = (6, 5)  # set pellet to be consumed in next move
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.prev_direction = Dir.EAST
        self.assertTrue(game.step(Step.FORWARD))
        self.assertEqual(game.snake, deque([(6, 5), (5, 5), (4, 5), (3, 5)]))

    def test_game_over(self):
        game = Game(10, 10)
        game.pellet = (0, 0)  # set pellet to (0, 0) for testing
        game.snake = deque([(5, 5), (4, 5), (4, 4), (5, 4), (6, 4)])
        game.prev_direction = Dir.EAST
        self.assertFalse(game.step(Step.LEFT))

    def test_win_game(self):
        game = Game(3, 3)
        game.pellet = (0, 0)  # set pellet to be consumed in next move to win game
        game.prev_direction = Dir.WEST
        game.snake = deque(
            [(1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2)]
        )
        self.assertFalse(game.step(Step.FORWARD))

    def test_get_print_symbol(self):
        game = Game(10, 10)
        game.snake = deque([(5, 5), (4, 5), (3, 5)])
        game.pellet = (0, 0)
        self.assertEqual(game._get_print_symbol(5, 5), "o")
        self.assertEqual(game._get_print_symbol(4, 5), "x")
        self.assertEqual(game._get_print_symbol(3, 5), "x")
        self.assertEqual(game._get_print_symbol(0, 0), "@")
        self.assertEqual(game._get_print_symbol(1, 1), ".")
