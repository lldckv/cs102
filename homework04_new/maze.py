from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    # grid[coord[0]][coord[1]] = " "
    if (coord[1] + 2) < len(grid[0]):
        grid[coord[0]][coord[1] + 1] = " "
    elif coord[0] > 0:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x in range(1, len(grid), 2):
        for y in range(1, len(grid[0]), 2):
            remove_wall(grid, (x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    res = list()
    for x, row in enumerate(grid):
        if row.count("X") == 1:
            res.append((x, row.index("X")))
        elif row.count("X") == 2:
            res.append((x, row.index("X")))
            res.append((x, len(row) - 1 - row[::-1].index("X")))
    return res


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == k:
                if x != 0 and grid[x - 1][y] != "■":
                    if int(grid[x - 1][y]) > k + 1 or int(grid[x - 1][y]) == 0:
                        grid[x - 1][y] = k + 1
                if (x != (len(grid) - 1)) and grid[x + 1][y] != "■":
                    if int(grid[x + 1][y]) > k + 1 or int(grid[x + 1][y]) == 0:
                        grid[x + 1][y] = k + 1
                if y != 0 and grid[x][y - 1] != "■":
                    if int(grid[x][y - 1]) > k + 1 or int(grid[x][y - 1]) == 0:
                        grid[x][y - 1] = k + 1
                if (y != (len(grid[0]) - 1)) and grid[x][y + 1] != "■":
                    if int(grid[x][y + 1]) > k + 1 or int(grid[x][y + 1]) == 0:
                        grid[x][y + 1] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    path = list()
    k = int(grid[exit_coord[0]][exit_coord[1]])
    path.append((exit_coord[0], exit_coord[1]))
    while k > 1:  # Type : Ignore
        if len(path) == 1:
            if exit_coord[0] == 0:
                path.append((exit_coord[0] + 1, exit_coord[1]))
            elif exit_coord[0] == len(grid) - 1:
                path.append((exit_coord[0] - 1, exit_coord[1]))
            elif exit_coord[1] == 0:
                path.append((exit_coord[0], exit_coord[1] + 1))
            else:
                path.append((exit_coord[0], exit_coord[1] - 1))
            k = k - 1  # Type : Ignore
        else:
            if grid[path[-1][0] - 1][path[-1][1]] == k - 1:
                path.append((path[-1][0] - 1, path[-1][1]))
                k = k - 1
            elif grid[path[-1][0] + 1][path[-1][1]] == k - 1:
                path.append((path[-1][0] + 1, path[-1][1]))
                k = k - 1
            elif grid[path[-1][0]][path[-1][1] - 1] == k - 1:
                path.append((path[-1][0], path[-1][1] - 1))
                k = k - 1
            elif grid[path[-1][0]][path[-1][1] + 1] == k - 1:
                path.append((path[-1][0], path[-1][1] + 1))
                k = k - 1
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    if (coord[0] % (len(grid) - 1)) == (coord[1] % (len(grid[0]) - 1)):
        return True
    if (coord[0] % (len(grid) - 1)) == 0 and (grid[max((coord[0] - 1), (1 - coord[0]))][coord[1]] != " "):
        return True
    if (coord[1] % (len(grid[0]) - 1)) == 0 and (grid[coord[0]][max((coord[1] - 1), (1 - coord[1]))] != " "):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:  # Type : Ignore
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits
    for i in exits:
        if encircled_exit(grid, i):
            return grid, None
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] != "■":
                grid[x][y] = 0

    grid[exits[0][0]][exits[0][1]] = 1
    k = 1
    while grid[exits[1][0]][exits[1][1]] == 0:
        make_step(grid, k)
        k = k + 1

    return grid, shortest_path(grid, exits[1])


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
