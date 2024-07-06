import pygame as pg
from game import Game
from constants import WINDOW_SIZE, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP


def main():
    pg.init()
    g = Game()
    surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    # initialize with 2 random cells with number 2
    for _ in range(2):
        g.generate_block()

    # start game
    loop = True
    while loop:
        surface.fill((250, 248, 240))
        g.board.draw(surface)
        for row in g.cell_values:
            for ele in row:
                if ele: 
                    ele.draw(surface)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    g.update(DIR_UP)
                elif event.key == pg.K_DOWN:
                    g.update(DIR_DOWN)
                elif event.key == pg.K_LEFT:
                    g.update(DIR_LEFT)
                elif event.key == pg.K_RIGHT:
                    g.update(DIR_RIGHT)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main() 