import sys
import pygame as pg
pg.init()

FPS = 60

BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
GRAY    = (204, 204, 204)

myFont = pg.font.SysFont("Times New Roman", 18)

W_BOX, H_BOX, M_BOX  = 40, 40, 8
size = (1000, 1000)

screen = pg.display.set_mode(size)
pg.display.set_caption("Suduko Solver")

grid = np.zeros((9, 9))
arr = [
    [0, 8, 0, 0, 3, 2, 0, 0, 1],
    [7, 0, 3, 0, 8, 0, 0, 0, 2],
    [5, 0, 0, 0, 0, 7, 0, 3, 0],
    [0, 5, 0, 0, 0, 1, 9, 7, 0],
    [6, 0, 0, 7, 0, 9, 0, 0, 8],
    [0, 4, 7, 2, 0, 0, 0, 5, 0],
    [0, 2, 0, 6, 0, 0, 0, 0, 9],
    [8, 0, 0, 0, 9, 0, 3, 0, 5],
    [3, 0, 0, 8, 2, 0, 0, 1, 0],
]

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            col = pos[0] // (W_BOX + M_BOX)
            row = pos[1] // (H_BOX + M_BOX)
            grid[row][col] = 1

    screen.fill(BLACK)
    for row in range(9):
        for col in range(9):
            color = WHITE
            if grid[row][col] == 1:
                color = GRAY
                pygame.draw.rect(screen,
                                 color,
                                 [(M_BOX + W_BOX) * col + M_BOX,
                                 (M_BOX + H_BOX) * row + M_BOX,
                                  W_BOX, H_BOX])
            if arr[row][col] == sol_arr[row][col]:
                screen.blit(myFont.render(arr[row][col], GREEN),
                                        ((M_BOX + W_BOX // 2) * col + M_BOX,
                                        (M_BOX + H_BOX // 2) * row + M_BOX
                                        ))
            else:
                screen.blit(myFont.render(arr[row][col], RED),
                                        ((M_BOX + W_BOX // 2) * col + M_BOX,
                                        (M_BOX + H_BOX // 2) * row + M_BOX
                                        ))
    clock.tick(FPS)
    pg.display.flip()
