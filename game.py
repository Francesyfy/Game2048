import pygame as pg
import numpy as np
import random
from constants import WINDOW_SIZE, BOARD_SIZE, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP


class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.bg_color = (185, 173, 161)
        self.pos = (WINDOW_SIZE - self.size) / 2
        self.cells = []
        self.cell_color = (202, 193, 181)

        gap = 10
        s = (BOARD_SIZE - gap) / 4
        for i in range(4):
            for j in range(4):
                x = self.pos + gap + s * j
                y = self.pos + gap + s * i
                self.cells.append(pg.Rect(x, y, s - gap, s - gap))

    def draw(self, surface):
        pg.draw.rect(
            surface, self.bg_color, pg.Rect(self.pos, self.pos, self.size, self.size)
        )
        for cell in self.cells:
            pg.draw.rect(surface, self.cell_color, cell)


class Block(Board):
    def __init__(self, index):
        super().__init__()
        self.color1 = (255, 255, 235)
        self.color2 = (235, 60, 10)
        self.val = 1
        self.index = index
        self.font = pg.font.SysFont("Arial", self.size // 10)
        self.text_color = (55, 50, 40)

    def get_row_col(self):
        return self.index // 4, self.index % 4

    def get_color(self):
        c1 = np.array(self.color1)
        c2 = np.array(self.color2)
        return tuple((c2 - c1) * (self.val - 1) / 10 + c1)

    def draw(self, surface):
        rect = pg.draw.rect(surface, self.get_color(), self.cells[self.index])
        text = self.font.render(str(2**self.val), True, self.text_color)
        surface.blit(text, text.get_rect(center=rect.center))


class Game:
    def __init__(self):
        self.board = Board()
        self.cell_values = np.full((4, 4), None)
        self.available_cells = set(range(16))
        for _ in range(2):
            self.generate_block()

    def print_board(self):
        """Print the current board state"""
        print("\nCurrent board state:")
        for i in range(4):
            row = []
            for j in range(4):
                block = self.cell_values[i, j]
                if block is None:
                    row.append("None")
                else:
                    row.append(str(2**block.val))
            print(" ".join(f"{val:>4}" for val in row))
        print()

    def reset(self):
        # reset cells
        self.cell_values = np.full((4, 4), None)
        self.available_cells = set(range(16))
        # initialize with 2 random cells with number 2
        for _ in range(2):
            self.generate_block()

    def generate_block(self):
        """
        Generate a new random 2 for an empty cell
        """
        index = random.choice(tuple(self.available_cells))
        self.available_cells.remove(index)
        block = Block(index)
        self.cell_values[block.get_row_col()] = block

    def has_board_changed(self, old_state, new_state):
        """
        Check if the board state has changed by comparing values and positions
        """
        if old_state.shape != new_state.shape:
            return True
            
        for i in range(old_state.shape[0]):
            for j in range(old_state.shape[1]):
                old_block = old_state[i, j]
                new_block = new_state[i, j]
                
                # If one is None and the other isn't, state changed
                if (old_block is None) != (new_block is None):
                    return True
                    
                # If both are blocks, compare their values
                if old_block is not None and new_block is not None:
                    if old_block.val != new_block.val:
                        return True
                        
        return False

    def move_left(self, cell_values):
        """
        Move all blocks to the left, return the new board state
        """
        new_cv = np.full(cell_values.shape, None)
        for i, row in enumerate(cell_values):
            blocks = []
            merged = False
            for ele in row:
                if ele:
                    # Create a copy of the block to avoid modifying the original
                    block_copy = Block(ele.index)
                    block_copy.val = ele.val
                    
                    # add up adjacent numbers that are the same
                    if (not merged) and blocks and blocks[-1].val == block_copy.val:
                        blocks[-1].val += 1
                        merged = True
                    else:
                        blocks.append(block_copy)
                        merged = False
            new_cv[i, : len(blocks)] = blocks
        return new_cv

    def update(self, direction):
        """
        Update existing blocks based on direction
        Returns whether the board state changed
        """
        # move blocks in cell_values matrix to new positions
        if direction == DIR_UP:
            new_cv = self.move_left(self.cell_values.T)
            new_cv = new_cv.T
        elif direction == DIR_DOWN:
            new_cv = self.move_left(np.flip(self.cell_values.T))
            new_cv = np.flip(new_cv.T)
        elif direction == DIR_LEFT:
            new_cv = self.move_left(self.cell_values)
        elif direction == DIR_RIGHT:
            new_cv = self.move_left(np.flip(self.cell_values, axis=1))
            new_cv = np.flip(new_cv, axis=1)

        # check if the board state has changed
        changed = self.has_board_changed(self.cell_values, new_cv)
        if changed:
            self.cell_values = new_cv

            # update blocks with new index values
            # index = row * 4 + col
            self.available_cells = set(range(16))
            for i in range(len(self.cell_values)):
                for j in range(len(self.cell_values[0])):
                    if self.cell_values[i, j]:
                        index = i * 4 + j
                        self.cell_values[i, j].index = index
                        self.available_cells.remove(index)

        return changed

    def update_and_generate(self, direction):
        """
        Update existing blocks based on direction and generate new block if changed
        """
        changed = self.update(direction)
        if changed:
            self.generate_block()
            print("after move")
            self.print_board()

    def if_lose(self):
        """
        Check if there are valid next moves
        """
        if len(self.available_cells) > 0:
            return False
            
        # Check all possible moves
        # Up
        new_cv = self.move_left(self.cell_values.T)
        if self.has_board_changed(self.cell_values.T, new_cv):
            return False
            
        # Down
        new_cv = self.move_left(np.flip(self.cell_values.T))
        if self.has_board_changed(np.flip(self.cell_values.T), new_cv):
            return False
            
        # Left
        new_cv = self.move_left(self.cell_values)
        if self.has_board_changed(self.cell_values, new_cv):
            return False
            
        # Right
        new_cv = self.move_left(np.flip(self.cell_values, axis=1))
        if self.has_board_changed(np.flip(self.cell_values, axis=1), new_cv):
            return False
            
        return True
