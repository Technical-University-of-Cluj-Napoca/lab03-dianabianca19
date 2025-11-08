import pygame
from utils import *
from grid import Grid
from searching_algorithms import *


GRID_WIDTH=600
GRID_HEIGHT=600
BUTTON_WIDTH=180
BUTTON_HEIGHT=40
BUTTON_MARGIN=10
GRID_ROWS=30
GRID_COLS= 30


COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'GREY': (128, 128, 128),
    'TURQUOISE': (64, 224, 208)
}

pygame.init()
WIN = pygame.display.set_mode((GRID_WIDTH + BUTTON_WIDTH + 3*BUTTON_MARGIN, GRID_HEIGHT))
pygame.display.set_caption("Path Visualizing Algorithm")
FONT = pygame.font.SysFont('Arial', 18)


class Button:
    def __init__(self, x, y, w, h, color, text, callback):
        self.rect=pygame.Rect(x, y, w, h)
        self.color=color
        self.text=text
        self.callback=callback

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        text_surf=FONT.render(self.text, True, (0, 0, 0))
        text_rect=text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def click(self):
        self.callback()


def main():
    grid=Grid(WIN, GRID_ROWS, GRID_COLS, GRID_WIDTH, GRID_HEIGHT)
    start=None
    end=None
    started=False

    def run_bfs():
        nonlocal started
        if start and end:
            started=True
            bfs(lambda: draw_all(), grid, start, end)
            started=False

    def run_dfs():
        nonlocal started
        if start and end:
            started=True
            dfs(lambda: draw_all(), grid, start, end)
            started=False

    def run_astar():
        nonlocal started
        if start and end:
            started = True
            astar(lambda: draw_all(), grid, start, end)
            started = False

    def run_dls():
        nonlocal started
        if start and end:
            started=True
            dls(lambda: draw_all(), grid, start, end)
            started=False

    def run_ucs():
        nonlocal started
        if start and end:
            started=True
            ucs(lambda: draw_all(), grid, start, end)
            started=False

    def run_greedy():
        nonlocal started
        if start and end:
            started=True
            greedy(lambda: draw_all(), grid, start, end)
            started=False

    def run_iddfs():
        nonlocal started
        if start and end:
            started=True
            iddfs(lambda: draw_all(), grid, start, end)
            started=False

    def run_ida():
        nonlocal started
        if start and end:
            started=True
            ida(lambda: draw_all(), grid, start, end)
            started=False

    def clear_grid():
        nonlocal start, end
        start=None
        end=None
        grid.reset()

    button_colors=[(200, 200, 0), (200, 100, 0), (0, 200, 200), (200, 0, 200),
                     (0, 150, 150), (150, 0, 150), (150, 150, 0), (100, 100, 200)]
    button_texts=["BFS", "DFS", "A*", "DLS", "UCS", "Greedy", "IDDFS", "IDA"]
    button_callbacks=[run_bfs, run_dfs, run_astar, run_dls, run_ucs, run_greedy, run_iddfs, run_ida]

    buttons=[]
    for i in range(len(button_texts)):
        x=GRID_WIDTH+2*BUTTON_MARGIN
        y=BUTTON_MARGIN+i*(BUTTON_HEIGHT+BUTTON_MARGIN)
        buttons.append(Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, button_colors[i%len(button_colors)],
                              button_texts[i], button_callbacks[i]))

    def draw_all():
        WIN.fill((220, 220, 220))

        for row in grid.grid:
            for spot in row:
                spot.draw(WIN)
        grid.draw_grid_lines()

        for button in buttons:
            button.draw(WIN)

        pygame.display.update()


    run=True
    while run:
        draw_all()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0]<GRID_WIDTH and pos[1]<GRID_HEIGHT:
                    row, col=grid.get_clicked_pos(pos)
                    if row<GRID_ROWS and col<GRID_COLS:
                        spot=grid.grid[row][col]
                        if not start and spot!=end:
                            start=spot
                            start.make_start()
                        elif not end and spot!=start:
                            end=spot
                            end.make_end()
                        elif spot!=start and spot!=end:
                            spot.make_barrier()
                else:
                    for button in buttons:
                        if button.rect.collidepoint(pos):
                            button.click()

            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                if pos[0]<GRID_WIDTH and pos[1]<GRID_HEIGHT:
                    row, col = grid.get_clicked_pos(pos)
                    spot=grid.grid[row][col]
                    spot.reset()
                    if spot==start:
                        start=None
                    elif spot==end:
                        end=None

            if event.type==pygame.KEYDOWN:
                if (event.key==
                        pygame.K_c):
                    clear_grid()

    pygame.quit()


if __name__ == "__main__":
    main()