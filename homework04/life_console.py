import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.life = life

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        # y, x = screen.getmaxyx()
        # y-=3
        # x-=2
        # border_line = '+' + (x * '-') + '+'
        # screen.addstr(0, 0, border_line)
        # screen.addstr(y + 1, 0, border_line)
        # for i in range(0,y):
        #   screen.addstr(1 + i, 0, '|')
        #  screen.addstr(1 + i, x + 1, '|')
        # screen.refresh()"
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation
        for i in range(len(grid)):
            screen.addstr(i + 1, 1, "".join(map(str, grid[i])).replace("1", "*").replace("0", " "))

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        screen.nodelay(True)
        screen.resize(self.life.rows + 3, self.life.cols + 3)

        self.draw_borders(screen)
        while screen.getch() != ord("e"):
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
        curses.endwin()
