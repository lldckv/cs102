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
    c = randint(0, 1)
    if c == 0:
        if coord[0] == 1 and coord[1] != len(grid) - 2:
            grid[coord[0]][coord[1] + 1] = " "
        elif coord[0] > 1:
            grid[coord[0] - 1][coord[1]] = " "
    else:
        if coord[1] == len(grid) - 2 and coord[0] != 1:
            grid[coord[0] - 1][coord[1]] = " "
        elif coord[1] != len(grid) - 2:
            grid[coord[0]][coord[1] + 1] = " "

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

    for i in empty_cells:
        grid = remove_wall(grid, i)

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
    return [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == "X"]


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
                    if int(grid[x - 1][y]) == 0:
                        grid[x - 1][y] = k + 1
                if (x != (len(grid) - 1)) and grid[x + 1][y] != "■":
                    if int(grid[x + 1][y]) == 0:
                        grid[x + 1][y] = k + 1
                if y != 0 and grid[x][y - 1] != "■":
                    if int(grid[x][y - 1]) == 0:
                        grid[x][y - 1] = k + 1
                if (y != (len(grid[0]) - 1)) and grid[x][y + 1] != "■":
                    if int(grid[x][y + 1]) == 0:
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
    copy_grid = deepcopy(grid)
    x, y = exit_coord
    ex = int(copy_grid[x][y])
    k = int(ex)
    path = [exit_coord]

    while k > 0:
        if x != 0 and copy_grid[x - 1][y] == k - 1:
            x -= 1
            path.append((x, y))
        elif x != len(copy_grid) - 1 and copy_grid[x + 1][y] == k - 1:
            x += 1
            path.append((x, y))
        elif y != 0 and copy_grid[x][y - 1] == k - 1:
            y -= 1
            path.append((x, y))
        elif y != len(copy_grid[0]) - 1 and copy_grid[x][y + 1] == k - 1:
            y += 1
            path.append((x, y))
        k -= 1

    if len(path) != ex:
        x, y = path[-1]
        copy_grid[x][y] = " "
        return shortest_path(grid, exit_coord)

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    return (
        (coord[0] % (len(grid) - 1)) == (coord[1] % (len(grid[0]) - 1))
        or ((coord[0] % (len(grid) - 1)) == 0 and (grid[abs(coord[0] - 1)][coord[1]] == "■"))
        or ((coord[1] % (len(grid[0]) - 1)) == 0 and (grid[coord[0]][abs(coord[1] - 1)] == "■"))
    )


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:  # Type : Ignore
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if (
        (len(exits) < 2)
        or (exits[0][0] == exits[1][0] and abs(exits[0][1] - exits[1][1]) == 1)
        or (exits[0][1] == exits[1][1] and abs(exits[0][0] - exits[1][0]) == 1)
    ):
        return grid, exits

    if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return grid, None

    for x, row in enumerate(grid):
        for y, column in enumerate(row):
            if column == " ":
                row[y] = 0

    en = exits[0]
    ex = exits[1]
    grid[en[0]][en[1]] = 1
    grid[ex[0]][ex[1]] = 0
    k = 0
    while grid[ex[0]][ex[1]] == 0:
        k += 1
        grid = make_step(grid, k)

    return grid, shortest_path(grid, ex)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """
    print(pd.DataFrame(grid))

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
