import unittest
from game import Game, Block
import numpy as np
import pygame
from constants import DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT

class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize pygame once for all tests
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        # Quit pygame after all tests
        pygame.quit()

    def setUp(self):
        self.game = Game()
        # Clear the initial board
        self.game.cell_values = np.full((4, 4), None)
        self.game.available_cells = set(range(16))

    def test_empty_board_not_lose(self):
        # Empty board should not be a losing state
        self.assertFalse(self.game.if_lose())

    def test_full_board_no_merges_lose(self):
        # Create a full board with no possible merges
        values = [1, 2, 1, 2,
                 2, 1, 2, 1,
                 1, 2, 1, 2,
                 2, 1, 2, 1]
        for i in range(16):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[i//4, i%4] = block
            self.game.available_cells.remove(i)
        self.assertTrue(self.game.if_lose())

    def test_full_board_with_merges_not_lose(self):
        # Create a full board with possible merges
        values = [1, 1, 2, 3,
                 2, 3, 4, 5,
                 1, 2, 3, 4,
                 2, 3, 4, 5]
        for i in range(16):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[i//4, i%4] = block
            self.game.available_cells.remove(i)
        self.assertFalse(self.game.if_lose())

    def test_partial_board_not_lose(self):
        # Board with some empty cells should not be a losing state
        values = [1, None, 2, None,
                 None, 1, None, 2,
                 1, None, 2, None,
                 None, 1, None, 2]
        for i in range(16):
            if values[i] is not None:
                block = Block(i)
                block.val = values[i]
                self.game.cell_values[i//4, i%4] = block
                self.game.available_cells.remove(i)
        self.assertFalse(self.game.if_lose())

    def test_vertical_merges_possible(self):
        # Test vertical merges
        values = [1, 2, 1, 2,
                 1, 2, 1, 2,
                 3, 4, 3, 4,
                 3, 4, 3, 4]
        for i in range(16):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[i//4, i%4] = block
            self.game.available_cells.remove(i)
        self.assertFalse(self.game.if_lose())

    def test_horizontal_merges_possible(self):
        # Test horizontal merges
        values = [1, 1, 2, 2,
                 3, 3, 4, 4,
                 5, 5, 6, 6,
                 7, 7, 8, 8]
        for i in range(16):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[i//4, i%4] = block
            self.game.available_cells.remove(i)
        self.assertFalse(self.game.if_lose())

    def test_move_left_merge(self):
        # Test left move with merges
        values = [1, 1, 2, 2,
                 None, None, None, None,
                 None, None, None, None,
                 None, None, None, None]
        for i in range(4):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[0, i] = block
            self.game.available_cells.remove(i)
        
        self.game.update(DIR_LEFT)
        
        # After move, should be [2, 3, None, None]
        self.assertIsNotNone(self.game.cell_values[0, 0])
        self.assertEqual(self.game.cell_values[0, 0].val, 2)  # 2^2 = 4
        self.assertIsNotNone(self.game.cell_values[0, 1])
        self.assertEqual(self.game.cell_values[0, 1].val, 3)  # 2^3 = 8
        self.assertIsNone(self.game.cell_values[0, 2])
        self.assertIsNone(self.game.cell_values[0, 3])

    def test_move_right_merge(self):
        # Test right move with merges
        values = [1, 1, 2, 2,
                 None, None, None, None,
                 None, None, None, None,
                 None, None, None, None]
        for i in range(4):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[0, i] = block
            self.game.available_cells.remove(i)
        
        self.game.update(DIR_RIGHT)
        
        # After move, should be [None, None, 2, 3]
        self.assertIsNone(self.game.cell_values[0, 0])
        self.assertIsNone(self.game.cell_values[0, 1])
        self.assertIsNotNone(self.game.cell_values[0, 2])
        self.assertEqual(self.game.cell_values[0, 2].val, 2)  # 2^2 = 4
        self.assertIsNotNone(self.game.cell_values[0, 3])
        self.assertEqual(self.game.cell_values[0, 3].val, 3)  # 2^3 = 8

    def test_move_up_merge(self):
        # Test up move with merges
        values = [1, None, None, None,
                 1, None, None, None,
                 2, None, None, None,
                 2, None, None, None]
        for i in range(4):
            block = Block(i*4)
            block.val = values[i*4]
            self.game.cell_values[i, 0] = block
            self.game.available_cells.remove(i*4)
        
        self.game.update(DIR_UP)
        
        # After move, should be [2, None, None, None] in first column
        self.assertIsNotNone(self.game.cell_values[0, 0])
        self.assertEqual(self.game.cell_values[0, 0].val, 2)  # 2^2 = 4
        self.assertIsNotNone(self.game.cell_values[1, 0])
        self.assertEqual(self.game.cell_values[1, 0].val, 3)  # 2^3 = 8
        self.assertIsNone(self.game.cell_values[2, 0])
        self.assertIsNone(self.game.cell_values[3, 0])

    def test_move_down_merge(self):
        # Test down move with merges
        values = [1, None, None, None,
                 1, None, None, None,
                 2, None, None, None,
                 2, None, None, None]
        for i in range(4):
            block = Block(i*4)
            block.val = values[i*4]
            self.game.cell_values[i, 0] = block
            self.game.available_cells.remove(i*4)
        
        self.game.update(DIR_DOWN)
        
        # After move, should be [None, None, 2, 3] in first column
        self.assertIsNone(self.game.cell_values[0, 0])
        self.assertIsNone(self.game.cell_values[1, 0])
        self.assertIsNotNone(self.game.cell_values[2, 0])
        self.assertEqual(self.game.cell_values[2, 0].val, 2)  # 2^2 = 4
        self.assertIsNotNone(self.game.cell_values[3, 0])
        self.assertEqual(self.game.cell_values[3, 0].val, 3)  # 2^3 = 8

    def test_invalid_move(self):
        # Test that invalid move doesn't change the board
        values = [1, 2, 3, 4,
                 None, None, None, None,
                 None, None, None, None,
                 None, None, None, None]
        for i in range(4):
            block = Block(i)
            block.val = values[i]
            self.game.cell_values[0, i] = block
            self.game.available_cells.remove(i)
        
        # Store initial state
        initial_state = self.game.cell_values.copy()
        
        # Try to move left (should be invalid)
        self.game.update(DIR_LEFT)
        
        # Board should be unchanged
        self.assertTrue(np.array_equal(initial_state, self.game.cell_values))

if __name__ == '__main__':
    unittest.main() 