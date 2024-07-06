import pygame as pg
from game import Game
from constants import WINDOW_SIZE, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP


def main():
    pg.init()
    pg.display.set_caption("2048")
    g = Game()
    surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    title_font = pg.font.SysFont("Arial", 80)
    font = pg.font.SysFont("Arial", 20)

    # start game
    loop = True
    game_status = "game"
    while loop:
        if game_status == "game":
            surface.fill((250, 248, 240))
            g.board.draw(surface)
            for row in g.cell_values:
                for ele in row:
                    if ele:
                        ele.draw(surface)
                        # reach 2**11 = 2048, win
                        if ele.val == 11:
                            game_status = "win"
            # no available cells, lose
            if game_status == "game" and (not g.available_cells):
                game_status = "lose"
            # display results
            if game_status != "game":
                s = pg.Surface((WINDOW_SIZE, WINDOW_SIZE), pg.SRCALPHA)
                s.fill((55, 50, 40, 120))
                surface.blit(s, (0, 0))
                if game_status == "win":
                    text = title_font.render("You Won!", True, (255, 255, 255))
                    surface.blit(
                        text,
                        (
                            WINDOW_SIZE / 2 - text.get_width() / 2,
                            WINDOW_SIZE / 2 - text.get_height() / 2 - 30,
                        ),
                    )
                elif game_status == "lose":
                    text = title_font.render("You Lost ...", True, (255, 255, 255))
                    surface.blit(
                        text,
                        (
                            WINDOW_SIZE / 2 - text.get_width() / 2,
                            WINDOW_SIZE / 2 - text.get_height() / 2 - 30,
                        ),
                    )
                text = font.render("press space to restart", True, (255, 255, 255))
                surface.blit(
                    text,
                    (
                        WINDOW_SIZE / 2 - text.get_width() / 2,
                        WINDOW_SIZE / 2 - text.get_height() / 2 + 30,
                    ),
                )
                text = font.render("press q to end the game", True, (255, 255, 255))
                surface.blit(
                    text,
                    (
                        WINDOW_SIZE / 2 - text.get_width() / 2,
                        WINDOW_SIZE / 2 - text.get_height() / 2 + 55,
                    ),
                )

        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            elif event.type == pg.KEYDOWN:
                # move
                if event.key == pg.K_UP:
                    g.update(DIR_UP)
                elif event.key == pg.K_DOWN:
                    g.update(DIR_DOWN)
                elif event.key == pg.K_LEFT:
                    g.update(DIR_LEFT)
                elif event.key == pg.K_RIGHT:
                    g.update(DIR_RIGHT)
                # restart
                elif event.key == pg.K_SPACE:
                    game_status = "game"
                    g.reset()
                # end
                elif event.key == pg.K_q:
                    loop = False
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
