import pygame as pg


WINDOW_SIZE = 500
BOARD_SIZE = 400

class Board:
    def __init__(self, surface):
        self.surface = surface
        self.size = BOARD_SIZE
        self.bg_color = (185, 173, 161)
        self.pos = (WINDOW_SIZE - self.size) / 2
        self.available_cells = []
        self.cell_color = (202, 193, 181)

        gap = 10
        s = (BOARD_SIZE - gap) / 4
        for i in range(4):
            for j in range(4):
                x = self.pos + gap + s*j
                y = self.pos + gap + s*i
                self.available_cells.append(pg.Rect(x, y, s-gap, s-gap))

    def draw(self):
        pg.draw.rect(self.surface, self.bg_color, pg.Rect(self.pos, self.pos, self.size, self.size))
        for cell in self.available_cells:
            pg.draw.rect(self.surface, self.cell_color, cell)


class Block(Board):
    def __init__(self, surface, row, col):
        super().__init__(surface)
        self.color = (255, 255, 0)
        self.val = 0
        self.row = row
        self.col = col
    
    def get_rect(self):
        return self.available_cells[self.row * 4 + self.col] 

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.get_rect())

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.col = 3
        if left:
            self.col = 0
        if down:
            self.row = 3
        if up:
            self.row = 0


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.loop = True
        self.board = Board(self.surface)
        self.block = Block(self.surface, 0, 0)

    def main(self):
        while self.loop:
            self.game_loop()
        pg.quit()

    def game_loop(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.block.move(up=True)
        if keys[pg.K_DOWN]:
            self.block.move(down=True)
        if keys[pg.K_LEFT]:
            self.block.move(left=True)
        if keys[pg.K_RIGHT]:
            self.block.move(right=True)

        self.surface.fill((250, 248, 240))
        self.board.draw()
        self.block.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
        pg.display.update()


if __name__ == "__main__":
    mygame = Game()
    mygame.main() 