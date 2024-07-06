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

    def move_left(self, cell_values):
        """
        Move all blocks to the left
        Check if cell_values changed
        """
        new_cv = np.full(cell_values.shape, None)
        for i, row in enumerate(cell_values):
            blocks = []
            merged = False
            for ele in row:
                if ele:
                    # add up adjacent numbers that are the same
                    if (not merged) and blocks and blocks[-1].val == ele.val:
                        blocks[-1].val += 1
                        merged = True
                    else:
                        blocks.append(ele)
                        merged = False
            new_cv[i, : len(blocks)] = blocks
        # if cell_values didn't change, this is an invalid move
        changed = not (cell_values == new_cv).all()
        return changed, new_cv

    def update(self, direction):
        """
        Update existing blocks based on direction
        Generate a new random block
        """
        # move blocks in cell_values matrix to new positions
        if direction == DIR_UP:
            changed, new_cv = self.move_left(self.cell_values.T)
            new_cv = new_cv.T
        elif direction == DIR_DOWN:
            changed, new_cv = self.move_left(np.flip(self.cell_values.T))
            new_cv = np.flip(new_cv.T)
        elif direction == DIR_LEFT:
            changed, new_cv = self.move_left(self.cell_values)
        elif direction == DIR_RIGHT:
            changed, new_cv = self.move_left(np.flip(self.cell_values, axis=1))
            new_cv = np.flip(new_cv, axis=1)

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

            # generate new block after each move
            self.generate_block()
