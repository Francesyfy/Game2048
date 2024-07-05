import pygame as pg
import numpy as np
import random

WINDOW_SIZE = 500
BOARD_SIZE = 400

DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4


class Board:
    def __init__(self, surface):
        self.surface = surface
        self.size = BOARD_SIZE
        self.bg_color = (185, 173, 161)
        self.pos = (WINDOW_SIZE - self.size) / 2
        self.cells = []
        self.cell_color = (202, 193, 181)

        gap = 10
        s = (BOARD_SIZE - gap) / 4
        for i in range(4):
            for j in range(4):
                x = self.pos + gap + s*j
                y = self.pos + gap + s*i
                self.cells.append(pg.Rect(x, y, s-gap, s-gap))

    def draw(self):
        pg.draw.rect(self.surface, self.bg_color, pg.Rect(self.pos, self.pos, self.size, self.size))
        for cell in self.cells:
            pg.draw.rect(self.surface, self.cell_color, cell)


class Block(Board):
    def __init__(self, surface, index):
        super().__init__(surface)
        self.color = (255, 255, 0)
        self.val = 2
        self.index = index
        self.font = pg.font.SysFont('Arial',40)
    
    def get_row_col(self):
        return self.index // 4, self.index % 4

    def draw(self):
        rect = pg.draw.rect(self.surface, self.color, self.cells[self.index])
        text = self.font.render(str(self.val), True, (0,0,0))
        self.surface.blit(text, text.get_rect(center=rect.center))


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.loop = True
        self.board = Board(self.surface)
        self.cell_values = np.full((4, 4), None)
        self.available_cells = set(range(16))

    def main(self):
        # initialize with 2 random cells with number 2
        for _ in range(2):
            self.generate_block()
        # start game
        while self.loop:
            self.game_loop()
        pg.quit()
    
    def generate_block(self):
        """
        Generate a new random 2 for an empty cell
        """
        index = random.choice(tuple(self.available_cells))
        self.available_cells.remove(index)
        block =  Block(self.surface, index)
        self.cell_values[block.get_row_col()] = block

    def move_left(self, cell_values):
        """
        Move all blocks to the left
        """
        new_cv = np.full(cell_values.shape, None)
        for i, row in enumerate(cell_values):
            blocks = [x for x in row if x]
            new_cv[i, :len(blocks)] = blocks
        return new_cv
    
    def update(self, direction):
        """
        Update existing blocks based on direction
        Generate a new random block
        """
        # move blocks in cell_values matrix to new positions
        if direction == DIR_UP:
            self.cell_values = self.move_left(self.cell_values.T).T
        elif direction == DIR_DOWN:
            temp = np.flip(self.cell_values.T)
            self.cell_values = np.flip(self.move_left(temp).T)
        elif direction == DIR_LEFT:
            self.cell_values = self.move_left(self.cell_values)
        else:
            temp = np.flip(self.cell_values, axis=1)
            self.cell_values = np.flip(self.move_left(temp), axis=1)

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
            

    def game_loop(self):
        self.surface.fill((250, 248, 240))
        self.board.draw()
        for row in self.cell_values:
            for ele in row:
                if ele: ele.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.update(DIR_UP)
                elif event.key == pg.K_DOWN:
                    self.update(DIR_DOWN)
                elif event.key == pg.K_LEFT:
                    self.update(DIR_LEFT)
                elif event.key == pg.K_RIGHT:
                    self.update(DIR_RIGHT)
        pg.display.update()


if __name__ == "__main__":
    mygame = Game()
    mygame.main() 