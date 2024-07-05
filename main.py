import pygame as pg
import numpy as np


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
    def __init__(self, surface, row, col):
        super().__init__(surface)
        self.color = (255, 255, 0)
        self.val = 0
        self.row = row
        self.col = col
        self.font = pg.font.SysFont('Arial',40)
    
    def get_rect(self):
        return self.cells[self.row * 4 + self.col] 

    def draw(self):
        rect = pg.draw.rect(self.surface, self.color, self.get_rect())
        text = self.font.render(str(self.val), True, (0,0,0))
        self.surface.blit(text, text.get_rect(center=rect.center))


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.loop = True
        self.board = Board(self.surface)
        self.cell_values = np.full((4, 4), None)

        self.cell_values[0, 2] = Block(self.surface, 0, 2)
        self.cell_values[0, 3] = Block(self.surface, 0, 3)
        self.cell_values[2, 2] = Block(self.surface, 2, 2)

    def main(self):
        while self.loop:
            self.game_loop()
        pg.quit()

    def move_left(self, cell_values):
        new_cv = np.full(cell_values.shape, None)
        for i, row in enumerate(cell_values):
            blocks = [x for x in row if x]
            new_cv[i, :len(blocks)] = blocks
        return new_cv

    def move(self, direction):
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

        # update blocks with new row & col values
        for i in range(len(self.cell_values)):
            for j in range(len(self.cell_values[0])):
                if self.cell_values[i, j]:
                    self.cell_values[i, j].row = i
                    self.cell_values[i, j].col = j
            

    def game_loop(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.move(DIR_UP)
        if keys[pg.K_DOWN]:
            self.move(DIR_DOWN)
        if keys[pg.K_LEFT]:
            self.move(DIR_LEFT)
        if keys[pg.K_RIGHT]:
            self.move(DIR_RIGHT)

        self.surface.fill((250, 248, 240))
        self.board.draw()
        for row in self.cell_values:
            for ele in row:
                if ele: ele.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
        pg.display.update()


if __name__ == "__main__":
    mygame = Game()
    mygame.main() 